# from collections import deque
# import copy

# def constraint_different(x, y):
#     return x != y

# def ac3(domains, neighbors):
#     queue = deque([(Xi, Xj) for Xi in domains for Xj in neighbors[Xi]])

#     while queue:
#         Xi, Xj = queue.popleft()
#         if revise(domains, Xi, Xj):
#             if not domains[Xi]:
#                 return False  # Domain trống => không hợp lệ
#             for Xk in neighbors[Xi]:
#                 if Xk != Xj:
#                     queue.append((Xk, Xi))
#     return True

# def revise(domains, Xi, Xj):
#     revised = False
#     for x in domains[Xi][:]:
#         if all(not constraint_different(x, y) for y in domains[Xj]):
#             domains[Xi].remove(x)
#             revised = True
#     return revised

# # Danh sách biến
# variables = [f'V{i}' for i in range(9)]

# # Khởi tạo miền ban đầu: mọi ô có thể là 0..8
# domains = {var: list(range(9)) for var in variables}
# domains['V0'] = [1]
# domains['V1'] = [2]
# #domains['V2'] = [0,1,2,3,4,5,6,7,8]
# #domains['V3'] = [0,1,2,3,4,5,6,7,8]
# #domains['V4'] = [0,1,2,3,4,5,6,7,8]
# #domains['V5'] = [0,1,2,3,4,5,6,7,8]
# #domains['V6'] = [0,1,2,3,4,5,6,7,8]
# #domains['V7'] = [0,1,2,3,4,5,6,7,8]
# #domains['V8'] = [0,1,2,3,4,5,6,7,8]

# # Thiết lập neighbors để kiểm tra all-different
# neighbors = {var: [v for v in variables if v != var] for var in variables}

# # Gọi AC-3
# domains_copy = copy.deepcopy(domains)
# result = ac3(domains_copy, neighbors)

# # In kết quả
# print("Kết quả AC-3:", result)
# for var in sorted(domains_copy):
#     print(f"{var}: {domains_copy[var]}")

times = [0]
print(times[0] + 1)
