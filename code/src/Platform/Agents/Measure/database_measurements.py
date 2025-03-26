import random
from Platform.Utilities.agent_response_management import get_history_object

def database_ping(state):
    choose = random.randrange(20, 99, 3)

    if choose<50:
        output = {"database ping": "Success"}
    else:
        output = {"database ping": "Failed"}

    new_history =  get_history_object({"history":state["history"]},
                                          {"agent":"database_ping","output":output})
    return {"history": new_history}

def database_connections(state):
  
    choose = random.randrange(20, 99, 3)

    if choose<=60:
        output = {"health": "green", "no_of_connections": choose}
    elif choose<=85:
        output = {"health": "yellow", "no_of_connections": choose}
    elif choose>85:
        output = {"health": "red", "no_of_connections": choose}

    new_history =  get_history_object({"history":state["history"]},
                                          {"agent":"database_connections","output":output})
    return {"history": new_history}