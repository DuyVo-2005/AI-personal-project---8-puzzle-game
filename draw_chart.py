import matplotlib.pyplot as plt

# nhom = "Nhóm tìm kiếm không có thông tin"
# algorithms = ['BFS', 'DFS', 'UCS', 'IDS']
# number_visited_node = [114902, 126595, 118083, 17951]
# # execution_times = [803.653, 930.288, 1049.0497, 720.4138]#ms
# # algorithms = ['BFS', 'DFS', 'UCS', 'IDS', ]
# # number_of_step = [23, 112431, 23, 27]

# nhom = "Nhóm tìm kiếm có thông tin"
# algorithms = ['Greedy', 'A*', 'IDA*']
# number_visited_node = [121, 1022, 1022]
# # execution_times = [2.252199, 31.4354, 11.1881]#ms
# # number_of_step = [49, 23, 23]

# nhom = "Nhóm tìm kiếm cục bộ"
# algorithms = ['SHC', 'SAHC', 'StochasticHC', 'Simulated annealing', 'Genetic algorithm', 'Beam search']
# number_visited_node = [2, 2, 2, 2, 420]
# # algorithms = ['Simple hill climbing', 'Steepest ascent hill climbing', 'Stochastic hill climbing', 'Simulated annealing', 'Genetic algorithm', 'Beam search']
# # execution_times = [5210e-05, 9780e-05, 7180e-05, 1.164, 0.128, 2.583]#ms
# number_of_step = [0, 0, 0, 0, 0, 100]

nhom = "Nhóm thuật toán tìm kiếm trong môi trường phức tạp"
algorithms = ['Search with no observation', 'Search with partial observation']
# number_visited_node = [35, 25]
# number_of_step = [3, 3]
execution_times = [67.204, 44.221]#ms

# nhom = "Nhóm tìm kiếm có ràng buộc"
# algorithms = ['Backtracking', 'Test', 'AC3']
# number_visited_node = [114902, 126595, 118083, 17951]
# number_of_step = [42, 872, 30]
# execution_times = [15.277, 578.893, 10.081]#ms


plt.figure(figsize=(10, 6))
bars = plt.bar(algorithms, execution_times, color='lightgreen')
#bars = plt.bar(algorithms, number_visited_node, color='orange')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, f'{yval} ms', ha='center', va='bottom')
    #plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, f'{yval}', ha='center', va='bottom')

plt.title(f'Thời gian thực thi của các thuật toán tìm kiếm AI - {nhom}', fontsize=14)
# plt.title(f'Số bước trong lời giải của các thuật toán tìm kiếm AI - {nhom}', fontsize=14)
#plt.title(f'Số trạng thái đã thăm của các thuật toán tìm kiếm AI - {nhom}', fontsize=14)
plt.xlabel('Thuật toán', fontsize=12)
plt.ylabel('Thời gian (ms)', fontsize=12)
#plt.ylabel('Số trạng thái đã thăm', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
