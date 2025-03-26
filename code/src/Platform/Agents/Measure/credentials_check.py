import random

def credentials_check(state):
    choose = random.randrange(20, 99, 3)

    if choose>=1:
        return {"health": "green", "score": choose}
    elif choose<=1:
        return {"health": "red", "score": choose}

