import time
from dataclasses import dataclass, field
from datetime import datetime

from agent import GridMindAgent


GROQ_PRICING = {
    "openai/gpt-oss-20b": {"input": 0.075, "output": 0.30},
}


def calculate_cost(model, prompt_tokens, completion_tokens):
    pricing = GROQ_PRICING.get(model)
    if pricing is None:
        return 0.0
    return (
        prompt_tokens * pricing["input"] + completion_tokens * pricing["output"]
    ) / 1_000_000


@dataclass
class LLMCallRecord:
    model: str
    question: str
    instructions: str
    answer: str
    llm_calls: int
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    response_time: float
    cost: float
    timestamp: datetime = field(default_factory=datetime.now)


class GridMindAgentWithMetrics(GridMindAgent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_call: LLMCallRecord = None
        self._llm_calls = 0
        self._prompt_tokens = 0
        self._completion_tokens = 0

    def llm(self, messages, tools=None):
        response = super().llm(messages, tools=tools)

        usage = response.usage
        self._llm_calls += 1
        self._prompt_tokens += usage.prompt_tokens
        self._completion_tokens += usage.completion_tokens

        return response

    def chat(self, question):
        self._llm_calls = 0
        self._prompt_tokens = 0
        self._completion_tokens = 0

        start_time = time.time()
        answer = super().chat(question)
        response_time = time.time() - start_time

        total_tokens = self._prompt_tokens + self._completion_tokens
        cost = calculate_cost(self.model, self._prompt_tokens, self._completion_tokens)

        call_record = LLMCallRecord(
            model=self.model,
            question=question,
            instructions=self.rag.instructions,
            answer=answer,
            llm_calls=self._llm_calls,
            prompt_tokens=self._prompt_tokens,
            completion_tokens=self._completion_tokens,
            total_tokens=total_tokens,
            response_time=response_time,
            cost=cost,
        )

        print(call_record)
        self.last_call = call_record

        return answer
