import random
from task import Task

def generate_tasks(n, seed, use_large_q=False):
    rng = random.Random(seed)

    p_times = [rng.randint(1, 29) for _ in range(n)]
    sum_p = sum(p_times)

    x_limit = sum_p if use_large_q else 29

    tasks = []
    for i in range(n):
        r_j = rng.randint(1, sum_p)

        q_j = rng.randint(1, x_limit)
        tasks.append(Task(i + 1, r_j, p_times[i], q_j))

    return tasks
