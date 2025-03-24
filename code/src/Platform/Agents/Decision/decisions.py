from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from Utilities.agent_response_management import get_history_object
import json
import os

def execute_operation(state):
    action = state['operation']
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = PromptTemplate.from_template("""
    You are an agent that executes a given opertion step by step, 
    the operation description is passed to you, the already completed steps is passed as state
 
    Operation : {operation}
                                          
    State : {history}

    Analyse the operation and state. Indicate in a short scentence which action to to be taken next, 
    if operation is completed give a single word 'completed'".

    """)
    chain = prompt | llm
    response = chain.invoke({"operation":action,"history": state["history"]})
    decision = response.content.strip().lower()
    new_history =  get_history_object({"history":state["history"]},{"agent":"execute_operation","output":decision})

    if 'completed' in decision:
        return {"history": new_history,"action":"completed"}
    else:
        return {"history": new_history,"action":"execute_agent", "input":decision}

def execute_agent(state):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    next_action = state["input"]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.dirname(script_dir)
    file_path = os.path.join(parent,"agents.json")

    # Open and read the JSON file
    with open(file_path, 'r') as file:
        agents = json.load(file)

    prompt = PromptTemplate.from_template("""
    You are an agent that identifies the which is the agent that has to be called to full fill the action requested, 
    the list of agents and discription are provided in the agents property
 
    action: {action}                                     
    agents : {agents}
   
    Analyse and output a single word which is the name of the agent to be called, no other text should be included".

    """)
    chain = prompt | llm
    response = chain.invoke({"action":next_action, "agents":agents})
    agent_to_call = response.content.strip().lower()

    new_history =  get_history_object({"history":state["history"]},{"agent":"execute_agent","output":agent_to_call})
    return {"history": new_history,"action":agent_to_call}
