from PyQt6 import uic, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow
from tkinter import messagebox
import time
import random
from collections import deque
from copy import deepcopy

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

def show_path_in_file(solution: dict):
    global visited_nodes
    with open(CURRENT_DIRECTORY_PATH + "/result.txt", "w", encoding="utf-8") as f:
        f.write("Solution: ")
        if solution == None:
            f.write("\nNo solution")
        else:
            for variable, value in solution.items():
                    # for i in range(0, 9, 3):
                    #         f.write(f"\n{state[i]}, {state[i+1]}, {state[i+2]}")
                    # f.write("\n")
                    # f.write("-" * 10)
                    f.write(f"\n{variable}: {value}")
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
    return tuple(random.randint(0, 8) for _ in range(9))      

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

def convert_domains_to_string(domains: dict):
    result = ""
    for variable, domain in domains.items():
        result += f"{variable}: {domain}" + "\n"
    return result

domains = {}

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        app = uic.loadUi(CURRENT_DIRECTORY_PATH + "/constrainSatisfactionProblemGUI.ui", self)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.btnSolve.clicked.connect(self.solve_click)
        self.cbbAlgorithm.addItems(["Backtracking", "Test", "AC3"])
        self.cbbAlgorithm.setCurrentText("Backtracking")
        self.txtSolveSpeedPerStep.setPlainText("1")
        self.speed_per_step = 1000#ms
        self.btnWriteToFile.clicked.connect(lambda: show_path_in_file(path))
    
    def update_cell(self, cell, value):
        if value == -1:
            cell.setPlainText(" ")
        else:
            cell.setPlainText(str(value))
        
    def solve_click(self):
        global path, visited_nodes, domains
        path, visited_nodes = [], []
        algorithm_type = self.cbbAlgorithm.currentText()
        
        variables = []#Danh sách các ô
        for i in range(1, 10):
            variables.append(f'X{i}')

        #Khởi tạo miền giá trị ban đầu: mọi ô có thể là 0..8
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
        print("Domain ban đầu:")
        print(domains)

        neighbors = { }
        for var in variables:
            neighbors[var] = [v for v in variables if v != var]

        #domains_copy = domains.copy()
        times = [0]#số lần thử gán
        
        def select_unassigned_variable(variables, assignment):
            for variable in variables:
                if variable not in assignment:
                    return variable
            return False
        def is_consistent(value:int, assignment: set) -> bool:
            """check constraint: all var is different"""
            for other_variable in assignment:
                if assignment[other_variable] == value:
                    return False
            return True
        def convert_assignment_to_state(assignment: dict) -> tuple:
            state = [-1, -1, -1, -1, -1, -1, -1, -1, -1]#Trạng thái ban đầu
            for variable, value in assignment.items():
                index = int(variable.strip("X"))
                state[index - 1] = value
            return tuple(state)
        def backtracking_search(assignment, times: list):
            if len(assignment) == len(variables):
                print("Tìm ra lời giải!")
                return assignment
            variable = select_unassigned_variable(variables, assignment)
            for value in domains[variable]:
                times[0] += 1
                print(f"Lần thử: {times[0]}")
                print(f"Thử {variable} = {value}")
                if is_consistent(value, assignment):
                    assignment[variable] = value
                    print(f"Gán {variable} = {value} -> assignment hiện tại: {assignment}")
                    visited_nodes.append(convert_assignment_to_state(assignment.copy()))
                    result = backtracking_search(assignment, times)
                    if result:
                        return result
                    print(f" <- Backtracking khỏi {variable} = {value}")
                    del assignment[variable]# Hủy gán (quay lui)
                    visited_nodes.append(convert_assignment_to_state(assignment.copy()))
                else:
                    print(f"Vi phạm ràng buộc! Không gán!")
            return []
            
        def test_search():#Tìm kiếm kiểm thử
            global visited_nodes
            visited = set()
            path = []
            new_state = (-1,-1,-1,-1,-1,-1,-1,-1,-1)
            while is_violate_constrain(new_state):
                new_state = generate_random_state()
                print_state(new_state)
                #print("\n------------\n")
                path.append(new_state)
                visited_nodes = path.copy()
                if not is_violate_constrain(new_state):
                    print("Solved")
                    return path
                visited.add(new_state)
            
        start_time = time.perf_counter()       
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
            print(f"Số lần thử gán: {len(path)}")
        elif algorithm_type == "AC3":
            if ac3(domains, neighbors) == False:
                messagebox.showerror("Error", "An consistency is found")
            else:
                print("Domain sau khi lọc:")
                print(domains)
                path = backtracking_search({}, times)
                print(path)
                print(f"Số lần thử gán: {times[0]}")
        else:           
            path = backtracking_search({}, times)
            print(path)
            print(f"Số lần thử gán: {times}")
        if path == []:
            messagebox.showinfo("Information", "No solutions found!")
            self.txtTotalStep.setPlainText("0")
            self.txtStep.setPlainText("0")
        else:         
            self.play_solution(visited_nodes)        
            self.txtTotalStep.setPlainText(str(len(visited_nodes)))
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        self.txtSolveTime.setPlainText(f"{execution_time:.10f}(s)")
        self.output_domain.setPlainText(convert_domains_to_string(domains))
                
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
