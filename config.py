from dotenv import load_dotenv
from openai import OpenAI
import os

from ingest import load_faq_data, build_index
from rag_helper import RAGHelper
from agent import GridMindAgent

load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

documents = load_faq_data()
index = build_index(documents)

rag_helper = RAGHelper(
    index=index,
    openai_client=openai_client
)

agent = GridMindAgent(
    rag_helper=rag_helper,
    openai_client=openai_client,
    model="openai/gpt-oss-20b"
)