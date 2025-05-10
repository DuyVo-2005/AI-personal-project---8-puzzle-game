import random
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QGridLayout, QVBoxLayout
from PyQt6.QtCore import Qt

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
MAX_DEPTH = 30

def is_goal(state):
    return state == GOAL_STATE

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
    print(len(plan))
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

initial_state = (1, 2, 3, 4, 5, 6, 0, 7, 8)
problem = {'initial': initial_state}
plan = AND_OR_SEARCH(problem)
print("Conditional Plan:")
print_plan_tree(plan)

class PuzzleGUI(QWidget):
    def __init__(self, plan):
        super().__init__()
        self.plan = plan
        self.state = [1, 2, 3, 4, 5, 6, 0, 7, 8]  # initial state (editable)
        self.step = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('8 Puzzle AND-OR Graph Search')
        layout = QVBoxLayout()

        # Puzzle grid
        self.grid_layout = QGridLayout()
        self.buttons = []

        for i in range(9):
            btn = QPushButton(str(self.state[i]) if self.state[i] != 0 else '')
            btn.setFixedSize(60, 60)
            self.grid_layout.addWidget(btn, i // 3, i % 3)
            self.buttons.append(btn)

        layout.addLayout(self.grid_layout)

        # Tree plan output
        self.plan_text = QTextEdit()
        self.plan_text.setReadOnly(True)
        layout.addWidget(self.plan_text)

        # Next step button
        self.next_btn = QPushButton("Next Step")
        self.next_btn.clicked.connect(self.next_step)
        layout.addWidget(self.next_btn)

        self.setLayout(layout)

        # Show initial tree
        self.plan_text.setText(self.format_plan_tree(self.plan))

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

    def next_step(self):
        if isinstance(self.plan, list):
            action = self.plan[0]
            self.state = list(move(tuple(self.state), action))
            self.update_grid()
            self.plan = self.plan[1][0] if isinstance(self.plan[1], list) else self.plan[1]

    def update_grid(self):
        for i in range(9):
            val = self.state[i]
            self.buttons[i].setText(str(val) if val != 0 else '')

# problem = {'initial': (1, 2, 3, 4, 5, 6, 0, 7, 8)}
# plan = AND_OR_SEARCH(problem)

# app = QApplication(sys.argv)
# window = PuzzleGUI(plan)
# window.show()
# sys.exit(app.exec())
