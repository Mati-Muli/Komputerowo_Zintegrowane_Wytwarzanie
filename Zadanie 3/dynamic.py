def solve_dynamic(tasks):
    n = len(tasks)
    num_states = 1 << n
    memory = [float('inf')] * num_states
    parent = [-1] * num_states
    memory[0] = 0

    times_sum = [0] * num_states
    for mask in range(num_states):
        for j in range(n):
            if (mask >> j) & 1:
                times_sum[mask] += tasks[j].p

    for mask in range(1, num_states):
        for j in range(n):
            if (mask >> j) & 1:
                prev_mask = mask ^ (1 << j)
                cost = max(0, times_sum[mask] - tasks[j].d) * tasks[j].w
                if memory[prev_mask] + cost < memory[mask]:
                    memory[mask] = memory[prev_mask] + cost
                    parent[mask] = j

    sequence = []
    curr_mask = num_states - 1
    while curr_mask > 0:
        idx = parent[curr_mask]
        sequence.append(tasks[idx])
        curr_mask ^= (1 << idx)

    return sequence[::-1], memory[num_states - 1]