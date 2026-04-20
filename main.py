from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from .rag import extract_order_id, get_order_details, get_policy_info

load_dotenv()

app = FastAPI()

# --- Request Schema ---
class QueryRequest(BaseModel):
    query: str


# --- LLM Setup ---
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

prompt = PromptTemplate(
    input_variables=["query", "order_data", "policy_data"],
    template="""
You are a retail customer support assistant.

User Query:
{query}

Order Data:
{order_data}

Policy Info:
{policy_data}

Provide a clear, professional response.
"""
)

chain = LLMChain(llm=llm, prompt=prompt)


# --- API Endpoint ---
@app.post("/ask")
def ask(request: QueryRequest):

    query = request.query

    # 1. Extract order id
    order_id = extract_order_id(query)

    # 2. Get DB data
    order_data = get_order_details(order_id) if order_id else None

    # 3. Get policy data
    policy_data = get_policy_info(query)

    # 4. LLM response
    response = chain.run({
        "query": query,
        "order_data": order_data,
        "policy_data": policy_data
    })

    return {"answer": response}
