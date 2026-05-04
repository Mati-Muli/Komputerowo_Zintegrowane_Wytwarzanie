import time
from tasks import generate_instance, calculate_objective
from greedy import solve_greedy
from bruteforce import solve_brute_force
from dynamic import solve_dynamic
from plot import plot_gantt


def measure_time(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return result, (end - start) * 1000


def main():
    n = 10
    tasks = generate_instance(n, "A")  #

    print(f"Test dla n={n}\n")
    print(f"{'Algorytm':<20} | {'Koszt':<10} | {'Czas [ms]':<10}")
    print("-" * 50)

    g_seq, g_time = measure_time(solve_greedy, tasks)
    g_val = calculate_objective(g_seq)
    print(f"{'Greedy (EDD)':<20} | {g_val:<12} | {g_time:<10.4f}")
    plot_gantt(g_seq, title=f"Algorytm Zachłanny (EDD) | F = {g_val}")

    (dp_seq, dp_val), dp_time = measure_time(solve_dynamic, tasks)
    print(f"{'Dynamic Prog':<20} | {dp_val:<12} | {dp_time:<10.4f}")
    plot_gantt(dp_seq, title=f"Programowanie Dynamiczne | F = {dp_val}")

    if n <= 10:
        (bf_seq, bf_val), bf_time = measure_time(solve_brute_force, tasks)
        print(f"{'Brute Force':<20} | {bf_val:<12} | {bf_time:<10.4f}")
        plot_gantt(bf_seq, title=f"Przegląd Zupełny (Brute Force) | F = {bf_val}")
    else:
        print(f"{'Brute Force':<20} | {'Pominięto (n zbyt duże)':<22}")

    print("\nGenerowanie wykresu Gantta dla rozwiązania optymalnego...")
    plot_gantt(dp_seq, title=f"Harmonogram Optymalny (DP) - n={n}, F={dp_val}")


if __name__ == "__main__":
    main()