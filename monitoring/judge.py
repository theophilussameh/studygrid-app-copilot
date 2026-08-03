import os
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel

from evaluation.evaluation_utils import generate_structured_with_retry, calc_call_cost


class RelevanceVerdict(BaseModel):
    relevance: Literal["NON_RELEVANT", "PARTLY_RELEVANT", "RELEVANT"]
    explanation: str


JUDGE_INSTRUCTIONS = """
You are an expert evaluator for GridMind, a RAG-based assistant that
answers questions about StudyGrid.
Analyze the relevance of the generated answer to the given question.

Classify the answer as:
- RELEVANT: the answer addresses the question
- PARTLY_RELEVANT: the answer partially addresses the question
- NON_RELEVANT: the answer does not address the question
""".strip()

JUDGE_PROMPT = """
Question: {question}
Generated Answer: {answer}
""".strip()

# Reused deliberately: evaluation/evaluation_utils.py already has a
# retrying structured-output helper (generate_structured_with_retry)
# and a Groq cost calculator (calc_call_cost) from the evaluation
# module. Both assume the Responses API's usage shape
# (usage.input_tokens / usage.output_tokens) — different from
# agent.py's Chat Completions usage shape, which is why metrics.py
# has its own calculate_cost() rather than sharing this one.

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1",
        )
    return _client


def evaluate_relevance(question, answer, client=None):
    if client is None:
        client = _get_client()

    prompt = JUDGE_PROMPT.format(question=question, answer=answer)

    result, usage = generate_structured_with_retry(
        client,
        JUDGE_INSTRUCTIONS,
        prompt,
        RelevanceVerdict,
    )

    cost = calc_call_cost(usage)["total_cost"]

    return result.relevance, result.explanation, cost