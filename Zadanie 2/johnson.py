def johnson_3machines(p):
    n = len(p)

    virtual = []
    for j in range(n):
        p1 = p[j][0] + p[j][1]
        p2 = p[j][1] + p[j][2]
        virtual.append((j, p1, p2))

    left = []
    right = []

    jobs = virtual.copy()

    while jobs:
        min_job = min(jobs, key=lambda x: min(x[1], x[2]))

        if min_job[1] < min_job[2]:
            left.append(min_job[0])
        else:
            right.insert(0, min_job[0])

        jobs.remove(min_job)

    return left + right