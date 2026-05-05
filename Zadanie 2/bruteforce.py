from flowshop import calculate_cmax

def brute_force(p):
    n = len(p)
    best_perm = None
    best_cmax = float('inf')

    def dfs(partial, remaining):
        nonlocal best_perm, best_cmax

        if not remaining:
            cmax = calculate_cmax(p, partial)
            if cmax < best_cmax:
                best_cmax = cmax
                best_perm = partial[:]
            return

        for job in remaining:
            dfs(partial + [job], [j for j in remaining if j != job])

    dfs([], list(range(n)))
    return best_perm, best_cmax