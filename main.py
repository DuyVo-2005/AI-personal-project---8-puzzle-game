from PyQt6 import uic, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow
from tkinter import messagebox
import time
import random

from const import *
from dataStructures import *

start_state_tuple = tuple([0,0,0,0,0,0,0,0,0])
end_state_tuple = tuple([0,0,0,0,0,0,0,0,0])
root = None
path = None
visited_nodes = None

def uninformed_search(root: SearchNode, type: str):
    global visited_nodes
    open_list = OpenList(type)
    open_list.insert(root)
    close_list = CloseList()
    
    while not open_list.is_empty():
        n = open_list.pop()
        if close_list.lookup(n.state):
            continue
            
        close_list.insert(n.state)
        
        if is_goal(n.state):
            visited_nodes = close_list
            return extract_path(n)
        
        for action, new_state in succ(n.state):
            if not close_list.lookup(new_state):#
                new_node = make_node(n, action, new_state)
                open_list.insert(new_node)
    visited_nodes = close_list
    return None

def DeepLimitedSearch(node: SearchNode, depth_limit):
    stack = [(node, [])]  # Stack chứa (node, path)
    close_list = CloseList()
    global visited_nodes
    
    while stack:
        current_node, path = stack.pop()  # Lấy phần tử cuối cùng (LIFO)        
        if is_goal(current_node.state):
            visited_nodes = close_list
            return path        
        if close_list.lookup(current_node.state):
            continue       
        close_list.insert(current_node.state) # Đánh dấu đã xét
        
        if len(path) < depth_limit:  #mở rộng nếu chưa đạt depth_limit
            for action, new_state in succ(current_node.state):
                if not close_list.lookup(new_state):
                    new_node = make_node(current_node, action, new_state)
                    stack.append((new_node, path + [new_state]))
    visited_nodes = close_list
    return None
       
def IDS(root: SearchNode):
    max_depth = 1000000000000
    for depth in range(max_depth + 1):
        solution = DeepLimitedSearch(root, depth)#, solution, open_list, close_list)
        if solution != None:
            return solution
    return None
    

def UCS(root: SearchNode):
    global visited_nodes
    open_list = OpenList("UCS")
    open_list.insert(root)
    close_list = CloseList()
    
    while not open_list.is_empty():
        current_node = open_list.pop()[1] # index 0 là cost
        if is_goal(current_node.state):
            visited_nodes = close_list
            return extract_path(current_node)
        
        if close_list.lookup(current_node.state):
            continue
        
        close_list.insert(current_node.state)
        
        for action, new_state in succ(current_node.state):
            if not close_list.lookup(new_state):
                new_node = make_node(current_node, action, new_state)
                open_list.insert(new_node) 
    visited_nodes = close_list
    return None

def heuristic(state: tuple):
    global end_state_tuple
    h = 0
    for i in range(1, 9):
        x1, y1 = divmod(state.index(i), 3)
        x2, y2 = divmod(end_state_tuple.index(i), 3)
        h += abs(x1 - x2) + abs(y1 - y2)
    return h

def Greedy(root: SearchNode):
    global visited_nodes
    queue = deque()
    queue.append((root, heuristic(root.state)))
    close_list = CloseList()
    
    while queue:
        queue = deque(sorted(queue, key=lambda x: x[1])) 
        current_node, current_heuristic = queue.popleft()
        
        if is_goal(current_node.state):
            visited_nodes = close_list
            return extract_path(current_node)
        
        if close_list.lookup(current_node.state):
            continue
        
        close_list.insert(current_node.state)
        
        for action, new_state in succ(current_node.state):
            if not close_list.lookup(new_state):
                new_node = make_node(current_node, action, new_state)
                queue.append((new_node, heuristic(new_node.state)))
    visited_nodes = close_list
    return None

def A_start(root: SearchNode):
    # f(n) = g(n) + h(n) = node_cost + heristic
    global visited_nodes
    queue = deque()
    queue.append((root, root.g_cost + heuristic(root.state)))
    close_list = CloseList()
    
    while queue:
        queue = deque(sorted(queue, key=lambda x: x[1]))  
        current_node, current_cost = queue.popleft()# Lấy phần tử có path_cost nhỏ nhất
        
        if is_goal(current_node.state):
            visited_nodes = close_list
            return extract_path(current_node)
        
        if close_list.lookup(current_node.state):
            continue
        
        close_list.insert(current_node.state)
        
        for action, new_state in succ(current_node.state):
            if not close_list.lookup(new_state):
                new_node = make_node(current_node, action, new_state)
                queue.append((new_node, new_node.g_cost + heuristic(new_node.state)))
    visited_nodes = close_list
    return None

# IDA* tăng ngưỡng xét từ vd 0, 2, 4, 6 (mỗi lần xét chỉ lấy giá trị bé hơn hoặc bằng ngưỡng)
def IDA_star(root: SearchNode):
    def search(node: SearchNode, path: set, threshold):# Tìm kiếm theo DFS với giới hạn threshold
        f_cost = node.g_cost + heuristic(node.state)
        if f_cost > threshold:
            return f_cost, None
        if is_goal(node.state):
            return None, extract_path(node)
        min_threshold = float("inf")
        path.add(node.state)
        for action, new_state in succ(node.state):
            if new_state in path:
                continue  
            new_node = make_node(node, action, new_state)
            result, found_path = search(new_node, path.copy(), threshold)# Truyền bản sao của path
            if found_path:
                return None, found_path

            min_threshold = min(min_threshold, result)

        path.remove(node.state)# Xóa khỏi tập hợp khi quay lui
        return min_threshold, None# Trả về threshold mới nếu không tìm thấy lời giải

    threshold = root.g_cost + heuristic(root.state)
    while True:
        close_list = CloseList()
        new_threshold, path = search(root, close_list.set, threshold)
        if path:
            return path
        if new_threshold == float("inf"):# Không tìm thấy lời giải
            return None
        threshold = new_threshold
 
def simple_hill_climbing(root: SearchNode):
    current_node = root
    while True:
        if is_goal(current_node.state):
            return extract_path(current_node)
        neighbors = succ(current_node.state)
        if not neighbors:
            return None
        for action, state in neighbors:
            if heuristic(state) < heuristic(current_node.state):
                current_node = make_node(current_node, action, state)
                break
        else:
            return None

def steepest_ascent_hill_climbing(root: SearchNode):
    current_node = root
    while True:
        if is_goal(current_node.state):
            return extract_path(current_node)
        neighbors = succ(current_node.state)#Trả về (action, state)
        if not neighbors:
            return None
        best_neighbor = min(neighbors, key=lambda x: heuristic(x[1]))#Chọn hàng xóm tốt nhất theo heuristic nhỏ nhất
        if heuristic(best_neighbor[1]) >= heuristic(current_node.state):#Không tìm thấy trạng thái tốt hơn, dừng lại
            return None
        current_node = make_node(current_node, best_neighbor[0], best_neighbor[1])#Tạo node mới để lưu đường đi


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
                        for i in range(0, 9, 3):
                                f.write(f"\n{state[i]}, {state[i+1]}, {state[i+2]}")
                        f.write("\n")
                        f.write("-" * 10)
        f.write("\nClose list: ")
        if visited_nodes == None:
                f.write("\nNone")
        else:
                for state in visited_nodes.set:
                        for i in range(0, 9, 3):
                                f.write(f"\n{state[i]}, {state[i+1]}, {state[i+2]}")
                        f.write("\n")
                        f.write("-" * 10)
        messagebox.showinfo("Infomation", "Write to file successfully")
        
                        

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        app = uic.loadUi(CURRENT_DIRECTORY_PATH + "/GUI.ui", self)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.btnRandomInput.clicked.connect(self.random_input)
        self.btnLoadValue.clicked.connect(self.load_value)
        self.cbbAlgorithm.addItems(["BFS", "DFS", "UCS", "IDS", "Greedy", "A*", "IDA*", "Simple hill climbing", "Steepest ascent hill climbing"])
        self.btnSolve.clicked.connect(self.solve_click)
        self.txtSolveSpeedPerStep.setPlainText("1")
        self.speed_per_step = 1000#ms
        self.btnWriteToFile.clicked.connect(lambda: show_path_in_file(path))
        self.btnQuit.clicked.connect(self.close)
        
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
        # for i in range(9):
        #     end_state_tuple[i] = numbers[i]
        self.cell1_2.setPlainText(str(end_state_tuple[0]))
        self.cell2_2.setPlainText(str(end_state_tuple[1]))
        self.cell3_2.setPlainText(str(end_state_tuple[2]))
        self.cell4_2.setPlainText(str(end_state_tuple[3]))
        self.cell5_2.setPlainText(str(end_state_tuple[4]))
        self.cell6_2.setPlainText(str(end_state_tuple[5]))
        self.cell7_2.setPlainText(str(end_state_tuple[6]))
        self.cell8_2.setPlainText(str(end_state_tuple[7]))
        self.cell9_2.setPlainText(str(end_state_tuple[8]))
        
    def solve_click(self):
        global root, path
        algorithm_type = self.cbbAlgorithm.currentText()
        start_time = time.time()
        if root is None:
                messagebox.showerror("Error", "Please load values first!")
                return
        try:
            if int(float(self.txtSolveSpeedPerStep.toPlainText()) * 1000) >= 1:#ms
                self.speed_per_step = end_state_tuple = int(float(self.txtSolveSpeedPerStep.toPlainText()) * 1000)
            else:
                messagebox.showerror("Error", "Speed per step must above or equal 0.001s")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid speed per step")
            return
        
        solution = None
        if algorithm_type == "BFS" or algorithm_type == "DFS":
            solution = uninformed_search(root, algorithm_type)
        elif algorithm_type == "UCS":
            solution = UCS(root)
        elif algorithm_type == "IDS":
            solution = IDS(root)
        elif algorithm_type == "A*":
            solution = A_start(root)
        elif algorithm_type == "IDA*":
            solution = IDA_star(root)
        elif algorithm_type == "Greedy":
            solution = Greedy(root)
        elif algorithm_type == "Simple hill climbing":
            solution = simple_hill_climbing(root)
        elif algorithm_type == "Steepest ascent hill climbing":
            solution = steepest_ascent_hill_climbing(root)

        if solution is None:
                messagebox.showinfo("Information", "No solutions found!")
                self.txtTotalStep.setPlainText("0")
                self.txtStep.setPlainText("0")
                path = None
        else:
                self.play_solution(solution)
                path = solution
                self.txtTotalStep.setPlainText(str(len(solution)))
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
        global start_state_tuple, end_state_tuple, root
        try:
                start_state_tuple = tuple([
                int(self.cell1.toPlainText()), int(self.cell2.toPlainText()), int(self.cell3.toPlainText()),
                int(self.cell4.toPlainText()), int(self.cell5.toPlainText()), int(self.cell6.toPlainText()),
                int(self.cell7.toPlainText()), int(self.cell8.toPlainText()), int(self.cell9.toPlainText())]
                )

                end_state_tuple = tuple([
                int(self.cell1_2.toPlainText()), int(self.cell2_2.toPlainText()), int(self.cell3_2.toPlainText()),
                int(self.cell4_2.toPlainText()), int(self.cell5_2.toPlainText()), int(self.cell6_2.toPlainText()),
                int(self.cell7_2.toPlainText()), int(self.cell8_2.toPlainText()), int(self.cell9_2.toPlainText())
                ])

                root = make_node(None, None, start_state_tuple)

        except ValueError:
                messagebox.showerror("Error", "Invalid input values!")
        else:
                messagebox.showinfo("Notification", "Values loaded successfully!")

if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec()
