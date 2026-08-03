from dotenv import load_dotenv
from openai import OpenAI
import os

from ingest import load_faq_data
from retriever import Retriever
from prompts import INSTRUCTIONS, USER_PROMPT_TEMPLATE
from monitoring.metrics import GridMindAgentWithMetrics

load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

documents = load_faq_data()

retriever = Retriever(
    documents=documents,
    instructions=INSTRUCTIONS,
    prompt_template=USER_PROMPT_TEMPLATE,
)

agent = GridMindAgentWithMetrics(
    retriever=retriever,
    openai_client=openai_client,
    model="openai/gpt-oss-20b"
)