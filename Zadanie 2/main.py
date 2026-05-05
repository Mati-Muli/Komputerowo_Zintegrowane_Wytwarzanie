from generator import generate_instance
from johnson import johnson_3machines
from bruteforce import brute_force
from branchNbound import branch_and_bound
from utils import print_instance, print_schedule, gantt_chart, measure_time
from flowshop import calculate_cmax

# parametry
n, m = 5, 3

p = generate_instance(n, m)

print_instance(p)

# Johnson
perm_j = johnson_3machines(p)
print_schedule(p, perm_j)

# BF
perm_bf, cmax_bf = brute_force(p)
print_schedule(p, perm_bf)

# BnB
perm_bnb, cmax_bnb = branch_and_bound(p)
print_schedule(p, perm_bnb)

print("\n=== PORÓWNANIE METOD ===")

# Johnson
(perm_j), time_j = measure_time(johnson_3machines, p)
cmax_j = calculate_cmax(p, perm_j)

# BF
(perm_bf, cmax_bf), time_bf = measure_time(brute_force, p)

# BnB
(perm_bnb, cmax_bnb), time_bnb = measure_time(branch_and_bound, p)

# wyniki
print("\nMetoda        Cmax     Czas [s]")
print("----------------------------------")
print(f"Johnson      {cmax_j:<8} {time_j:.6f}")
print(f"Brute Force  {cmax_bf:<8} {time_bf:.6f}")
print(f"BnB          {cmax_bnb:<8} {time_bnb:.6f}")

# wykres gantta dla najlepszej permutacji
gantt_chart(p, perm_j)
gantt_chart(p, perm_bnb)
gantt_chart(p, perm_bf)
