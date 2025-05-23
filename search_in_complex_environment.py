#Kết quả là 1 cây tìm kiếm (mỗi nhánh là áp 1 hành động lên một tập trạng thái)
#Trạng thái trùng trong tập thì bỏ
#Nhìn thấy 1 phần biết được vài ô

#Tìm kiếm trong môi trường phức tạp:
#Search with partial observation
#Search with no observation
#AND OR search #8 puzzle là môi trường xác định có thể áp dụng nhưng không có phần else

from collections import deque
from dataStructures import SearchNode

MOVES = {
    'Up': -3,
    'Down': 3,
    'Left': -1,
    'Right': 1
}

# #Tập trạng thái mục tiêu
# goal_set = [
#     (1, 2, 3,
#      4, 5, 6,
#      7, 8, 0),
#     (1, 2, 3,
#      4, 0, 6,
#      7, 5, 8)
# ]
# #Tập trạng thái khởi tạo
# initial_belief_set = [
#     (1, 2, 3,
#      4, 5, 6,
#      0, 7, 8),
#     (1, 2, 3,
#      4, 5, 6,
#      7, 0, 8),
#     (1, 2, 3,
#      4, 5, 6,
#      7, 8, 0),
#     (1, 2, 3,
#      4, 0, 6,
#      7, 5, 8),
# #     # (8, 7, 6,
# #     #  5, 4, 3,
# #     #  2, 1, 0)
# ]
max_depth = 100000

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
def move(state: tuple, direction: str):
    zero_index = state.index(0)
    if not is_valid_move(zero_index, direction):
        return None
    new_index = zero_index + MOVES[direction]
    new_state = list(state)
    new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
    return tuple(new_state)
def apply_action_to_belief(belief: list, action: str, goal_set: list, is_partial_observation: bool = False):
    result = []
    visited = set()
    for state in belief:
        new_state = move(state, action)
        if new_state is None:
            new_state = state#giữ nguyên trạng thái nếu không di chuyển được
        if new_state not in visited:
            visited.add(new_state)
            if is_partial_observation:
                if is_near_goal(new_state, goal_set):                  
                    result.append(new_state)
            else:                
                result.append(new_state)
    return result
def is_goal_belief_set(belief: list, goal_set: list) -> bool:
    return all(state in goal_set for state in belief)
# def is_near_goal(state):
#        return state[:3] == (1,2,3)
def is_near_goal(state:tuple, goal_set:list) -> bool:
        return state[:3] == goal_set[0][:3]
def print_state(state):
    for i in range(0, 9, 3):
        print(state[i], state[i+1], state[i+2])
def search_in_complex_enviroment(initial_belief_set: list, goal_set: list, number_of_opened_state: list, is_partial_observation: bool = False) -> list:
    """Return actions set from start state to goal state"""
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
        if is_goal_belief_set(belief_set, goal_set):
            print("Reached goal set!")
            number_of_opened_state[0] = len(visited)
            return actions
        for action in MOVES:
            new_belief = apply_action_to_belief(belief_set, action, goal_set, is_partial_observation)
            if new_belief:
                queue.append((new_belief, actions + [action]))
        depth += 1
    number_of_opened_state[0] = len(visited)
    return None

def search_in_complex_environment_solve(initial_belief_set: list, goal_set: list, number_of_opened_state: list, is_partial_observation: bool = False) -> list:
    plan = search_in_complex_enviroment(initial_belief_set, goal_set, number_of_opened_state, is_partial_observation)
    print("Plan to reach goal:", plan)
    return plan

# number_of_opened_state = 0
# search_in_complex_environment_solve(initial_belief_set, goal_set, is_partial_observation = False, number_of_opened_state=number_of_opened_state)