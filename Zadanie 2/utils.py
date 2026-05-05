import matplotlib.pyplot as plt
import time

def measure_time(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return result, end - start

def print_instance(p):
    print("=== INSTANCJA ===")
    for j, row in enumerate(p):
        print(f"Zadanie {j}: {row}")

def print_schedule(p, perm):
    from flowshop import schedule

    S, C = schedule(p, perm)

    print("\n=== HARMONOGRAM ===")
    print("Permutacja:", " -> ".join(f"J{j}" for j in perm))
    print("Cmax:", C[-1][-1])

    print("\nMacierz S (starty):")
    for row in S:
        print(row)

    print("\nMacierz C (zakończenia):")
    for row in C:
        print(row)

def gantt_chart(p, perm):
    from flowshop import schedule

    S, C = schedule(p, perm)
    m = len(p[0])

    fig, ax = plt.subplots()

    for i, job in enumerate(perm):
        for machine in range(m):
            start = S[i][machine]
            duration = p[job][machine]

            ax.barh(
                y=machine,
                width=duration,
                left=start
            )

            ax.text(
                start + duration/2,
                machine,
                f"J{job}",
                va='center',
                ha='center'
            )

    ax.set_yticks(range(m))
    ax.set_yticklabels([f"M{i}" for i in range(m)])
    ax.set_xlabel("Czas")
    ax.set_title("Wykres Gantta")

    plt.show()