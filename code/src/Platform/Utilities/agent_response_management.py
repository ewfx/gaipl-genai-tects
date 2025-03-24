import json

def get_history_object(state,new_history):
    history_so_far = state['history']

    if history_so_far == '':
        history_so_far = '{"history":[]}'
    
    json_history = json.loads(history_so_far)

    json_history['history'].append(new_history)

    json_string = json.dumps(json_history)
      
    return json_string