import copy
import sys
import carlier as car_mod
from generator import generate_tasks
from schrage import schrage, schrage_heap, schrage_pmtn, calculate_cmax
from wykresy import plot_gantt



def print_result(label, pi):
    if isinstance(pi, list):
        ids = [t.id for t in pi]
        cmax = calculate_cmax(pi)
        print(f"{label:20} | Cmax: {cmax:4} | Kolejność: {ids}")
    else:
        print(f"{label:20} | Cmax: {pi:4} | (Wartość optymalna z przerwaniami)")


if __name__ == "__main__":
    # --- KONFIGURACJA ---
    N_TASKS = 10
    SEED = 2026

    print("=" * 70)
    print(f"   Parametry: n={N_TASKS}, seed={SEED}")
    print("=" * 70 + "\n")

    # Instrukcja wymaga przetestowania dwóch wariantów zakresu q_j (X=29 i X=A)
    datasets = [
        ("ZESTAW: MAŁE q (X=29)", generate_tasks(N_TASKS, SEED, use_large_q=False)),
        ("ZESTAW: DUŻE q (X=A)", generate_tasks(N_TASKS, SEED, use_large_q=True))
    ]

    for label, tasks in datasets:
        print(f">>> {label}")

        t1 = copy.deepcopy(tasks)
        pi_sch = schrage(t1)
        print_result("Schrage Basic", pi_sch)

        t2 = copy.deepcopy(tasks)
        pi_heap = schrage_heap(t2)
        print_result("Schrage Heap", pi_heap)

        t3 = copy.deepcopy(tasks)
        cmax_pmtn = schrage_pmtn(t3)
        print_result("Schrage PMTN", cmax_pmtn)

        car_mod.best_u = float('inf')
        car_mod.best_pi = []
        t4 = copy.deepcopy(tasks)
        pi_car = car_mod.carlier(t4)
        print_result("Carlier (Optimum)", pi_car)

        print(f"\nGenerowanie wykresu dla {label}...")
        plot_gantt(pi_car, title=f"Optymalny Harmonogram Carlier ({label})")
        print("-" * 70 + "\n")

    print("Wszystkie testy zakończone pomyślnie.")