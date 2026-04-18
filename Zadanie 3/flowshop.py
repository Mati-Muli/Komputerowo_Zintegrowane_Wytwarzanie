def calculate_cmax(p, permutation):
    n = len(permutation)
    m = len(p[0])

    C = [[0] * m for _ in range(n)]

    for i in range(n):
        job = permutation[i]
        for j in range(m):
            if i == 0 and j == 0:
                C[i][j] = p[job][j]
            elif i == 0:
                C[i][j] = C[i][j-1] + p[job][j]
            elif j == 0:
                C[i][j] = C[i-1][j] + p[job][j]
            else:
                C[i][j] = max(C[i-1][j], C[i][j-1]) + p[job][j]

    return C[-1][-1]

def schedule(p, permutation):
    n = len(permutation)
    m = len(p[0])

    S = [[0]*m for _ in range(n)]
    C = [[0]*m for _ in range(n)]

    for i in range(n):
        job = permutation[i]
        for j in range(m):
            if i == 0 and j == 0:
                S[i][j] = 0
            elif i == 0:
                S[i][j] = C[i][j-1]
            elif j == 0:
                S[i][j] = C[i-1][j]
            else:
                S[i][j] = max(C[i-1][j], C[i][j-1])

            C[i][j] = S[i][j] + p[job][j]

    return S, C