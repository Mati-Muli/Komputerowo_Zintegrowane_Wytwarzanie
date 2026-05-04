def solve_greedy(tasks):
    return sorted(tasks, key=lambda x: x.d)