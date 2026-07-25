from dotenv import load_dotenv
from openai import OpenAI
import os

from ingest import load_faq_data, build_index
from retriever import Retriever
from agent import GridMindAgent

load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

documents = load_faq_data()
index = build_index(documents)

retriever = Retriever(
    index=index,
    openai_client=openai_client
)

agent = GridMindAgent(
    retriever=retriever,
    openai_client=openai_client,
    model="openai/gpt-oss-20b"
)

