from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY가 .env 파일에 없습니다.")

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

response = llm.invoke("안녕! 한 줄로 자기소개해줘.")
print(response.content)