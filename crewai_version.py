import os
import re
# from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from sqlalchemy import create_engine, text

from crewai import Agent, Task, Crew
# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["OPENAI_API_KEY"] = "***"
DATABASE_URL = "***"

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)

app = FastAPI(
    title="Retail Customer Support API",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    query: str

def extract_order_id(query: str):
    match = re.search(r"\b\d{5}\b", query)
    return int(match.group()) if match else None

def get_order_details(order_id: int):
    if not order_id:
        return None

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT status, delivery_date, amount
                FROM orders
                WHERE order_id=:id
            """),
            {"id": order_id}
        ).fetchone()

    if result:
        return {
            "status": result[0],
            "delivery_date": str(result[1]),
            "amount": float(result[2])
        }

    return None
 
POLICY_INDEX = {
    "return": "Items can be returned within 30 days.",
    "damaged": "Damaged items are eligible for full refund.",
    "delayed": "Delayed orders can be refunded or cancelled."
}

def get_policy_info(query: str):
    query = query.lower()
    matches = [v for k, v in POLICY_INDEX.items() if k in query]
    return " ".join(matches) if matches else "No policy found."


llm = "gpt-4o-mini"

router_agent = Agent(
    role="Router",
    goal="Decide whether the query is about order details or policy",
    backstory="Expert in classifying customer queries",
    llm=llm,
    verbose=True
)

order_agent = Agent(
    role="Order Specialist",
    goal="Fetch and explain order details",
    backstory="Expert in handling order database queries",
    llm=llm,
    verbose=True
)

policy_agent = Agent(
    role="Policy Expert",
    goal="Provide company policy information",
    backstory="Expert in return, refund, and delay policies",
    llm=llm,
    verbose=True
)

response_agent = Agent(
    role="Support Assistant",
    goal="Generate final response for the user",
    backstory="Professional customer support assistant",
    llm=llm,
    verbose=True
)


def route_query(query):

    router_task = Task(
        description=f"""
Classify this query:
"{query}"

Respond with ONLY one word:
- ORDER
- POLICY
""",
        expected_output="A single word: either ORDER or POLICY",
        agent=router_agent
    )

    crew = Crew(
        agents=[router_agent],
        tasks=[router_task]
    )

    decision = str(crew.kickoff()).strip().upper()

    return decision

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 80px auto; text-align: center;">
        <h1>Retail Support API</h1>
        <p>The API is running.</p>
        <a href="/docs" style="font-size: 18px;">Open Interactive Docs (Swagger UI)</a>
    </body>
    </html>
    """

@app.post("/ask")
def ask(request: QueryRequest):

    query = request.query

    # 1️⃣ Route decision
    decision = route_query(query)

    order_data = None
    policy_data = None

    # 2️⃣ Conditional execution
    if "ORDER" in decision :
        order_id = extract_order_id(query)
        order_data = get_order_details(order_id)

    elif "POLICY" in decision:
        policy_data = get_policy_info(query)

    # 3️⃣ Final response task
    final_task = Task(
    description=f"""User Query: {query}

Order Data: {order_data or 'No order data available.'}
Policy Data: {policy_data or 'No policy data available.'}

Generate a helpful and professional customer support response.""",
    expected_output="A clear, helpful, and professional customer support response",
    agent=response_agent
)

    crew = Crew(
        agents=[response_agent],
        tasks=[final_task]
    )

    final_response = crew.kickoff()

    return {
        "decision": decision,
        "answer": final_response,
        "order_data": order_data,
        "policy_data": policy_data
    }


if __name__ == "__main__":
    #import uvicorn
    #uvicorn.run("Agentic_retail_Customer_Support_Assistant:app", host="0.0.0.0", port=8000, reload=True)
    #if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 50)
    print("  Starting Retail Support API...")
    print("  Open: http://127.0.0.1:8000/docs")
    print("=" * 50 + "\n")
    uvicorn.run(
        "Agentic_retail_Customer_Support_Assistant:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
