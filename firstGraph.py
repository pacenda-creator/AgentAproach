from typing import TypedDict
from langgraph.graph import StateGraph, END
from tools import get_invoice, get_tariff
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

import os


question = input("Napiš dotaz: ")

class State(TypedDict):
    question: str
    intent: str
    answer: str

def route(state):
    return state["intent"]

def router_node(state):

    question = state["question"]

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
        Jsi router.

        Možné intenty:
        billing
        sales
        unknown

        Vrať pouze intent.

        Dotaz:
        {question}
        """
    )

    intent = response.output_text.strip()

    return {
        "intent": intent
    }

def billing_node(state):
    return {"answer": get_invoice()}

def sales_node(state):
    return {"answer": get_tariff()}


graph = StateGraph(State)


graph.add_node("billing", billing_node)
graph.add_node("sales", sales_node)
graph.add_node("router", router_node)

graph.set_entry_point("router")
                      
graph.add_conditional_edges(
    "router",
    route,
    {
        "billing": "billing",
        "sales": "sales"
    }
)


graph.add_edge("billing", END)
graph.add_edge("sales", END)

app = graph.compile()

result = app.invoke({"question": question})

print(result["answer"])