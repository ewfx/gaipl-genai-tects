from langgraph.graph import StateGraph, END
from typing import Annotated, TypedDict
from Platform.Agents.Measure.database_measurements import database_connections, database_ping
from Platform.Agents.Measure.queue_measurements import queue_load, queue_response_time
from Platform.Agents.Measure.log_measurements import error_count, frequent_error
from Platform.Agents.Measure.credentials_check import credentials_check
from Platform.Agents.Decision.decisions import execute_agent, execute_operation

class AgentState(TypedDict):
    input: str
    output: str
    operation: str
    action: str
    decision: str
    history: str


def create_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("execute_operation", execute_operation)
    workflow.add_node("execute_agent", execute_agent)
    workflow.add_node("database_ping", database_ping)
    workflow.add_node("database_connections", database_connections)
    workflow.add_node("error_count", error_count)
    workflow.add_node("frequent_error", frequent_error)
    workflow.add_node("queue_response_time", queue_response_time)
    workflow.add_node("queue_load", queue_load)
    workflow.add_node("credentials_check", credentials_check)

    workflow.add_conditional_edges(
        "execute_operation",
        lambda x: x["action"],
        {
            "execute_agent": "execute_agent",
            "completed": END,
        }
    )

    workflow.add_conditional_edges(
        "execute_agent",
        lambda x: x["action"],
        {
            "database_ping": "database_ping",
            "database_connections": "database_connections",
            "error_count": "error_count",
            "frequent_error": "frequent_error",
            "queue_response_time": "queue_response_time",
            "queue_load": "queue_load",
            "credentials_check": "credentials_check"
        }
    )

    workflow.set_entry_point("execute_operation")
    workflow.add_edge("database_ping", "execute_operation")
    workflow.add_edge("database_connections", "execute_operation")
    workflow.add_edge("error_count", "execute_operation")
    workflow.add_edge("frequent_error", "execute_operation")
    workflow.add_edge("queue_response_time", "execute_operation")
    workflow.add_edge("queue_load", "execute_operation")
    workflow.add_edge("credentials_check", "execute_operation")

    workflow.add_edge("execute_operation", END)

    return workflow.compile()