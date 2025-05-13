# Danh sách biến
variables = ["X", "Y", "Z"]


# Domain mới đã được rút gọn
# domains = {
#     "X": [1, 2],
#     "Y": [2, 3],
#     "Z": [1, 3]
# }
domains = {
    "X": [0,1,2,3,4,5,6,7,8],
    "Y": [0,1,2,3,4,5,6,7,8],
    "Z": [0,1,2,3,4,5,6,7,8]
}
# Ràng buộc: All-different (giá trị của mỗi biến phải khác nhau)
def is_consistent(var, value, assignment):
    for other_var in assignment:
        if assignment[other_var] == value:
            return False
    return True

# Chọn biến chưa được gán
def select_unassigned_variable(variables, assignment):
    for var in variables:
        if var not in assignment:
            return var
    return None

def backtrack(assignment):
    if len(assignment) == len(variables):#Phép gán hoàn tất
        return assignment

    var = select_unassigned_variable(variables, assignment)
    for value in domains[var]:
        if is_consistent(var, value, assignment):
            assignment[var] = value
            result = backtrack(assignment)
            if result:
                return result
            del assignment[var]  # Hủy gán nếu thất bại
    return None

# Gọi thuật toán
solution = backtrack({})
print("Lời giải:", solution)

# import sys
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QPushButton,
#     QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel
# )
# from PyQt6.QtCore import QTimer
# import copy

# # Trạng thái đích
# goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# # Trạng thái bắt đầu (có thể thay đổi)
# initial_state = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]

# # Di chuyển hợp lệ (trái, phải, lên, xuống)
# moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# class PuzzleApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("8 Puzzle Backtracking - PyQt")
#         self.setGeometry(100, 100, 300, 350)

#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)

#         self.table = QTableWidget(3, 3)
#         self.layout.addWidget(self.table)

#         # Nút điều khiển
#         button_layout = QHBoxLayout()
#         self.btn_next = QPushButton("Next")
#         self.btn_auto = QPushButton("Auto")
#         self.btn_reset = QPushButton("Reset")
#         button_layout.addWidget(self.btn_next)
#         button_layout.addWidget(self.btn_auto)
#         button_layout.addWidget(self.btn_reset)
#         self.layout.addLayout(button_layout)

#         # Thông tin trạng thái
#         self.status_label = QLabel("Đang chờ...")
#         self.layout.addWidget(self.status_label)

#         # Sự kiện nút
#         self.btn_next.clicked.connect(self.next_step)
#         self.btn_auto.clicked.connect(self.auto_run)
#         self.btn_reset.clicked.connect(self.reset)

#         self.timer = QTimer()
#         self.timer.timeout.connect(self.next_step)

#         self.reset()

#     def reset(self):
#         self.visited = set()
#         self.path = []
#         self.stack = [(copy.deepcopy(initial_state), [])]
#         self.update_table(initial_state)
#         self.status_label.setText("Đã reset.")
#         self.timer.stop()

#     def update_table(self, state):
#         for i in range(3):
#             for j in range(3):
#                 val = state[i][j]
#                 item = QTableWidgetItem("" if val == 0 else str(val))
#                 self.table.setItem(i, j, item)

#     def next_step(self):
#         if not self.stack:
#             self.status_label.setText("Không tìm được lời giải.")
#             self.timer.stop()
#             return

#         current_state, path = self.stack.pop()
#         key = tuple(map(tuple, current_state))
#         if key in self.visited:
#             return
#         self.visited.add(key)

#         self.update_table(current_state)
#         self.path = path

#         if current_state == goal:
#             self.status_label.setText(f"✅ Đã giải xong sau {len(path)} bước.")
#             self.timer.stop()
#             return

#         zero_x, zero_y = next((i, j) for i in range(3) for j in range(3) if current_state[i][j] == 0)

#         for dx, dy in moves:
#             nx, ny = zero_x + dx, zero_y + dy
#             if 0 <= nx < 3 and 0 <= ny < 3:
#                 new_state = copy.deepcopy(current_state)
#                 new_state[zero_x][zero_y], new_state[nx][ny] = new_state[nx][ny], new_state[zero_x][zero_y]
#                 new_key = tuple(map(tuple, new_state))
#                 if new_key not in self.visited:
#                     self.stack.append((new_state, path + [new_state]))

#         self.status_label.setText(f"Đang duyệt {len(self.visited)} trạng thái...")

#     def auto_run(self):
#         self.timer.start(500)  # 0.5 giây mỗi bước

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     win = PuzzleApp()
#     win.show()
#     sys.exit(app.exec())

