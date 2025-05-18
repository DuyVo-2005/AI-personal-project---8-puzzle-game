# tìm kiếm không có thông tin: BFS, DFS, UCS, IDS
# tìm kiếm có thông tin: Greedy, A*, IDA*
# tìm kiếm cục bộ: Steepest Ascent Hill climbing, Simple Hill climbing, Stochastic Hill Climbing ,Simulated annealing, Beam Search, Genetic algorithm
from PyQt6 import uic, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow
from tkinter import messagebox
import time
import random

from const import *
from dataStructures import *
from search_in_complex_environment import search_in_complex_environment_solve, MOVES

WINDOW_WIDTH, WINDOW_HEIGHT = 1012, 680

start_state_tuple = tuple([0,0,0,0,0,0,0,0,0])
start_state_tuple2 = tuple([0,0,0,0,0,0,0,0,0])
start_state_tuple3 = tuple([0,0,0,0,0,0,0,0,0])
start_state_tuple4 = tuple([0,0,0,0,0,0,0,0,0])
end_state_tuple = tuple([0,0,0,0,0,0,0,0,0])
end_state_tuple2 = tuple([0,0,0,0,0,0,0,0,0])
end_state_tuple3 = tuple([0,0,0,0,0,0,0,0,0])
end_state_tuple4 = tuple([0,0,0,0,0,0,0,0,0])
root = None
path = None
visited_nodes = None

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

def is_valid_move(zero_index, direction):
    if direction == 'Up' and zero_index < 3:
        return False
    if direction == 'Down' and zero_index > 5:
        return False
    if direction == 'Left' and zero_index % 3 == 0:
        return False
    if direction == 'Right' and zero_index % 3 == 2:
        return False
    return True
        
def apply_action_for_current_state(direction: str, current_state: tuple):
    zero_idx = current_state.index(0)
    if is_valid_move(zero_idx, direction):
        d_action = MOVES[direction]
        current_state = list(current_state)
        current_state[zero_idx], current_state[zero_idx + d_action] = current_state[zero_idx + d_action], current_state[zero_idx]
        return tuple(current_state)
    return current_state

def is_empty_plain_text(plain_text_variable) -> bool:
    """Input: QPlainTextEdit"""
    return not plain_text_variable.toPlainText().strip()

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        app = uic.loadUi(CURRENT_DIRECTORY_PATH + "/complex_environment_GUI.ui", self)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.btnRandomInput.clicked.connect(self.random_input)
        self.cbbAlgorithm.addItems(["Search with no observation", "Search with partial observation"])
        self.btnSolve.clicked.connect(self.solve_click)
        self.txtSolveSpeedPerStep.setPlainText("1")
        self.speed_per_step = 1000#ms
        self.btnWriteToFile.clicked.connect(lambda: show_path_in_file(path))
        self.belief_set = []
        self.goal_set = []
        self.solution = []

    def random_input(self):
        global start_state_tuple, start_state_tuple2, start_state_tuple3, start_state_tuple4
        global end_state_tuple, end_state_tuple2, end_state_tuple3, end_state_tuple4
        
        numbers = random.sample(range(9), 9)
        start_state_tuple = tuple(numbers)
        self.cell1_start1.setPlainText(str(start_state_tuple[0]))
        self.cell2_start1.setPlainText(str(start_state_tuple[1]))
        self.cell3_start1.setPlainText(str(start_state_tuple[2]))
        self.cell4_start1.setPlainText(str(start_state_tuple[3]))
        self.cell5_start1.setPlainText(str(start_state_tuple[4]))
        self.cell6_start1.setPlainText(str(start_state_tuple[5]))
        self.cell7_start1.setPlainText(str(start_state_tuple[6]))
        self.cell8_start1.setPlainText(str(start_state_tuple[7]))
        self.cell9_start1.setPlainText(str(start_state_tuple[8]))
        
        numbers = random.sample(range(9), 9)
        start_state_tuple2 = tuple(numbers)
        self.cell1_start2.setPlainText(str(start_state_tuple2[0]))
        self.cell2_start2.setPlainText(str(start_state_tuple2[1]))
        self.cell3_start2.setPlainText(str(start_state_tuple2[2]))
        self.cell4_start2.setPlainText(str(start_state_tuple2[3]))
        self.cell5_start2.setPlainText(str(start_state_tuple2[4]))
        self.cell6_start2.setPlainText(str(start_state_tuple2[5]))
        self.cell7_start2.setPlainText(str(start_state_tuple2[6]))
        self.cell8_start2.setPlainText(str(start_state_tuple2[7]))
        self.cell9_start2.setPlainText(str(start_state_tuple2[8]))
        
        numbers = random.sample(range(9), 9)
        start_state_tuple3 = tuple(numbers)
        self.cell1_start3.setPlainText(str(start_state_tuple3[0]))
        self.cell2_start3.setPlainText(str(start_state_tuple3[1]))
        self.cell3_start3.setPlainText(str(start_state_tuple3[2]))
        self.cell4_start3.setPlainText(str(start_state_tuple3[3]))
        self.cell5_start3.setPlainText(str(start_state_tuple3[4]))
        self.cell6_start3.setPlainText(str(start_state_tuple3[5]))
        self.cell7_start3.setPlainText(str(start_state_tuple3[6]))
        self.cell8_start3.setPlainText(str(start_state_tuple3[7]))
        self.cell9_start3.setPlainText(str(start_state_tuple3[8]))
        
        numbers = random.sample(range(9), 9)
        start_state_tuple4 = tuple(numbers)
        self.cell1_start4.setPlainText(str(start_state_tuple4[0]))
        self.cell2_start4.setPlainText(str(start_state_tuple4[1]))
        self.cell3_start4.setPlainText(str(start_state_tuple4[2]))
        self.cell4_start4.setPlainText(str(start_state_tuple4[3]))
        self.cell5_start4.setPlainText(str(start_state_tuple4[4]))
        self.cell6_start4.setPlainText(str(start_state_tuple4[5]))
        self.cell7_start4.setPlainText(str(start_state_tuple4[6]))
        self.cell8_start4.setPlainText(str(start_state_tuple4[7]))
        self.cell9_start4.setPlainText(str(start_state_tuple4[8]))
        
        numbers = random.sample(range(9), 9)
        end_state_tuple = tuple(numbers)
        self.cell1_end1.setPlainText(str(end_state_tuple[0]))
        self.cell2_end1.setPlainText(str(end_state_tuple[1]))
        self.cell3_end1.setPlainText(str(end_state_tuple[2]))
        self.cell4_end1.setPlainText(str(end_state_tuple[3]))
        self.cell5_end1.setPlainText(str(end_state_tuple[4]))
        self.cell6_end1.setPlainText(str(end_state_tuple[5]))
        self.cell7_end1.setPlainText(str(end_state_tuple[6]))
        self.cell8_end1.setPlainText(str(end_state_tuple[7]))
        self.cell9_end1.setPlainText(str(end_state_tuple[8]))
        
        numbers = random.sample(range(9), 9)
        end_state_tuple2 = tuple(numbers)
        self.cell1_end2.setPlainText(str(end_state_tuple2[0]))
        self.cell2_end2.setPlainText(str(end_state_tuple2[1]))
        self.cell3_end2.setPlainText(str(end_state_tuple2[2]))
        self.cell4_end2.setPlainText(str(end_state_tuple2[3]))
        self.cell5_end2.setPlainText(str(end_state_tuple2[4]))
        self.cell6_end2.setPlainText(str(end_state_tuple2[5]))
        self.cell7_end2.setPlainText(str(end_state_tuple2[6]))
        self.cell8_end2.setPlainText(str(end_state_tuple2[7]))
        self.cell9_end2.setPlainText(str(end_state_tuple2[8]))
        
        numbers = random.sample(range(9), 9)
        end_state_tuple3 = tuple(numbers)
        self.cell1_end3.setPlainText(str(end_state_tuple3[0]))
        self.cell2_end3.setPlainText(str(end_state_tuple3[1]))
        self.cell3_end3.setPlainText(str(end_state_tuple3[2]))
        self.cell4_end3.setPlainText(str(end_state_tuple3[3]))
        self.cell5_end3.setPlainText(str(end_state_tuple3[4]))
        self.cell6_end3.setPlainText(str(end_state_tuple3[5]))
        self.cell7_end3.setPlainText(str(end_state_tuple3[6]))
        self.cell8_end3.setPlainText(str(end_state_tuple3[7]))
        self.cell9_end3.setPlainText(str(end_state_tuple3[8]))
        
        numbers = random.sample(range(9), 9)
        end_state_tuple4 = tuple(numbers)
        self.cell1_end4.setPlainText(str(end_state_tuple4[0]))
        self.cell2_end4.setPlainText(str(end_state_tuple4[1]))
        self.cell3_end4.setPlainText(str(end_state_tuple4[2]))
        self.cell4_end4.setPlainText(str(end_state_tuple4[3]))
        self.cell5_end4.setPlainText(str(end_state_tuple4[4]))
        self.cell6_end4.setPlainText(str(end_state_tuple4[5]))
        self.cell7_end4.setPlainText(str(end_state_tuple4[6]))
        self.cell8_end4.setPlainText(str(end_state_tuple4[7]))
        self.cell9_end4.setPlainText(str(end_state_tuple4[8]))

    def solve_click(self):
        global path
        algorithm_type = self.cbbAlgorithm.currentText()
        global start_state_tuple, start_state_tuple2, start_state_tuple3, start_state_tuple4
        global end_state_tuple, end_state_tuple2, end_state_tuple3, end_state_tuple4
        try:
            if all(not is_empty_plain_text(plain_text) for plain_text in [
                self.cell1_start1, self.cell4_start1, self.cell7_start1,
                self.cell2_start1, self.cell5_start1, self.cell8_start1,
                self.cell3_start1, self.cell6_start1, self.cell9_start1]):
                start_state_tuple = tuple([
                    int(self.cell1_start1.toPlainText()), int(self.cell2_start1.toPlainText()), int(self.cell3_start1.toPlainText()),
                    int(self.cell4_start1.toPlainText()), int(self.cell5_start1.toPlainText()), int(self.cell6_start1.toPlainText()),
                    int(self.cell7_start1.toPlainText()), int(self.cell8_start1.toPlainText()), int(self.cell9_start1.toPlainText())
                ])
                self.belief_set.append(start_state_tuple)
            
            if all(not is_empty_plain_text(plain_text) for plain_text in [
                self.cell1_start2, self.cell4_start2, self.cell7_start2,
                self.cell2_start2, self.cell5_start2, self.cell8_start2,
                self.cell3_start2, self.cell6_start2, self.cell9_start2]):
                start_state_tuple2 = tuple([
                    int(self.cell1_start2.toPlainText()), int(self.cell2_start2.toPlainText()), int(self.cell3_start2.toPlainText()),
                    int(self.cell4_start2.toPlainText()), int(self.cell5_start2.toPlainText()), int(self.cell6_start2.toPlainText()),
                    int(self.cell7_start2.toPlainText()), int(self.cell8_start2.toPlainText()), int(self.cell9_start2.toPlainText())
                ])
                self.belief_set.append(start_state_tuple2)
            
            if all(not is_empty_plain_text(plain_text) for plain_text in [
                self.cell1_start3, self.cell4_start3, self.cell7_start3,
                self.cell2_start3, self.cell5_start3, self.cell8_start3,
                self.cell3_start3, self.cell6_start3, self.cell9_start3]):
                start_state_tuple3 = tuple([
                    int(self.cell1_start3.toPlainText()), int(self.cell2_start3.toPlainText()), int(self.cell3_start3.toPlainText()),
                    int(self.cell4_start3.toPlainText()), int(self.cell5_start3.toPlainText()), int(self.cell6_start3.toPlainText()),
                    int(self.cell7_start3.toPlainText()), int(self.cell8_start3.toPlainText()), int(self.cell9_start3.toPlainText())
                ])
                self.belief_set.append(start_state_tuple3)
            
            if all(not is_empty_plain_text(plain_text) for plain_text in [
                self.cell1_start4, self.cell4_start4, self.cell7_start4,
                self.cell2_start4, self.cell5_start4, self.cell8_start4,
                self.cell3_start4, self.cell6_start4, self.cell9_start4]):
                start_state_tuple4 = tuple([
                    int(self.cell1_start4.toPlainText()), int(self.cell2_start4.toPlainText()), int(self.cell3_start4.toPlainText()),
                    int(self.cell4_start4.toPlainText()), int(self.cell5_start4.toPlainText()), int(self.cell6_start4.toPlainText()),
                    int(self.cell7_start4.toPlainText()), int(self.cell8_start4.toPlainText()), int(self.cell9_start4.toPlainText())
                ])
                self.belief_set.append(start_state_tuple4)
                
            if all(not is_empty_plain_text(plain_text) for plain_text in [
                self.cell1_end1, self.cell2_end1, self.cell3_end1,
                self.cell4_end1, self.cell5_end1, self.cell6_end1,
                self.cell7_end1, self.cell8_end1, self.cell9_end1]):
                end_state_tuple = tuple([
                    int(self.cell1_end1.toPlainText()), int(self.cell2_end1.toPlainText()), int(self.cell3_end1.toPlainText()),
                    int(self.cell4_end1.toPlainText()), int(self.cell5_end1.toPlainText()), int(self.cell6_end1.toPlainText()),
                    int(self.cell7_end1.toPlainText()), int(self.cell8_end1.toPlainText()), int(self.cell9_end1.toPlainText())
                ])
                self.goal_set.append(end_state_tuple)

            if all(not is_empty_plain_text(plain_text) for plain_text in [
                self.cell1_end2, self.cell2_end2, self.cell3_end2,
                self.cell4_end2, self.cell5_end2, self.cell6_end2,
                self.cell7_end2, self.cell8_end2, self.cell9_end2]):
                end_state_tuple2 = tuple([
                    int(self.cell1_end2.toPlainText()), int(self.cell2_end2.toPlainText()), int(self.cell3_end2.toPlainText()),
                    int(self.cell4_end2.toPlainText()), int(self.cell5_end2.toPlainText()), int(self.cell6_end2.toPlainText()),
                    int(self.cell7_end2.toPlainText()), int(self.cell8_end2.toPlainText()), int(self.cell9_end2.toPlainText())
                ])
                self.goal_set.append(end_state_tuple2)
                
            if all(not is_empty_plain_text(plain_text) for plain_text in [
                self.cell1_end3, self.cell2_end3, self.cell3_end3,
                self.cell4_end3, self.cell5_end3, self.cell6_end3,
                self.cell7_end3, self.cell8_end3, self.cell9_end3]):
                end_state_tuple3 = tuple([
                    int(self.cell1_end3.toPlainText()), int(self.cell2_end3.toPlainText()), int(self.cell3_end3.toPlainText()),
                    int(self.cell4_end3.toPlainText()), int(self.cell5_end3.toPlainText()), int(self.cell6_end3.toPlainText()),
                    int(self.cell7_end3.toPlainText()), int(self.cell8_end3.toPlainText()), int(self.cell9_end3.toPlainText())
                ])
                self.goal_set.append(end_state_tuple3)
                
            if all(not is_empty_plain_text(plain_text) for plain_text in [
                self.cell1_end4, self.cell2_end4, self.cell3_end4,
                self.cell4_end4, self.cell5_end4, self.cell6_end4,
                self.cell7_end4, self.cell8_end4, self.cell9_end4]):
                end_state_tuple4 = tuple([
                    int(self.cell1_end4.toPlainText()), int(self.cell2_end4.toPlainText()), int(self.cell3_end4.toPlainText()),
                    int(self.cell4_end4.toPlainText()), int(self.cell5_end4.toPlainText()), int(self.cell6_end4.toPlainText()),
                    int(self.cell7_end4.toPlainText()), int(self.cell8_end4.toPlainText()), int(self.cell9_end4.toPlainText())
                ])
                self.goal_set.append(end_state_tuple4)
        except ValueError:
            messagebox.showerror("Error", "Invalid input values!")
            return
              
        start_time = time.perf_counter()
        if len(self.belief_set) == 0:
            messagebox.showerror("Error", "Initial belief set is empty!")
            return
        if len(self.goal_set) == 0:
            messagebox.showerror("Error", "Initial goal set is empty!")
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

        solution = None
        number_of_opened_state = [0]
        if algorithm_type == "Search with no observation":
            solution = search_in_complex_environment_solve(self.belief_set, self.goal_set, is_partial_observation=False, number_of_opened_state = number_of_opened_state)
        else:
            solution = search_in_complex_environment_solve(self.belief_set, self.goal_set, is_partial_observation=True, number_of_opened_state = number_of_opened_state)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        self.txtSolveTime.setPlainText(f"{execution_time:.10f}(s)")
        print(f"Execution time: {execution_time}")
        print(f"Algorithm type: {algorithm_type}")
        print(f"Number of opened state: {number_of_opened_state}")
        if solution is None:
            messagebox.showinfo("Information", "No solutions found!")
            self.txtTotalStep.setPlainText("0")
            self.txtStep.setPlainText("0")
            path = None
            print("Size of path: 0")
        else:
            print(f"Size of path: {len(solution)}")
            path1, path2, path3, path4 = [], [], [], []
            current_state1, current_state2, current_state3, current_state4 = None, None, None, None
            if start_state_tuple != tuple([0,0,0,0,0,0,0,0,0]):
                current_state1 = start_state_tuple
            if start_state_tuple2 != tuple([0,0,0,0,0,0,0,0,0]):
                current_state2 = start_state_tuple2
            if start_state_tuple3 != tuple([0,0,0,0,0,0,0,0,0]):
                current_state3 = start_state_tuple3
            if start_state_tuple4 != tuple([0,0,0,0,0,0,0,0,0]):
                current_state4 = start_state_tuple4
            for action in solution:
                if current_state1 != None:
                    current_state1 = apply_action_for_current_state(action, current_state1)
                    path1.append(current_state1)
                if current_state2 != None:
                    current_state2 = apply_action_for_current_state(action, current_state2)
                    path2.append(current_state2)
                if current_state3 != None:
                    current_state3 = apply_action_for_current_state(action, current_state3)
                    path3.append(current_state3)
                if current_state4 != None:
                    current_state4 = apply_action_for_current_state(action, current_state4)
                    path4.append(current_state4)
            for sub_path in [path1, path2, path3, path4]:
                self.solution.append(sub_path)
            self.play_solution()
        
    def play_solution(self):
        self.step = 0
        self.timer = QtCore.QTimer()
        print(self.solution)
        self.timer.timeout.connect(self.update_step)
        self.timer.start(self.speed_per_step)
    def update_cell(self, cell, value):
        if value == 0:
            cell.setPlainText(" ")
        else:
            cell.setPlainText(str(value))
    def update_step(self):
        first_none_empty_solution = None
        for sub_solution in self.solution:
            if sub_solution != []:
                first_none_empty_solution = sub_solution
                break
        self.txtTotalStep.setPlainText(str(len(first_none_empty_solution)))
        if self.step < len(first_none_empty_solution):
            if self.solution[0] != []:
                e = self.solution[0][self.step]
                self.update_cell(self.cell1_result1, e[0])
                self.update_cell(self.cell2_result1, e[1])
                self.update_cell(self.cell3_result1, e[2])
                self.update_cell(self.cell4_result1, e[3])
                self.update_cell(self.cell5_result1, e[4])
                self.update_cell(self.cell6_result1, e[5])
                self.update_cell(self.cell7_result1, e[6])
                self.update_cell(self.cell8_result1, e[7])
                self.update_cell(self.cell9_result1, e[8])
            
            if self.solution[1] != []:
                e = self.solution[1][self.step]
                self.update_cell(self.cell1_result2, e[0])
                self.update_cell(self.cell2_result2, e[1])
                self.update_cell(self.cell3_result2, e[2])
                self.update_cell(self.cell4_result2, e[3])
                self.update_cell(self.cell5_result2, e[4])
                self.update_cell(self.cell6_result2, e[5])
                self.update_cell(self.cell7_result2, e[6])
                self.update_cell(self.cell8_result2, e[7])
                self.update_cell(self.cell9_result2, e[8])
            
            if self.solution[2] != []:
                e = self.solution[2][self.step]
                self.update_cell(self.cell1_result3, e[0])
                self.update_cell(self.cell2_result3, e[1])
                self.update_cell(self.cell3_result3, e[2])
                self.update_cell(self.cell4_result3, e[3])
                self.update_cell(self.cell5_result3, e[4])
                self.update_cell(self.cell6_result3, e[5])
                self.update_cell(self.cell7_result3, e[6])
                self.update_cell(self.cell8_result3, e[7])
                self.update_cell(self.cell9_result3, e[8])
            
            if self.solution[3] != []:
                e = self.solution[3][self.step]              
                self.update_cell(self.cell1_result4, e[0])
                self.update_cell(self.cell2_result4, e[1])
                self.update_cell(self.cell3_result4, e[2])
                self.update_cell(self.cell4_result4, e[3])
                self.update_cell(self.cell5_result4, e[4])
                self.update_cell(self.cell6_result4, e[5])
                self.update_cell(self.cell7_result4, e[6])
                self.update_cell(self.cell8_result4, e[7])
                self.update_cell(self.cell9_result4, e[8])
            self.step += 1
            self.txtStep.setPlainText(str(self.step))
        else:
            self.timer.stop()

app = QApplication([])
window = MyApp()
window.show()
app.exec()
