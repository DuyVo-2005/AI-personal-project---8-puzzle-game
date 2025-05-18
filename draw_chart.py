import matplotlib.pyplot as plt

# nhom = "Nhóm tìm kiếm không có thông tin"
# nhom = "Nhóm tìm kiếm có thông tin"
# nhom = "Nhóm tìm kiếm cục bộ"
# nhom = "Nhóm tìm kiếm có ràng buộc"
nhom = "Nhóm thuật toán tìm kiếm trong môi trường phức tạp"

# algorithms = ['BFS', 'DFS', 'UCS', 'IDS', ]
# execution_times = [803.653, 930.288, 1049.0497, 720.4138]#ms

# algorithms = ['Greedy', 'A*', 'IDA*']
# execution_times = [2.252199, 31.4354, 11.1881]#ms

# algorithms = ['Simple hill climbing', 'Steepest ascent hill climbing', 'Stochastic hill climbing', 'Simulated annealing', 'Genetic algorithm', 'Beam search']
# algorithms = ['SHC', 'SAHC', 'StochasticHC', 'Simulated annealing', 'Genetic algorithm', 'Beam search']
# execution_times = [5210e-05, 9780e-05, 7180e-05, 1.164, 0.128, 2.583]#ms

# algorithms = ['Backtracking', 'Test', 'AC3']
# execution_times = [15.277, 578.893, 10.081]#ms

algorithms = ['Search with no observation', 'Search with partial observation', 'AC3']
execution_times = [67.204, 44.221, 131.102]#ms

plt.figure(figsize=(10, 6))
bars = plt.bar(algorithms, execution_times, color='lightgreen')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f'{yval} ms', ha='center', va='bottom')

plt.title(f'Thời gian thực thi của các thuật toán tìm kiếm AI - {nhom}', fontsize=14)
plt.xlabel('Thuật toán', fontsize=12)
plt.ylabel('Thời gian (ms)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
