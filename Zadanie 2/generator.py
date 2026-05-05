import random

def generate_instance(n, m):
    random.seed()
    p = [[random.randint(1, 29) for _ in range(m)] for _ in range(n)]
    return p