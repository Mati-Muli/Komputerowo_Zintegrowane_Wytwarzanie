import copy
from schrage import schrage_heap, schrage_pmtn, calculate_cmax

best_u = float('inf')
best_pi = []


def carlier(tasks):
    global best_u, best_pi
    pi = schrage_heap(tasks)
    u = calculate_cmax(pi)

    if u < best_u:
        best_u = u
        best_pi = copy.deepcopy(pi)

    # Znalezienie parametrów bloku krytycznego
    b = -1
    t_moment = 0
    c_times = [0] * len(pi)
    for i, task in enumerate(pi):
        t_moment = max(t_moment, task.r) + task.p
        c_times[i] = t_moment

    for i in range(len(pi)):
        if c_times[i] + pi[i].q == u:
            b = i  # Ostatnie zadanie bloku

    a = -1
    for i in range(b + 1):
        p_sum = sum(t.p for t in pi[i:b + 1])
        if pi[i].r + p_sum + pi[b].q == u:
            a = i  # Pierwsze zadanie bloku
            break

    c = -1
    for i in range(a, b):
        if pi[i].q < pi[b].q:
            c = i  # Zadanie interferencyjne

    if c == -1:
        return best_pi

    k_block = pi[c + 1: b + 1]
    r_k = min(t.r for t in k_block)
    q_k = min(t.q for t in k_block)
    p_k = sum(t.p for t in k_block)

    tasks_left = copy.deepcopy(tasks)
    task_c_left = next(t for t in tasks_left if t.id == pi[c].id)
    old_r = task_c_left.r
    task_c_left.r = max(old_r, r_k + p_k)

    if schrage_pmtn(tasks_left) < best_u:
        carlier(tasks_left)
  
    tasks_right = copy.deepcopy(tasks)
    task_c_right = next(t for t in tasks_right if t.id == pi[c].id)

    old_q = task_c_right.q
    task_c_right.q = max(old_q, q_k + p_k)

    if schrage_pmtn(tasks_right) < best_u:
        carlier(tasks_right)

    return best_pi
