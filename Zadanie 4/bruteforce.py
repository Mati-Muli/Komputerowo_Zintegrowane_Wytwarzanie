import itertools
from tasks import calculate_objective

def solve_brute_force(tasks):
    best_value = float('inf')
    best_seq = None
    for p in itertools.permutations(tasks):
        val = calculate_objective(p)
        if val < best_value:
            best_value = val
            best_seq = p
    return list(best_seq), best_value