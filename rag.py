import re
from sqlalchemy import text
from .db import engine

# --- Extract Order ID ---
def extract_order_id(query: str):
    match = re.search(r"\b\d{5}\b", query)
    return int(match.group()) if match else None


# --- SQL Retrieval ---
def get_order_details(order_id: int):
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


# --- Simple Policy Index (Vectorless RAG style) ---
POLICY_INDEX = {
    "return": "Items can be returned within 30 days.",
    "damaged": "Damaged items are eligible for full refund.",
    "delayed": "Delayed orders can be refunded or cancelled."
}

def get_policy_info(query: str):
    query = query.lower()
    matches = [v for k, v in POLICY_INDEX.items() if k in query]
    return " ".join(matches) if matches else "No policy found."
