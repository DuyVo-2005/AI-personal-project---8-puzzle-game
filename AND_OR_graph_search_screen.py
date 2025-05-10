# tìm kiếm không có thông tin: BFS, DFS, UCS, IDS
# tìm kiếm có thông tin: Greedy, A*, IDA*
# tìm kiếm cục bộ: Steepest Ascent Hill climbing, Simple Hill climbing, Stochastic Hill Climbing ,Simulated annealing, Beam Search, Genetic algorithm
from PyQt6 import uic, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow
from tkinter import messagebox
import time
import random
import math

from const import *
from dataStructures import *

MAX_DEPTH = 30

start_state_tuple = tuple([0,0,0,0,0,0,0,0,0])
end_state_tuple = tuple([0,0,0,0,0,0,0,0,0])
root = None
path = None
visited_nodes = None

def is_goal(state):
    return state == end_state_tuple

def find_blank(state):
    index = state.index(0)
    return index // 3, index % 3

def move(state, direction):
    i, j = find_blank(state)
    index = i * 3 + j
    new_state = list(state)

    if direction == 'up' and i > 0:
        swap_idx = (i - 1) * 3 + j
    elif direction == 'down' and i < 2:
        swap_idx = (i + 1) * 3 + j
    elif direction == 'left' and j > 0:
        swap_idx = i * 3 + (j - 1)
    elif direction == 'right' and j < 2:
        swap_idx = i * 3 + (j + 1)
    else:
        return state#Không hợp lệ trả về trạng thái như cũ

    new_state[index], new_state[swap_idx] = new_state[swap_idx], new_state[index]
    return tuple(new_state)

def actions(state):
    i, j = find_blank(state)
    moves = []
    if i > 0: moves.append('up')
    if i < 2: moves.append('down')
    if j > 0: moves.append('left')
    if j < 2: moves.append('right')
    return moves

def results(state, action):
    #Có thể di chuyển đúng hoặc không di chuyển - do cảm biến có vấn đề trong môi trường không phức tạp
    result = [move(state, action)]
    if random.random() < 0.5:
        result.append(state)  # Không di chuyển
    return result

def AND_OR_SEARCH(problem):
    memo = {}
    return OR_SEARCH(problem['initial'], problem, [], 0, memo)

def OR_SEARCH(state, problem, path, depth, memo):
    if is_goal(state):
        return []
    if state in path:
        return 'failure'
    if depth > MAX_DEPTH:
        return 'failure'
    if state in memo:
        return memo[state]

    for action in actions(state):
        result_states = results(state, action)
        plan = AND_SEARCH(result_states, problem, path + [state], depth + 1, memo)
        if plan != 'failure':
            full_plan = [action, plan]
            memo[state] = full_plan
            return full_plan
    memo[state] = 'failure'
    return 'failure'

def AND_SEARCH(states, problem, path, depth, memo):
    plans = []
    for s in states:
        plan = OR_SEARCH(s, problem, path, depth + 1, memo)
        if plan == 'failure':
            return 'failure'
        plans.append(plan)
    return plans
def print_plan_tree(plan, indent=0):
    if plan == 'failure':
        print(' ' * indent + 'failure')
    elif plan == []:
        print(' ' * indent + 'GOAL')
    elif isinstance(plan, list):
        action = plan[0]
        subplan = plan[1]
        print(' ' * indent + f'→ {action}')
        if isinstance(subplan, list):
            for sp in subplan:
                print_plan_tree(sp, indent + 4)
        else:
            print_plan_tree(subplan, indent + 4)
    else:
        print(' ' * indent + str(plan))

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
        if visited_nodes == None:
                f.write("\nNone")
        else:
                for state in visited_nodes.set:
                        # for i in range(0, 9, 3):
                        #         f.write(f"\n{state[i]}, {state[i+1]}, {state[i+2]}")
                        # f.write("\n")
                        # f.write("-" * 10)
                        f.write(f"\n{state}")
        messagebox.showinfo("Infomation", "Write to file successfully")

# def extract_state_sequence(start_state, plan):
#     sequence = [start_state]
#     current_state = start_state
#     if plan == 'failure' or plan == []:
#         return sequence
#     def dfs(state, plan):
#         nonlocal sequence
#         if plan == []:
#             return
#         action = plan[0]
#         next_states = results(state, action)
#         for next_state in next_states:
#             if next_state != state:
#                 sequence.append(next_state)
#                 break  # Chỉ lấy một kết quả để mô phỏng
#         subplans = plan[1]
#         if isinstance(subplans, list):
#             for subplan in subplans:
#                 dfs(sequence[-1], subplan)
#         else:
#             dfs(sequence[-1], subplans)
#     dfs(current_state, plan)
#     return sequence

def extract_state_sequence(plan, state):
    if plan == 'failure' or plan == []:
        return [state]
    sequence = [state]
    if isinstance(plan, list):
        action = plan[0]
        subplans = plan[1]
        for subplan in subplans:
            # Do hàm results() không chắc chắn → chọn hành động đầu tiên tạo ra trạng thái khác
            for result_state in results(state, action):
                if result_state != state:
                    sequence += extract_state_sequence(subplan, result_state)
                    break
    return sequence

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        app = uic.loadUi(CURRENT_DIRECTORY_PATH + "/AND_OR_graph_search_GUI.ui", self)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.btnRandomInput.clicked.connect(self.random_input)
        self.btnLoadValue.clicked.connect(self.load_value)        
        self.btnSolve.clicked.connect(self.solve_click)
        self.txtSolveSpeedPerStep.setPlainText("1")
        self.speed_per_step = 1000#ms
        self.btnWriteToFile.clicked.connect(lambda: show_path_in_file(path))
        self.txt_plan_tree.setReadOnly(True)

    def random_input(self):
        global start_state_tuple, end_state_tuple
        numbers = random.sample(range(9), 9)
        start_state_tuple = tuple(numbers)
        # for i in range(9):
        #     start_state_tuple[i] = numbers[i]
        self.cell1.setPlainText(str(start_state_tuple[0]))
        self.cell2.setPlainText(str(start_state_tuple[1]))
        self.cell3.setPlainText(str(start_state_tuple[2]))
        self.cell4.setPlainText(str(start_state_tuple[3]))
        self.cell5.setPlainText(str(start_state_tuple[4]))
        self.cell6.setPlainText(str(start_state_tuple[5]))
        self.cell7.setPlainText(str(start_state_tuple[6]))
        self.cell8.setPlainText(str(start_state_tuple[7]))
        self.cell9.setPlainText(str(start_state_tuple[8]))
        
        numbers = random.sample(range(9), 9)
        end_state_tuple = tuple(numbers)
        self.cell1_end.setPlainText(str(end_state_tuple[0]))
        self.cell2_end.setPlainText(str(end_state_tuple[1]))
        self.cell3_end.setPlainText(str(end_state_tuple[2]))
        self.cell4_end.setPlainText(str(end_state_tuple[3]))
        self.cell5_end.setPlainText(str(end_state_tuple[4]))
        self.cell6_end.setPlainText(str(end_state_tuple[5]))
        self.cell7_end.setPlainText(str(end_state_tuple[6]))
        self.cell8_end.setPlainText(str(end_state_tuple[7]))
        self.cell9_end.setPlainText(str(end_state_tuple[8]))
        self.load_value()
    def format_plan_tree(self, plan, indent=0):
        if plan == 'failure':
            return ' ' * indent + 'failure\n'
        elif plan == []:
            return ' ' * indent + 'GOAL\n'
        elif isinstance(plan, list):
            action = plan[0]
            subplan = plan[1]
            result = ' ' * indent + f'→ {action}\n'
            if isinstance(subplan, list):
                for sp in subplan:
                    result += self.format_plan_tree(sp, indent + 4)
            else:
                result += self.format_plan_tree(subplan, indent + 4)
            return result
        else:
            return ' ' * indent + str(plan) + '\n'
    def solve_click(self):
        global root, path     
        start_time = time.time()
        if root is None:
                messagebox.showerror("Error", "Please load values first!")
                return
        try:
            if int(float(self.txtSolveSpeedPerStep.toPlainText()) * 1000) >= 1:#ms
                self.speed_per_step = int(float(self.txtSolveSpeedPerStep.toPlainText()) * 1000)
            else:
                messagebox.showerror("Error", "Speed per step must above or equal 0.001s")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid speed per step")
            return

        problem = {'initial': start_state_tuple}
        plan = AND_OR_SEARCH(problem)
        
        if plan is None:
            messagebox.showinfo("Information", "No solutions found!")
            self.txtTotalStep.setPlainText("0")
            self.txtStep.setPlainText("0")          
        else:          
            path = extract_state_sequence(start_state_tuple, plan)
            print(start_state_tuple)
            print(end_state_tuple)
            print(path)
            print(plan)
            self.play_solution(path)
            self.txtTotalStep.setPlainText(str(len(path)))
        end_time = time.time()
        execution_time = end_time - start_time
        self.txtSolveTime.setPlainText(f"{execution_time:.5f}(s)")
        self.txt_plan_tree.setPlainText(self.format_plan_tree(plan))

    def play_solution(self, solution):
        self.step = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_step)
        self.solution = solution
        self.timer.start(self.speed_per_step)
        
    def update_cell(self, cell, value):
        if value == 0:
            cell.setPlainText(" ")
        else:
            cell.setPlainText(str(value))
            
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

    def load_value(self):
        global start_state_tuple, end_state_tuple, root
        try:
            start_state_tuple = tuple([
            int(self.cell1.toPlainText()), int(self.cell2.toPlainText()), int(self.cell3.toPlainText()),
            int(self.cell4.toPlainText()), int(self.cell5.toPlainText()), int(self.cell6.toPlainText()),
            int(self.cell7.toPlainText()), int(self.cell8.toPlainText()), int(self.cell9.toPlainText())]
            )             
            root = make_node(None, None, start_state_tuple)
        except ValueError:
            messagebox.showerror("Error", "Invalid input values!")
        else:
            messagebox.showinfo("Notification", "Values loaded successfully!")

app = QApplication([])
window = MyApp()
window.show()
app.exec()
