from PyQt6 import uic, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow
from tkinter import messagebox
import time
import random

from const import *

end_state_tuple = None
visited_nodes = None

def is_goal(state:tuple) -> bool:
    global end_state_tuple
    return state == end_state_tuple

def succ(state: tuple) -> list:
    "return children with (action, state)"
    children = []
    zero_index = state.index(0)
    row, col = zero_index//3, zero_index%3

    moves = {
        'UP': (-1, 0),
        'DOWN': (1, 0),
        'LEFT': (0, -1),
        'RIGHT': (0, 1)
    }

    for action, (dr, dc) in moves.items():
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            new_state = list(state)           
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
            children.append((action, tuple(new_state)))
    return children

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

# def generate_unique_can_solved_puzzle_states(n):   
#     result = []
#     while len(result) < n:
#         nums = list(range(9))
#         random.shuffle(nums)
#         state = tuple(nums)
#         if state not in result and not violate_constrain(state):          
#             result.append(state)
#     return result

def is_violate_constrain(state):
    if not all(0 <= element <= 8 for element in state):#Kiểm tra các giá trị phải nằm trong [0..8]
        return True
    if len(set(state)) != 9:#Kiểm tra không trùng lặp
        return True
    return False

def generate_random_state():
    return tuple(random.randint(0, 9) for _ in range(9))

def test_search():#Tìm kiếm kiểm thử
    visited = set()
    goal_state = generate_random_state()
    while is_violate_constrain(goal_state):
        new_state = generate_random_state()
        print_state(new_state)
        #print("\n------------\n")
        if not is_violate_constrain(new_state):
            print("Solved")
            return
        visited.add(new_state)                   

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        app = uic.loadUi(CURRENT_DIRECTORY_PATH + "/constrainSatisfactionProblemGUI.ui", self)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.btnRandomInput.clicked.connect(self.random_input)
        self.btnLoadValue.clicked.connect(self.load_value)     
        self.btnSolve.clicked.connect(self.solve_click)
        self.txtSolveSpeedPerStep.setPlainText("1")
        self.speed_per_step = 1000#ms
        self.btnWriteToFile.clicked.connect(lambda: show_path_in_file(path))
        self.btnQuit.clicked.connect(self.close)
        
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
        
    def solve_click(self):
        global end_state_tuple, path
        start_time = time.time()
        if end_state_tuple is None:
                messagebox.showerror("Error", "Please load values first!")
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
        
        # initial_board = [9] * 9
        # used = [False] * 9#ràng buộc không trùng giá trị trong trạng thái
        # # goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        # solve_path = []
        # backtracking_search(initial_board, 0, used, end_state_tuple, solve_path)
        initial_board = [-1] * 9
        used = [False] * 9#ràng buộc không trùng giá trị trong trạng thái
        # goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        # goal_state = [6, 7, 8, 0, 1, 2, 3, 4, 5]

        def backtracking_search(board:list, pos: int, used, goal, path: list):
            """_summary_

            Args:
                board (list): _description_
                pos (int): _description_
                element pos idx
                0 1 2
                3 4 5
                6 7 8
                used (_type_): _description_
                goal (int): 
                
                path (list): _description_
            """
            if pos == 9:
                if board == goal:
                    print("Found goal state:")
                    #print_board(board)
                    for board in path:
                        print_board(board)
                    return path.copy()
                return []
            if pos > 9:
                return []

            for num in range(9):
                if not used[num]:
                    board[pos] = num
                    used[num] = True
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
        path = []
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
            self.cell1_3.setPlainText(str(e[0]))
            self.cell2_3.setPlainText(str(e[1]))
            self.cell3_3.setPlainText(str(e[2]))
            self.cell4_3.setPlainText(str(e[3]))
            self.cell5_3.setPlainText(str(e[4]))
            self.cell6_3.setPlainText(str(e[5]))
            self.cell7_3.setPlainText(str(e[6]))
            self.cell8_3.setPlainText(str(e[7]))
            self.cell9_3.setPlainText(str(e[8]))
        else:
            self.timer.stop()
                
    def load_value(self):
        global end_state_tuple
        try:
            end_state_tuple = tuple([
            int(self.cell1.toPlainText()), int(self.cell2.toPlainText()), int(self.cell3.toPlainText()),
            int(self.cell4.toPlainText()), int(self.cell5.toPlainText()), int(self.cell6.toPlainText()),
            int(self.cell7.toPlainText()), int(self.cell8.toPlainText()), int(self.cell9.toPlainText())]
            )
        except ValueError:
            messagebox.showerror("Error", "Invalid input values!")
        else:
            messagebox.showinfo("Notification", "Values loaded successfully!")      

app = QApplication([])
window = MyApp()
window.show()
app.exec()
