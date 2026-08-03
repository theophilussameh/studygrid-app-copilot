import time

from tqdm.auto import tqdm


# Groq pricing per million tokens.
# Source: https://groq.com/pricing — last checked 2026-08-02
MODEL_PRICING = {
    "openai/gpt-oss-20b": {"input": 0.075, "output": 0.30},
    "openai/gpt-oss-120b": {"input": 0.15, "output": 0.60},
}
DEFAULT_MODEL_FOR_PRICING = "openai/gpt-oss-20b"


def calc_call_cost(usage, model=DEFAULT_MODEL_FOR_PRICING):
    # The Responses API (client.responses.parse) returns usage with
    # input_tokens/output_tokens. The Chat Completions API (used by
    # GridMindAgent, since Groq's chat.completions.create is what the
    # production agent calls) returns prompt_tokens/completion_tokens.
    # Support both so this function works for ground-truth generation
    # (Responses API) and agent evaluation (Chat Completions API) alike.
    input_tokens = getattr(usage, "input_tokens", None)
    output_tokens = getattr(usage, "output_tokens", None)

    if input_tokens is None:
        input_tokens = usage.prompt_tokens
    if output_tokens is None:
        output_tokens = usage.completion_tokens

    pricing = MODEL_PRICING.get(model, MODEL_PRICING[DEFAULT_MODEL_FOR_PRICING])

    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    total_cost = input_cost + output_cost

    return {
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
    }


def calc_total_cost(usages):
    total_cost = 0.0

    for usage in usages:
        cost = calc_call_cost(usage)
        total_cost = total_cost + cost["total_cost"]

    return total_cost


def generate_structured(client, instructions, user_prompt, output_type, model="openai/gpt-oss-20b", max_output_tokens=2000):
    messages = [
        {"role": "developer", "content": instructions},
        {"role": "user", "content": user_prompt}
    ]

    response = client.responses.parse(
        model=model,
        input=messages,
        text_format=output_type,
        max_output_tokens=max_output_tokens
    )

    return response.output_parsed, response.usage


def generate_structured_with_retry(
    client,
    instructions,
    user_prompt,
    output_type,
    model="openai/gpt-oss-20b",
    max_retries=5,
    base_wait_seconds=10,
):
    for attempt in range(max_retries):
        try:
            return generate_structured(
                client,
                instructions,
                user_prompt,
                output_type,
                model=model,
            )
        except Exception:
            if attempt == max_retries - 1:
                raise
            # Groq's free-tier TPM rate limit resets on the order of
            # several seconds, not milliseconds, so we wait longer than
            # a typical exponential backoff would.
            time.sleep(base_wait_seconds * (attempt + 1))


class GridMindAgentWithUsage:
    """
    Wraps the production GridMindAgent (agent.py) for evaluation.

    GridMindAgent.chat() can call the LLM multiple times in a single
    conversation (its tool-calling loop, up to max_iterations). The
    course's RAGWithUsage only ever makes one LLM call per question, so
    we can't reuse it as-is — we need to accumulate usage across every
    call in the loop, and separately track the tool calls the agent
    made (its "trajectory"), which we'll need for agent evaluation.

    We compose around GridMindAgent instead of subclassing it, so we
    don't have to duplicate or fight with its internal chat() loop.
    """

    def __init__(self, agent):
        self.agent = agent
        self.usages = []
        self.last_trajectory = []

        self._original_llm = agent.llm
        self._original_execute_tool = agent.execute_tool

        agent.llm = self._llm_with_tracking
        agent.execute_tool = self._execute_tool_with_tracking

    def _llm_with_tracking(self, messages, tools=None):
        response = self._original_llm(messages, tools=tools)

        if response.usage is not None:
            self.usages.append(response.usage)

        return response

    def _execute_tool_with_tracking(self, tool_call):
        tool_output = self._original_execute_tool(tool_call)

        self.last_trajectory.append({
            "tool": tool_call.function.name,
            "arguments": tool_call.function.arguments,
            "output": tool_output,
        })

        return tool_output

    def reset_usage(self):
        self.usages = []

    def chat(self, question):
        self.last_trajectory = []
        return self.agent.chat(question)

    def total_cost(self, model=None):
        model = model or self.agent.model
        total_cost = 0.0

        for usage in self.usages:
            cost = calc_call_cost(usage, model=model)
            total_cost = total_cost + cost["total_cost"]

        return total_cost


def map_progress(pool, seq, f):
    results = []

    with tqdm(total=len(seq)) as progress:
        futures = []

        for el in seq:
            future = pool.submit(f, el)
            future.add_done_callback(lambda p: progress.update())
            futures.append(future)

        for future in futures:
            result = future.result()
            results.append(result)

    return results