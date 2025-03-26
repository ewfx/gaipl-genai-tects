import random
from Platform.Utilities.agent_response_management import get_history_object

def queue_load(state):
    choose = random.randrange(20, 99, 3)

    if choose<=60:
        output = {"health": "green", "score": choose}
    elif choose<=85:
        output = {"health": "yellow", "score": choose}
    elif choose>85:
        output = {"health": "red", "score": choose}
    
    new_history =  get_history_object({"history":state["history"]},
                                          {"agent":"queue_load","output":output})
    return {"history": new_history}


def queue_response_time(state):
    choose = random.randrange(50, 1000, 10)

    if choose<=100:
        output = {"health": "green", "score": choose}
    elif choose<=500:
        output = {"health": "yellow", "score": choose}
    elif choose>500:
        output = {"health": "red", "score": choose}
    
    new_history =  get_history_object({"history":state["history"]},
                                          {"agent":"queue_response_time","output":output})
    return {"history": new_history}
