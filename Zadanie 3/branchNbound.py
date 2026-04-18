from flowshop import calculate_cmax
from johnson import johnson_3machines

def lower_bound(p, partial, remaining):
    from flowshop import calculate_cmax

    if not partial:
        current = 0
    else:
        current = calculate_cmax(p, partial)

    min_sum = 0
    for job in remaining:
        min_sum += min(p[job])

    return current + min_sum

def branch_and_bound(p):
    n = len(p)

    # górne ograniczenie z Johnsona
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
            return  # obcięcie

        for job in remaining:
            dfs(partial + [job], [j for j in remaining if j != job])

    dfs([], list(range(n)))
    return best_perm, UB