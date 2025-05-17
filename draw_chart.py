import matplotlib.pyplot as plt

#nhom = "Nhóm tìm kiếm không có thông tin"
# nhom = "Nhóm tìm kiếm có thông tin"
nhom = "Nhóm tìm kiếm cục bộ"

# algorithms = ['BFS', 'DFS', 'UCS', 'IDS', ]
# execution_times = [803.653, 930.288, 1049.0497, 720.4138]#ms

# algorithms = ['Greedy', 'A*', 'IDA*']
# execution_times = [2.252199, 31.4354, 11.1881]#ms

algorithms = ['Simple hill climbing', 'Steepest ascent hill climbing', 'Stochastic hill climbing', 'Simulated annealing', 'Genetic algorithm', 'Beam search']
execution_times = []#ms

# algorithms = ['Simple hill climbing', 'Steepest ascent hill climbing', 'Stochastic hill climbing', 'Simulated annealing', 'Genetic algorithm', 'Beam search']
# execution_times = [803.653, 152.5667599999906, 1049.0497, 720.4138]#ms

plt.figure(figsize=(10, 6))
bars = plt.bar(algorithms, execution_times, color='lightgreen')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 5, f'{yval} μs', ha='center', va='bottom')

plt.title(f'Thời gian thực thi của các thuật toán tìm kiếm AI - {nhom}', fontsize=14)
plt.xlabel('Thuật toán', fontsize=12)
plt.ylabel('Thời gian (μs)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
