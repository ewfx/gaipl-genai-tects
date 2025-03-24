import os

#Embedding API keys directly in your code is definilty not secure or recommended for production environments.
#Always use proper key management practices.
os.environ["OPENAI_API_KEY"] = "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"

from Flows.core_graph import create_graph
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from Utilities.agent_response_management import get_history_object
import os


class UserInput(TypedDict):
    input: str
    continue_execution: bool

def get_operation(state: UserInput) -> UserInput:

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir,"Operations", "docs", "downtime.txt")

    f = open(file_path, "r")
    data = f.read()
    return {
        "input": data,
        "continue_conversation": False
    }

def process_operation(state: UserInput):
    graph = create_graph()
    result = graph.invoke({"operation": state["input"],"history":'{"history":[]}'})
    print("\n--- Execution Result ---")
    print(result["history"])
    return state

def create_main_graph():
    workflow = StateGraph(UserInput)

    workflow.add_node("get_operation", get_operation)
    workflow.add_node("process_operation", process_operation)

    workflow.set_entry_point("get_operation")
    
    workflow.add_edge("get_operation", "process_operation")
    workflow.add_edge("process_operation", END)

    return workflow.compile()

def main():
    conversation_graph = create_main_graph()
    conversation_graph.invoke({"input": "downtime.txt", "continue_conversation": True})


if __name__ == "__main__":
    main()