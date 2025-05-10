#Kết quả là 1 cây tìm kiếm (mỗi nhánh là áp 1 hành động lên một tập trạng thái)
#Trạng thái trùng trong tập thì bỏ
#Nhìn thấy 1 phần biết được vài ô
#Search with no observation, search with partial observation
from collections import deque

from dataStructures import SearchNode
import random

MOVES = {
    'Up': -3,
    'Down': 3,
    'Left': -1,
    'Right': 1
}

#Tập trạng thái mục tiêu
goal_set = [
    (1, 2, 3,
     4, 5, 6,
     7, 8, 0),
    (1, 2, 3,
     4, 0, 6,
     7, 5, 8)
]
#Tập trạng thái khởi tạo
initial_belief_set = [
    (1, 2, 3,
     4, 5, 6,
     0, 7, 8),
    (1, 2, 3,
     4, 5, 6,
     7, 0, 8),
    (1, 2, 3,
     4, 5, 6,
     7, 8, 0),
    (1, 2, 3,
     4, 0, 6,
     7, 5, 8),
    (8,7,6,
     5,4,3,
     2,1,0   
    )
]
max_depth = 50

def is_valid_move(blank_index, direction):
    if direction == 'Up' and blank_index < 3:
        return False
    if direction == 'Down' and blank_index > 5:
        return False
    if direction == 'Left' and blank_index % 3 == 0:
        return False
    if direction == 'Right' and blank_index % 3 == 2:
        return False   
    return True
def move(state, direction):
    zero_index = state.index(0)
    if not is_valid_move(zero_index, direction):
        return None
    new_index = zero_index + MOVES[direction]
    new_state = list(state)
    new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
    return tuple(new_state)
def apply_action_to_belief(belief, action, is_partial_observation: bool = False):
    result = []
    visited = set()
    for state in belief:
        new_state = move(state, action)
        if new_state is None:
            new_state = state#giữ nguyên trạng thái nếu không di chuyển được
        if new_state not in visited:
            visited.add(new_state)
            if is_partial_observation:
                if is_near_goal(new_state):                  
                    result.append(new_state)
            else:                
                result.append(new_state)
    return result
def is_goal_belief_set(belief):
    return all(state in goal_set for state in belief)
def is_near_goal(state):
       return state[:3] == (1,2,3)
def print_state(state):
    for i in range(0, 9, 3):
        print(state[i], state[i+1], state[i+2])
def search_in_complex_enviroment(initial_belief_set: list, is_partial_observation: bool = False):
    queue = deque()
    visited = set()
    queue.append((initial_belief_set, []))
    depth = 0
    while queue and depth < max_depth:
        belief_set, actions = queue.popleft()
        frozen_belief_set = frozenset(belief_set)# set add set lỗi unhashable (do set có thể thay đổi thứ tự)
        if frozen_belief_set in visited:
            continue
        visited.add(frozen_belief_set)
        print("=====================")
        print(f"Actions: {actions}\n")
        print(f"Belief set (size={len(belief_set)}):")
        for state in belief_set:
            print_state(state)
            print("----")
        if is_goal_belief_set(belief_set):
            print("Reached goal set!")
            return actions
        for action in MOVES:
            new_belief = apply_action_to_belief(belief_set, action, is_partial_observation)
            if new_belief:
                queue.append((new_belief, actions + [action]))
        depth += 1
    return None

#8 puzzle là môi trường xác định có thể áp dụng nhưng không có phần else
MAX_DEPTH = 100
def AND_OR_graph_search(root: SearchNode):
    """
    Returns: conditional_plan or None
    """
    return OR_search(root.state, [], 0)

def AND_search(states: list, path: list, depth: int):
    if depth > MAX_DEPTH:
        return None
    plans = []
    for state in states:
        if state in path:# Tránh lặp vô hạn
            return None
        plan_i = OR_search(state, path, depth + 1)# + [state])#Truyền path mở rộng
        if plan_i == None:
            return None
        plans.append(plan_i)
    return plans

def Results(state: tuple, action: str):
    possible_results = [] 
    S1 = ApplyAction(state, action)
    if S1 != None:
        possible_results.append(S1)
    possible_results += generate_error_action(state)
    return possible_results

def generate_unique_puzzle_states(n):
    seen = set()
    result = []

    while len(result) < n:
        nums = list(range(9))
        random.shuffle(nums)
        state = tuple(nums)
        if state not in seen:
            seen.add(state)
            result.append(state)

    return result

#belief_set = generate_unique_puzzle_states(1000)
goal_set = generate_unique_puzzle_states(30)

def goal_test(state):
    return state in goal_set

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

def OR_search(state: tuple, path: list, depth: int):
    if depth > MAX_DEPTH:
        return None
    if goal_test(state):
        return []#empty plan = "Success"
    if state in path:
        return None
    for action, current_state in succ(state):
        plan = AND_search(Results(state, action), [state] + path, depth + 1)
        if plan != None:
            #return Plan(action, plan)
            return [action] + plan
    return None

def ApplyAction(state: tuple, action: str):
    """->tuple or None'"""
    """Apply action to state and return new state"""
    state = list(state)
    new_state = state.copy()
    idx = new_state.index(0)#vị trí ô trống
    row, col = idx // 3, idx % 3

    if action == "UP" and row > 0:
        swap_idx = idx - 3
    elif action == "DOWN" and row < 2:
        swap_idx = idx + 3
    elif action == "LEFT" and col > 0:
        swap_idx = idx - 1
    elif action == "RIGHT" and col < 2:
        swap_idx = idx + 1
    else:
        return None#hành động không hợp lệ

    #Thực hiện hoán đổi vị trí
    new_state[idx], new_state[swap_idx] = new_state[swap_idx], new_state[idx]
    return tuple(new_state)

def generate_error_action(state: tuple)->list:
    # error_action = []
    # error_action.append(state)
    # error_action.append(state[::-1])
    # return error_action
    #swap 2 ô
    state = list(state)
    indices = [i for i in range(len(state))]

    i, j = random.sample(indices, 2)
    state[i], state[j] = state[j], state[i]
    return [tuple(state)]

is_partial_observation = False
plan = search_in_complex_enviroment(initial_belief_set, is_partial_observation)
print("Plan to reach goal:", plan)
