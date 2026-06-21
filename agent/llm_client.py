import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("BASE_URL")
MODEL = os.getenv("MODEL", "gpt-4o-mini")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)
