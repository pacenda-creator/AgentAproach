from typing import TypedDict
from langgraph.graph import StateGraph, END


class State(TypedDict):
    question: str
    intent: str
    answer: str

def route(state):
    return state["intent"]

def hello_node(state):
    print ("start")
    return {}

def router_node(state):
    print ("router")
    return {
        "intent": "sales"
    }

def billing_node(state):
    return {"answer": "Poslední faktura: 499 Kč"}

def sales_node(state):
    return {"answer": "Doporučuji tarif Premium"}


graph = StateGraph(State)

graph.add_node("hello", hello_node)
graph.add_node("billing", billing_node)
graph.add_node("sales", sales_node)
graph.add_node("router", router_node)

graph.set_entry_point("hello")
                      
graph.add_conditional_edges(
    "router",
    route,
    {
        "billing": "billing",
        "sales": "sales"
    }
)

graph.add_edge("hello", "router")
graph.add_edge("billing", END)
graph.add_edge("sales", END)

app = graph.compile()

result = app.invoke({"question": "Jaká je moje faktura?"})

print(result)