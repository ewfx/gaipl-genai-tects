from flask import Flask, jsonify,request
from langchain.tools import Tool
from langgraph.prebuilt import create_react_agent
import random
import time
from typing import Dict, Any
import os
import traceback
from langchain.chat_models import init_chat_model
from langsmith import traceable,Client
import langsmith as ls
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)
# Server Monitoring Agent
   
def check_availability() -> bool:
        """Simulate server availability check."""
        return random.random() < 0.9  # 90% chance of being available

    
def check_performance() -> float:
        """Simulate server performance check."""
        return random.uniform(0.5, 1.0)  # Random performance score
    
    
def check_latency() -> float:
        """Simulate server latency check."""
        return random.uniform(50, 500)  # Random latency in ms
    
def get_server_state() -> Dict[str, Any]:
        """Return the server state as a dictionary."""
        health= {
            "availability": check_availability(),
            "performance": check_performance(),
            "latency": check_latency(),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return str(health)

def get_analyze_logs() -> Dict[str, Any]:
        """Simulate log analysis."""
        errors = random.randint(0, 5)  # Random number of errors
        logs= {
            "errors_found": errors,
            "log_status": "Healthy" if errors == 0 else "Unhealthy"
        }
        return str(logs)

def get_database_health() -> Dict[str, Any]:
        """Simulate database health check."""
        db_health= {
            "status": "Healthy" if random.random() < 0.8 else "Unhealthy",  # 80% chance of being healthy
            "response_time": random.uniform(100, 1000)  # Random response time in ms
        }
        return str(db_health)


def get_thread_history(thread_id: str, project_name: str,langsmith_client): # Filter runs by the specific thread and project
        filter_string = f'and(in(metadata_key, ["session_id","conversation_id","thread_id"]), eq(metadata_value, "{thread_id}"))' # Only grab the LLM runs
        runs = [r for r in langsmith_client.list_runs(project_name=project_name, filter=filter_string, run_type="llm")]

        # Sort by start time to get the most recent interaction
        runs = sorted(runs, key=lambda run: run.start_time, reverse=True)
        if runs:
            print(runs[0])
            content1 = str(runs[0].inputs['messages'][0][0]["kwargs"]["content"])
            content2 = str(runs[0].outputs['generations'][0][0]['message']["kwargs"]["content"])
            combined_content = f"{content1} {content2}" 
            return combined_content
        else:
                return None
@traceable(name="LangGraph Agent")
def invoke_agent(agent,health_summary,langsmith_client):
            task=f"Here is the current system health data: {health_summary}. Can you summarize the health of the system?"
            run_tree = ls.get_current_run_tree()
            combined_content=get_thread_history(run_tree.extra["metadata"]["session_id"],run_tree.session_name,langsmith_client)
            messages=[]
            if combined_content:
                messages =  [combined_content]+ [("user", task)]
            else:
                messages =  [("user", task)]
            inputs = {"messages": messages}
            response = agent.invoke(inputs)
            return response["messages"][-1].content

def intialize_agent():
            
            model = init_chat_model("gpt-4", model_provider="openai")
            # Define tools
            monitor_server_tool=Tool(
                    name="monitor_server",
                    func=get_server_state,
                    description="Useful for checking the state of the server, including availability, performance, and latency."
                )
            
            analyze_logs_tool=Tool(
                    name="analyze_logs",
                    func=get_analyze_logs,
                    description="Useful for analyzing server logs to detect errors."
                )
            
            check_db_tool=Tool(
                    name="check_database_health",
                    func=get_database_health,
                    description="Useful for checking the health of the production database."
                )
            
            tools = [ monitor_server_tool,analyze_logs_tool,check_db_tool]

            # Create a React agent
            agent = create_react_agent(model, tools)
            health_summary = monitor_server_tool.func()+" "+analyze_logs_tool.func()+" "+check_db_tool.func()
            agent_details={"agent":agent,"health_summary":health_summary}
            return agent_details



@app.route("/production_support", methods=["GET"])
def production_support():
        try:    
            load_dotenv()
            
            langsmith_project = "project_with_data"
            session_id = "thread_agent"  # Unique thread identifier
            langsmith_extra = {"project_name": langsmith_project, "metadata": {"session_id": session_id}}
            langsmith_client = Client()
            
            agent_details=intialize_agent()
            agent_response=invoke_agent(agent_details["agent"],agent_details["health_summary"],langsmith_client,langsmith_extra=langsmith_extra)
            print(agent_response)
            return jsonify({
                "status": "success",
                "response": agent_response
            })
            
        except Exception as e:
            error_details = traceback.format_exc()
            print(f"Exception occurred: {error_details}")  # Log the error to the console

            print(f"Exception occurred: {error_details}")  # Log the error to the console

            # Return a meaningful error response
            return jsonify({
                    "status": "error",
                    "error": str(e),
                    "traceback": error_details
                }), 500 
# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
