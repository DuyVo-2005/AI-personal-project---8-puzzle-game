from PyQt6 import uic, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow
from tkinter import messagebox
import time
import random
from collections import deque

from const import *

end_state_tuple = None
visited_nodes = []
path = None

def is_goal(state:tuple) -> bool:
    global end_state_tuple
    return state == end_state_tuple

def print_state(state):
    for i in range(0, 9, 3):
        print(state[i], state[i+1], state[i+2])
    print("-" * 10)                         

def show_path_in_file(solution):
    global visited_nodes
    with open(CURRENT_DIRECTORY_PATH + "/result.txt", "w", encoding="utf-8") as f:
        f.write("Solution: ")
        if solution == None:
            f.write("\nNo solution")
        else:
            for state in solution:
                    # for i in range(0, 9, 3):
                    #         f.write(f"\n{state[i]}, {state[i+1]}, {state[i+2]}")
                    # f.write("\n")
                    # f.write("-" * 10)
                    f.write(f"\n{state}")
        f.write("\nClose list: ")
        if visited_nodes == []:
            f.write("\nNone")
        else:
            for state in visited_nodes:
                    # for i in range(0, 9, 3):
                    #         f.write(f"\n{state[i]}, {state[i+1]}, {state[i+2]}")
                    # f.write("\n")
                    # f.write("-" * 10)
                    f.write(f"\n{state}")
        messagebox.showinfo("Infomation", "Write to file successfully")

def is_violate_constrain(state):
    if not all(0 <= element <= 8 for element in state):#Kiểm tra các giá trị phải nằm trong [0..8]
        return True
    if len(set(state)) != 9:#Kiểm tra không trùng lặp
        return True
    return False

def generate_random_state():
    return tuple(random.randint(0, 9) for _ in range(9))      

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


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        app = uic.loadUi(CURRENT_DIRECTORY_PATH + "/constrainSatisfactionProblemGUI.ui", self)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.btnRandomInput.clicked.connect(self.random_input)  
        self.btnSolve.clicked.connect(self.solve_click)
        self.cbbAlgorithm.addItems(["Backtracking", "Test", "AC3"])
        self.cbbAlgorithm.setCurrentText("Backtracking")
        self.txtSolveSpeedPerStep.setPlainText("1")
        self.speed_per_step = 1000#ms
        self.btnWriteToFile.clicked.connect(lambda: show_path_in_file(path))
        
    def random_input(self):
        global end_state_tuple
        numbers = random.sample(range(9), 9)
        end_state_tuple = tuple(numbers)
        self.cell1.setPlainText(str(end_state_tuple[0]))
        self.cell2.setPlainText(str(end_state_tuple[1]))
        self.cell3.setPlainText(str(end_state_tuple[2]))
        self.cell4.setPlainText(str(end_state_tuple[3]))
        self.cell5.setPlainText(str(end_state_tuple[4]))
        self.cell6.setPlainText(str(end_state_tuple[5]))
        self.cell7.setPlainText(str(end_state_tuple[6]))
        self.cell8.setPlainText(str(end_state_tuple[7]))
        self.cell9.setPlainText(str(end_state_tuple[8]))
    
    def update_cell(self, cell, value):
        if value == -1:
            cell.setPlainText(" ")
        else:
            cell.setPlainText(str(value))
        
    def solve_click(self):
        global end_state_tuple, path
        algorithm_type = self.cbbAlgorithm.currentText()
        
        variables = []#Danh sách các ô
        for i in range(1, 10):
            variables.append(f'X{i}')

        #Khởi tạo miền giá trị ban đầu: mọi ô có thể là 0..8
        domains = {}
        min_pole = [
            self.spinBox_minX1.value(),
            self.spinBox_minX2.value(),
            self.spinBox_minX3.value(),
            self.spinBox_minX4.value(),
            self.spinBox_minX5.value(),
            self.spinBox_minX6.value(),
            self.spinBox_minX7.value(),
            self.spinBox_minX8.value(),
            self.spinBox_minX9.value()
        ]
        max_pole = [
            self.spinBox_maxX1.value(),
            self.spinBox_maxX2.value(),
            self.spinBox_maxX3.value(),
            self.spinBox_maxX4.value(),
            self.spinBox_maxX5.value(),
            self.spinBox_maxX6.value(),
            self.spinBox_maxX7.value(),
            self.spinBox_maxX8.value(),
            self.spinBox_maxX9.value()
        ]
        idx = 0
        for var in variables:
            domains[var] = list(range(min_pole[idx], max_pole[idx] + 1))
            idx += 1
        # domains['X0'] = [1]
        # domains['X1'] = [2]
        print(domains)

        neighbors = { }
        for var in variables:
            neighbors[var] = [v for v in variables if v != var]

        domains_copy = domains.copy()
        #has_result = ac3(domains_copy, neighbors)
        def backtracking_search(board:list, pos: int, used, goal, path: list) -> list:
            """
            Args:
                board (list)
                pos (int)
                element pos idx
                0 1 2
                3 4 5
                6 7 8
                used (_type_)
                goal (int)
            Return
                path (list)
            """
            global visited_nodes
            if pos == 9:
                if board == goal:
                    print("Found goal state:")
                    for board in path:
                        print_board(board)
                    return path
                return []
            if pos > 9:
                return []

            for num in range(9):
                if not used[num]:
                    board[pos] = num
                    used[num] = True
                    visited_nodes.append(board.copy())
                    path.append(board[:])#bản sao
                    result = backtracking_search(board, pos + 1, used, goal, path)
                    if result:
                        return result
                    path.pop()
                    used[num] = False
                    board[pos] = -1#quay lui

        def print_board(board):
            for i in range(0, 9, 3):
                print(board[i:i+3])
            print()
            print("--------------------")
            print()
            
        def test_search():#Tìm kiếm kiểm thử
            visited = set()
            path = []
            goal_state = generate_random_state()
            while is_violate_constrain(goal_state):
                new_state = generate_random_state()
                print_state(new_state)
                #print("\n------------\n")
                path.append(new_state)
                if not is_violate_constrain(new_state):
                    print("Solved")
                    return path
                visited.add(new_state)
            
        start_time = time.time()
        if not algorithm_type == "Test" or not algorithm_type == "AC3":
            if end_state_tuple is None:
                messagebox.showerror("Error", "Please enter values first!")
                return
            try:
                end_state_tuple = tuple([
                int(self.cell1.toPlainText()), int(self.cell2.toPlainText()), int(self.cell3.toPlainText()),
                int(self.cell4.toPlainText()), int(self.cell5.toPlainText()), int(self.cell6.toPlainText()),
                int(self.cell7.toPlainText()), int(self.cell8.toPlainText()), int(self.cell9.toPlainText())]
                )
            except ValueError:
                messagebox.showerror("Error", "Invalid input values!")
                return
        try:
            if int(float(self.txtSolveSpeedPerStep.toPlainText()) * 1000) >= 1:#ms
                self.speed_per_step  = int(float(self.txtSolveSpeedPerStep.toPlainText()) * 1000)
            else:
                messagebox.showerror("Error", "Speed per step must above or equal 0.001s")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid speed per step")
            return
        path = []
        if algorithm_type == "Test":
            path = test_search()
        else:
            initial_board = [-1] * 9
            used = [False] * 9#ràng buộc không trùng giá trị trong trạng thái
            path = backtracking_search(initial_board, 0, used, list(end_state_tuple), path)
            print(path)
        if path == []:
            messagebox.showinfo("Information", "No solutions found!")
            self.txtTotalStep.setPlainText("0")
            self.txtStep.setPlainText("0")
        else:         
            self.play_solution(path)        
            self.txtTotalStep.setPlainText(str(len(path)))
        end_time = time.time()
        execution_time = end_time - start_time
        self.txtSolveTime.setPlainText(f"{execution_time:.5f}(s)") 
                
    def play_solution(self, solution):
        self.step = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_step)
        self.solution = solution
        self.timer.start(self.speed_per_step)

    def update_step(self):
        if self.step < len(self.solution):
            e = self.solution[self.step]
            self.step += 1
            self.txtStep.setPlainText(str(self.step))
            self.update_cell(self.cell1_3, e[0])
            self.update_cell(self.cell2_3, e[1])
            self.update_cell(self.cell3_3, e[2])
            self.update_cell(self.cell4_3, e[3])
            self.update_cell(self.cell5_3, e[4])
            self.update_cell(self.cell6_3, e[5])
            self.update_cell(self.cell7_3, e[6])
            self.update_cell(self.cell8_3, e[7])
            self.update_cell(self.cell9_3, e[8])
        else:
            self.timer.stop()
                
app = QApplication([])
window = MyApp()
window.show()
app.exec()
