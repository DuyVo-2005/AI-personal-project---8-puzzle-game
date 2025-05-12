from collections import deque

def different_constraint(x: int, y: int):
    return x != y

def ac3(domains, neighbors):
    queue = deque([(Xi, Xj) for Xi in domains for Xj in neighbors[Xi]])# queue chứa các cạnh (cung), khởi tạo là tất cả các cạnh
    while queue:
        Xi, Xj = queue.popleft()
        if revise(domains, Xi, Xj):
            if not domains[Xi]:
                return False#Domain rỗng -> không hợp lệ -> dừng (an consistency is found)
            for Xk in neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return True

def revise(domains: dict, Xi, Xj):
    revised = False#biến ghi nhận có sửa đổi hay không
    for x in domains[Xi][:]:
        #Không có y nào trong Dj cho phép (x,y) thỏa mãn ràng buộc (khác nhau) giữa Di và Dj
        if all(not different_constraint(x, y) for y in domains[Xj]):
            domains[Xi].remove(x)
            revised = True
    return revised

variables = []#Danh sách các ô
for i in range(9):
    variables.append(f'X{i}')

#Khởi tạo miền giá trị ban đầu: mọi ô có thể là 0..8
domains = {}
for var in variables:
    domains[var] = list(range(9))
domains['X0'] = [1]
domains['X1'] = [2]

neighbors = { }
for var in variables:
    neighbors[var] = [v for v in variables if v != var]

domains_copy = domains.copy()
has_result = ac3(domains_copy, neighbors)

if has_result:
    print("Kết quả thuật toán AC3:")
    for var in sorted(domains_copy):
        print(f"{var}: {domains_copy[var]}")
else:
    print("Không tìm ra lời giải")