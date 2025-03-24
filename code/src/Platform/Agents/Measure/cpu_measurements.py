import random

def cpu_utlization(state):
    choose = random.randrange(20, 99, 3)

    if choose<=60:
        return {"health": "green", "score": choose}
    elif choose<=85:
        return {"health": "yellow", "score": choose}
    elif choose>85:
        return {"health": "red", "score": choose}


def cpu_ready_time(state):
    choose = random.randrange(50, 1000, 10)

    if choose<=100:
        return {"health": "green", "score": choose}
    elif choose<=500:
        return {"health": "yellow", "score": choose}
    elif choose>500:
        return {"health": "red", "score": choose}

