import heapq
import copy

def calculate_cmax(permutation):
    t = 0
    c_max = 0
    for task in permutation:
        t = max(t, task.r) + task.p
        c_max = max(c_max, t + task.q)
    return c_max

def schrage(tasks):
    n_set = list(tasks)
    g_set = []
    pi = []
    t = min(task.r for task in n_set) if n_set else 0
    while g_set or n_set:
        while n_set and min(n_set).r <= t:
            j_star = min(n_set)
            g_set.append(j_star)
            n_set.remove(j_star)
        if g_set:
            j_star = max(g_set, key=lambda x: x.q)
            g_set.remove(j_star)
            pi.append(j_star)
            t += j_star.p
        else:
            t = min(n_set).r
    return pi

def schrage_heap(tasks):
    n_set = list(tasks)
    heapq.heapify(n_set)
    g_set = []
    pi = []
    t = n_set[0].r if n_set else 0
    while g_set or n_set:
        while n_set and n_set[0].r <= t:
            task = heapq.heappop(n_set)
            heapq.heappush(g_set, (-task.q, task)) # Max-heap po q
        if g_set:
            _, j_star = heapq.heappop(g_set)
            pi.append(j_star)
            t += j_star.p
        else:
            t = n_set[0].r
    return pi

def schrage_pmtn(tasks):
    """Dolne ograniczenie dla Carliera"""
    n_set = list(copy.deepcopy(tasks))
    heapq.heapify(n_set)
    g_set = []
    t, c_max = 0, 0
    current_task = None
    while g_set or n_set:
        while n_set and n_set[0].r <= t:
            j_star = heapq.heappop(n_set)
            heapq.heappush(g_set, (-j_star.q, j_star))
            if current_task and j_star.q > current_task.q:
                current_task.p = t - j_star.r
                t = j_star.r
                if current_task.p > 0:
                    heapq.heappush(g_set, (-current_task.q, current_task))
                current_task = None
        if g_set:
            _, j_star = heapq.heappop(g_set)
            current_task = j_star
            t += j_star.p
            c_max = max(c_max, t + j_star.q)
        else:
            t = n_set[0].r
    return c_max