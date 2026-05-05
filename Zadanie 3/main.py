import time
from tasks import generate_instance, calculate_objective
from greedy import solve_greedy
from bruteforce import solve_brute_force
from dynamic import solve_dynamic
from plot import plot_gantt
import matplotlib.pyplot as plt

def measure_time(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return result, (end - start) * 1000


def main():
    n = 10
    tasks = generate_instance(n, "A")  

    print(f"Test dla n={n}\n")
    print(f"{'Algorytm':<20} | {'Koszt':<10} | {'Czas [ms]':<10}")
    print("-" * 50)

    # ===== LICZENIE (z zabezpieczeniem) =====
    g_seq = dp_seq = bf_seq = None
    g_val = dp_val = bf_val = None
    g_time = dp_time = bf_time = None

    try:
        g_seq, g_time = measure_time(solve_greedy, tasks)
        g_val = calculate_objective(g_seq)
        print(f"{'Greedy (EDD)':<20} | {g_val:<12} | {g_time:<10.4f}")
    except Exception as e:
        print(f"Greedy ERROR: {e}")

    try:
        (dp_seq, dp_val), dp_time = measure_time(solve_dynamic, tasks)
        print(f"{'Dynamic Prog':<20} | {dp_val:<12} | {dp_time:<10.4f}")
    except Exception as e:
        print(f"Dynamic ERROR: {e}")

    if n <= 10:
        try:
            (bf_seq, bf_val), bf_time = measure_time(solve_brute_force, tasks)
            print(f"{'Brute Force':<20} | {bf_val:<12} | {bf_time:<10.4f}")
        except Exception as e:
            print(f"Brute Force ERROR: {e}")
    else:
        print(f"{'Brute Force':<20} | {'Pominięto (n zbyt duże)':<22}")

    # ===== RYSOWANIE =====
    fig, axs = plt.subplots(3, 1, figsize=(12, 10))

    # Greedy
    if g_seq:
        plot_gantt(g_seq, axs[0], title=f"Greedy | F = {g_val}")
    else:
        axs[0].set_title("Greedy - brak")

    # Dynamic
    if dp_seq:
        plot_gantt(dp_seq, axs[1], title=f"Dynamic | F = {dp_val}")
    else:
        axs[1].set_title("Dynamic - brak")

    # Brute Force
    if bf_seq:
        plot_gantt(bf_seq, axs[2], title=f"Brute Force | F = {bf_val}")
    else:
        axs[2].set_title("Brute Force - brak")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
