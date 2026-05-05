from flowshop import calculate_cmax
from johnson import johnson_3machines

# ograniczenie dolne LB3

def get_machine_times(p, partial):
    if not partial:
        return [0] * len(p[0])

    m = len(p[0])
    times = [0] * m
    for job in partial:
        times[0] += p[job][0]
        for i in range(1, m):
            times[i] = max(times[i - 1], times[i]) + p[job][i]
    return times


def lower_bound(p, partial, remaining):
    m = len(p[0])
    completion_times = get_machine_times(p, partial)
    lb_values = []
    for i in range(m):
        c_i_x = completion_times[i]
        sum_p_ij = sum(p[job][i] for job in remaining)
        sum_min_pkj = 0
        for k in range(i + 1, m):
            sum_min_pkj += min(p[job][k] for job in remaining)
        lb_values.append(c_i_x + sum_p_ij + sum_min_pkj)

    return max(lb_values)


def branch_and_bound(p):
    n = len(p)
    init_perm = johnson_3machines(p)
    UB = calculate_cmax(p, init_perm)
    best_perm = init_perm

    def dfs(partial, remaining):
        nonlocal UB, best_perm
        if not remaining:
            cmax = calculate_cmax(p, partial)
            if cmax < UB:
                UB = cmax
                best_perm = partial[:]
            return

        lb = lower_bound(p, partial, remaining)

        if lb >= UB:
            return

        for job in remaining:
            new_remaining = [j for j in remaining if j != job]
            dfs(partial + [job], new_remaining)

    dfs([], list(range(n)))
    return best_perm, UB