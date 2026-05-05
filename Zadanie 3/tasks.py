import random

class Task:
    def __init__(self, id, p, w, d):
        self.id = id
        self.p = p
        self.w = w
        self.d = d

    def __repr__(self):
        return f"T{self.id}"

def generate_instance(n, X_type="A"):
    random.seed()
    tasks_data = []
    sum_p = 0
    for i in range(1, n + 1):
        p = random.randint(1, 29)
        w = random.randint(1, 9)
        tasks_data.append({'id': i, 'p': p, 'w': w})
        sum_p += p
    X = sum_p if X_type == "A" else 29
    return [Task(d['id'], d['p'], d['w'], random.randint(1, X)) for d in tasks_data]

def calculate_objective(sequence):
    twt = 0
    current_time = 0
    for task in sequence:
        current_time += task.p
        tardiness = max(0, current_time - task.d)
        twt += task.w * tardiness
    return twt