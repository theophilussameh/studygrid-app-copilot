import time

from tqdm.auto import tqdm


# Groq pricing for openai/gpt-oss-20b (per million tokens)
# Source: https://groq.com/pricing — last checked 2026-08-02
INPUT_PRICE_PER_MILLION = 0.075
OUTPUT_PRICE_PER_MILLION = 0.30


def calc_call_cost(usage):
    input_cost = (usage.input_tokens / 1_000_000) * INPUT_PRICE_PER_MILLION
    output_cost = (usage.output_tokens / 1_000_000) * OUTPUT_PRICE_PER_MILLION
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