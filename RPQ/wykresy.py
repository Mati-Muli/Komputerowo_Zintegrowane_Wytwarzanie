import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def plot_gantt(permutation, title="Harmonogram RPQ"):
    fig, ax = plt.subplots(figsize=(16, 10))

    t_moment = 0
    max_time = 0
    data = []
    for task in permutation:
        s_j = max(task.r, t_moment)  # Moment rozpoczęcia Sj
        c_j = s_j + task.p  # Moment zakończenia Cj
        q_end = c_j + task.q  # Moment opuszczenia systemu[cite: 1]

        data.append({
            'id': task.id,
            'r_val': task.r,
            'r_start': s_j - task.r,
            's_j': s_j,
            'c_j': c_j,
            'q_end': q_end
        })
        t_moment = c_j
        max_time = max(max_time, q_end)

    # 2. Rysowanie warstwowe
    for i, d in enumerate(data):
        y_pos = i
        ax.broken_barh([(d['r_start'], d['r_val'])], (y_pos + 0.55, 0.2),
                       facecolors='palegreen', edgecolors='green', alpha=0.7)
        ax.text(d['r_start'], y_pos + 0.65, f" r={d['r_val']}", va='center', fontsize=8, color='darkgreen')

        ax.broken_barh([(d['s_j'], d['c_j'] - d['s_j'])], (y_pos + 0.3, 0.4),
                       facecolors='royalblue', edgecolors='black', zorder=10)
        ax.text(d['s_j'] + (d['c_j'] - d['s_j']) / 2, y_pos + 0.5, f"Z{d['id']}",
                ha='center', va='center', color='white', fontweight='bold')

        ax.broken_barh([(d['c_j'], d['q_end'] - d['c_j'])], (y_pos + 0.2, 0.15),
                       facecolors='salmon', edgecolors='red', alpha=0.6)

    ax.set_ylim(-0.5, len(data))
    ax.set_xlim(min(0, min(d['r_start'] for d in data)), max_time + 10)
    ax.set_xlabel("Czas [t]", fontsize=12)
    ax.set_ylabel("Zadania w kolejności uszeregowania", fontsize=12)
    ax.set_yticks([i + 0.5 for i in range(len(data))])
    ax.set_yticklabels([f"Krok {i + 1}" for i in range(len(data))])

    ax.grid(True, axis='x', linestyle='--', alpha=0.4)

    legend_elements = [
        Patch(facecolor='palegreen', edgecolor='green', label='Czas przygotowania (r)'),
        Patch(facecolor='royalblue', edgecolor='black', label='Czas wykonania (p)'),
        Patch(facecolor='salmon', edgecolor='red', label='Czas stygnięcia (q)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', ncol=3)

    plt.title(title, fontsize=15, pad=20)
    plt.tight_layout()
    plt.show()