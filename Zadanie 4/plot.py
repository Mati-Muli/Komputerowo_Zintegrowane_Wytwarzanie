import matplotlib.pyplot as plt

def plot_gantt(sequence, title="Wykres Gantta"):
    fig, ax = plt.subplots(figsize=(10, 3))
    current_time = 0

    for i, task in enumerate(sequence):
        start_time = current_time
        finish_time = start_time + task.p
        is_tardy = finish_time > task.d

        color = 'red' if is_tardy else 'skyblue'
        ax.broken_barh([(start_time, task.p)], (10, 9), facecolors=color, edgecolor='black')
        ax.text(start_time + task.p / 2, 14.5, f"T{task.id}", ha='center', va='center', fontweight='bold')
        ax.text(start_time + task.p / 2, 11, f"d:{task.d}", ha='center', va='center', fontsize=8)

        current_time = finish_time

    ax.set_ylim(5, 20)
    ax.set_xlim(0, current_time + 2)
    ax.set_xlabel('Czas')
    ax.set_yticks([])
    ax.set_title(title)
    ax.grid(True, axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()