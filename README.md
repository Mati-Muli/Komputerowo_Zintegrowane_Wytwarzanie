# Komputerowo zintegrowane wytwarzanie

# Zadanie 2 - RPQ
<details>
<summary> Opis zadania </summary>

## Badany problem:
Problem *1|ri, qi|Cmax* należy do klasy problemów szeregowania zadań na jednej maszynie.

Dla każdego zadania *j* określone są:
- *rj* -czas gotowości (release time),
- *pj* - czas przetwarzania,
- *qj* – czas dostarczenia (delivery time).

Celem jest takie uszeregowanie zadań, aby zminimalizować wartość:
<img width="581" height="111" alt="image" src="https://github.com/user-attachments/assets/1e4c2a42-77f7-4b1e-8db7-9c3952190724" />

gdzie *Cj* to moment zakończenia przetwarzania zadania *j*.
## Sposób generowania instancji:

Instancje problemu generowane są losowo na podstawie liczby zadań *n* oraz ziarna generatora *Z*.

Proces generowania:
1. Inicjalizacja generatora liczb pseudolosowych:

Dla każdego zadania losowany jest czas przetwarzania z przedziału ⟨1, 29⟩:
```
rng = random.Random(seed)
```
2. Generowanie czasów przetwarzania *pj*:
```
p_times = [rng.randint(1, 29) for _ in range(n)]
```
3. Obliczenie sumy czasów przetwarzania:
```
sum_p = sum(p_times)
```
4. Ustalenie zakresu dla *qj*
```
x_limit = sum_p if use_large_q else 29
```
W eksperymentach rozpatrywane są dwa warianty:
- X = 29 (mały zakres wartości *qj*)
- X = A (duży zakres wartości *qj*)

Pozwala to zbadać wpływ rozkładu parametrów *qj* na działanie algorytmów.

## Metody rozwiązania:
### __Algorytm Schrage__ 

jest algorytmem zachłannym stosowanym do wyznaczania przybliżonego rozwiązania problemu *1|ri, qi|Cmax*.

__Główna idea działania:__
1. Ustawia czas początkowy *t=min(rj)*
2. Dzieli zadania na dwa zbiory - zadania jeszcze niedostępne (*rj>t*) oraz zadania dostępne (*rj<=t*)
3. Dopóki istnieją zadania do wykonania wszystkie zadania spełniające warunek *rj<=t* zostają przeniesione ze zbioru N do zbioru G
4. Jeśli zbiór G nie jest pusty program wybiera zadanie o największym *qj*, dodaje je do permutacji i aktualizuje czas.
5. Proces powtarzany jest do momentu, aż wszystkie zadania zostaną uszeregowane.

__Obliczanie wartości funkcji celu__

Dla wygenerowanej permutacji zadań wartość *Cmax* obliczana jest w następujący sposób:
```
def calculate_cmax(permutation):
    t = 0
    c_max = 0
    for task in permutation:
        t = max(t, task.r) + task.p
        c_max = max(c_max, t + task.q)
    return c_max
```

__1. Podstawowa wersja algorytmu Schrage__

Algorytm wykorzystuje dwa zbiory:
- N – zadania niegotowe (jeszcze niedostępne)
- G – zadania gotowe do wykonania
```
def schrage(tasks):
    n_set = list(tasks)
    g_set = []
    pi = []
    t = min(task.r for task in n_set) if n_set else 0
```
Główna pętla algorytmu:
```
while g_set or n_set:
  while n_set and min(n_set).r <= t:
    j_star = min(n_set)
    g_set.append(j_star)
    n_set.remove(j_star)
```
Dodawanie dostępnych zadań do zbioru gotowych:
```
if g_set:
    j_star = max(g_set, key=lambda x: x.q)
    g_set.remove(j_star)
    pi.append(j_star)
    t += j_star.p
```
Wybór zadania o największym *qj*:
```
    else:
        t = min(n_set).r
    return pi
```
__2. Wersja zoptymalizowana z zastosowaniem struktury kopca.__

```
def schrage_heap(tasks):
    n_set = list(tasks)
    heapq.heapify(n_set)
    g_set = []
    pi = []
    t = n_set[0].r if n_set else 0
```

Zamiast przeszukiwać listy:
- zbiór zadań niegotowych (N) przechowywany jest jako min-kopiec według *rj*
- zbiór zadań gotowych (G) jako max-kopiec według *qj*

Dzięki temu:
- najszybciej dostępne zadanie (najmniejsze *rj*) można pobrać w czasie *O(log n)*​
- wybór zadania o największym *qj* również zajmuje *O(log n)*

Algorytm działa analogicznie do podstawowej wersji, jednak operacje wyboru i przenoszenia zadań są znacznie bardziej efektywne.

__3. Schrage z preempcją (PMTN)__

Wersja z przerwaniami (preemption) wykorzystywana jest do wyznaczania dolnego ograniczenia w algorytmie Carliera, różni się tym, że aktualnie wykonywane zadanie może zostać przerwane.
```
def schrage_pmtn(tasks):
    """Dolne ograniczenie dla Carliera"""
    n_set = list(copy.deepcopy(tasks))
    heapq.heapify(n_set)
    g_set = []
    t, c_max = 0, 0
    current_task = None
```
Mechanizm działania:
- gdy pojawi się nowe zadanie o większym *qj*, aktualne zadanie zostaje przerwane
- jego pozostały czas przetwarzania trafia ponownie do zbioru zadań gotowych
- wykonywane jest zadanie o największym *qj*

Wersja ta nie tworzy permutacji zadań, a jedynie wyznacza wartość *Cmax*, stanowiąc dolne ograniczenie w algorytmie Carliera.

### __Algorytm Carlier__
Algorytm Carliera jest algorytmem dokładnym rozwiązującym problem *1|ri, qi|Cmax* z wykorzystaniem techniki branch and bound.

__Wykorzystuje on:__
- algorytm Schrage – do wyznaczania rozwiązania (górne ograniczenie),
- Schrage z preempcją (PMTN) – do wyznaczania dolnego ograniczenia

__Główna idea działania:__
1. Wyznacza rozwiązanie przybliżone (Schrage)
2. Identyfikuje tzw. blok krytyczny
3. Wybiera zadanie zakłócające (interferencyjne)
4. Tworzy dwa podproblemy (branching)
5. Odcina gałęzie, które nie mogą poprawić rozwiązania (bounding)

__Na bazie kodu:__
1. Wyznaczanie rozwiązania początkowego
```
pi = schrage_heap(tasks)
u = calculate_cmax(pi)

if u < best_u:
    best_u = u
    best_pi = copy.deepcopy(pi)
```
gdzie *u* to aktualne górne ograniczenie, natomiast best_u – najlepsze znalezione rozwiązanie

2. Wyznaczanie bloku krytycznego
```
t_moment = 0
c_times = [0] * len(pi)
for i, task in enumerate(pi):
    t_moment = max(t_moment, task.r) + task.p
    c_times[i] = t_moment
```
Blok krytyczny to ciąg kolejnych zadań, którego modyfikacja może prowadzić do poprawy rozwiązania.

3. Wyznaczenie zadania interferencyjnego
```
for i in range(a, b):
    if pi[i].q < pi[b].q:
        c = i
```

4. Podział na gałęzie
Gałąź lewa – modyfikacja *rc*:
```
task_c_left.r = max(old_r, r_k + p_k)
```
Gałąź prawa - modyfikacja *qc*:
```
task_c_right.q = max(old_q, q_k + p_k)
```

5. Odcinanie gałęzi (bounding)
```
if schrage_pmtn(tasks_left) < best_u:
    carlier(tasks_left)
```

## Wnioski:
Algorytm Schrage pozwala na szybkie wyznaczenie dobrego rozwiązania przybliżonego,
natomiast algorytm Carliera umożliwia znalezienie rozwiązania optymalnego kosztem
większej złożoności obliczeniowej.
</details>

# Zadanie 3
<details>
<summary> Opis zadania </summary>
    
## Badany problem:
Problem *F P||Cmax* jest klasyczny problem szeregowania typu flow shop, gdzie na każdej maszynie kolejność wykonywanych zadań jest inna.

Dla badanego problemu, mamy zbiór *n* zadań:

*J={1,2,...,n}*

zbiór maszyn:

*M={1,2,...,m}*

Każde zadanie j składa się z ciągu operacji:

*Oj​=(o1j​,o2j​,...,omj​)*

gdzie:
- *oij​* -operacja zadania j na maszynie i,
- *pij* - czas trwania operacji.

### Ograniczenia
1. Na każdej maszynie w danym momencie może być wykonywana tylko jedna operacja
2. Operacje zadania muszą być wykonywane w ustalonej kolejności (technologicznej)

### Cel
Celem jest minimalizacja czasu zakończenia wszystkich zadań Cmax:
<img width="440" height="112" alt="image" src="https://github.com/user-attachments/assets/b429dadc-0ee5-4e24-9d7e-be123c455dbd" />

## Sposób generowania instancji:
Instancje generowane są losowo na podstawie parametrów:
- liczba zadań *n*
- liczba maszyn *m*
- ziarno generatora *Z*

1. Inicjalizacja generatora liczb pseudolosowych:
```
init(Z)
```
2. Dla każdego zadania *j∈J*:
- dla każdej maszyny *i∈M*:
<img width="272" height="44" alt="image" src="https://github.com/user-attachments/assets/577a069d-d9f3-41fe-b7e8-505c312e33dd" />

Instancja jest zapisana jako macierz:
```
p[j][i]
```
gdzie j - indeks zadania, i - indeks maszyny

## Metody rozwiązania:

### Algorytm Johnsona
Algorytm Johnsona polega na kolejnym znajdywaniu operacji o najkrótszym czasie wykonywania na pierwszej lub drugiej
Maszynie, należy więc on do metod dedykowanych dla problemu *F P2||Cmax*. 

W ramach badanego problemu algorytm został rozszerzony o dodatkową 'środkową' maszynę wirtualną, dzięki czemu możliwe jest operowanie na 3 maszynach..
```
virtual = []
for j in range(n):
    p1 = p[j][0] + p[j][1]
    p2 = p[j][1] + p[j][2]
    virtual.append((j, p1, p2))
```
gdzie p1 oraz p2 wyznaczają czas wykonania na wirtualnych maszynach.

__Główna idea działania:__

```
jobs = virtual.copy()

while jobs:
    min_job = min(jobs, key=lambda x: min(x[1], x[2]))

    if min_job[1] < min_job[2]: #1.
        left.append(min_job[0])
    else:
        right.insert(0, min_job[0]) #2.

    jobs.remove(min_job) #3.

return left + right
```

1. Dla każdego zadania oblicz czasy na maszynach wirtualnych
2. Wybierz zadanie z najmniejszym czasem:
    - jeśli minimum jest na M1' → dodaj na początek
    - jeśli na M2' → dodaj na koniec
3. Usuń zadanie i powtarzaj

### Metoda siłowa (Brute Force)
Metoda siłowa to technika rozwiązywania problemów polegająca na bezpośrednim sprawdzeniu wszystkich możliwych kombinacji lub rozwiązań, aż do znalezienia właściwego.

Sprawdzane są wszystkie możliwe permutacje zadań *n!*

gdzie dla każdej permutacji:
- obliczany jest *Cmax*,
- wybierane jest najlepsze rozwiązanie.
	​
### Metoda podziału i ograniczeń (Branch and Bound)

*Metoda Branch and Bound (BnB)* polega na przeszukiwaniu przestrzeni wszystkich permutacji zadań w postaci drzewa, z jednoczesnym odrzucaniem tych gałęzi, które nie mogą prowadzić do rozwiązania lepszego od aktualnie najlepszego.

Każdy węzeł drzewa odpowiada:
- częściowej permutacji zadań (partial)
- zbiorowi pozostałych zadań (remaining)

__Górne ograniczenie (Upper Bound, UB)__

Jako początkowe rozwiązanie przyjmowane jest rozwiązanie heurystyczne uzyskane za pomocą algorytmu Johnsona:
```
init_perm = johnson_3machines(p)
UB = calculate_cmax(p, init_perm)
```
__Dolne ograniczenie (Lower Bound, LB)__

Dolne ograniczenie szacuje najlepszy możliwy czas zakończenia dla danej częściowej permutacji.

Najpierw obliczane są czasy zakończenia operacji dla aktualnej częściowej permutacji:
```
def get_machine_times(p, partial):
    if not partial:
        return [0] * len(p[0])

    m = len(p[0])
    times = [0] * m
    for job in partial:
        times[0] += p[job][0]
        for i in range(1, m):
            times[i] = max(times[i - 1], times[i]) + p[job][i]
    return times
```
Następnie dla każdej maszyny wyznaczane jest ograniczenie:
<img width="1045" height="174" alt="image" src="https://github.com/user-attachments/assets/f317fcc8-161e-4e97-b3ea-c554450ef687" />


__Implementacja:__
```
def lower_bound(p, partial, remaining):
    m = len(p[0])
    completion_times = get_machine_times(p, partial)
    lb_values = []

    for i in range(m):
        c_i_x = completion_times[i]
        sum_p_ij = sum(p[job][i] for job in remaining)

        sum_min_pkj = 0
        for k in range(i + 1, m):
            sum_min_pkj += min(p[job][k] for job in remaining)

        lb_values.append(c_i_x + sum_p_ij + sum_min_pkj)

    return max(lb_values)
```
__Przebieg algorytmu:__
1. Start od pustej permutacji
2. Rekurencyjne budowanie drzewa permutacji (DFS)
3. Dla każdego węzła:
	- obliczenie LB
	- porównanie z UB
	- ewentualne odcięcie gałęzi
4. Aktualizacja UB po znalezieniu lepszego rozwiązania

## Wyniki
<img width="294" height="138" alt="image" src="https://github.com/user-attachments/assets/e740479e-dc9f-48ec-bbb7-5c575e0bd47e" />

</details>
