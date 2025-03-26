import random
from Platform.Utilities.agent_response_management import get_history_object

def error_count(state):

    #application_name = state['app_name']

    choose = random.randrange(20, 99, 3)
        
    if choose<=30:
        output = {"health": "green", "score": choose}    
    elif choose<=40:
        output =  {"health": "yellow", "score": choose}
    elif choose>40:
        output =  {"health": "red", "score": choose}
    
    new_history =  get_history_object({"history":state["history"]},
                                          {"agent":"error_count","output":output})
    return {"history": new_history}
    

def frequent_error(state):

    #application_name = state['app_name']

    choose = random.randrange(20, 99, 3)
    
    output = {"error": "Unable to connect to the database", "count": choose}

    new_history =  get_history_object({"history":state["history"]},
                                          {"agent":"frequent_error","output":output})
    return {"history": new_history}    