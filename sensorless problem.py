# tìm kiếm trong môi trường phức tạp:
# search with partial observation
# search with no observation
# AND OR search



from dataStructures import *
import random

def generate_unique_puzzle_states(n):   
    result = []
    while len(result) < n:
        nums = list(range(9))
        random.shuffle(nums)
        state = tuple(nums)
        if state not in result:          
            result.append(state)
    return result

#1. Initial state (s)
b = [(1,2,3,4,5,6,0,8,7),(1,2,3,4,5,6,0,8,7),(8,7,6,5,4,3,2,1,0),(7,8,0,1,2,3,5,6,4),(8,7,6,5,4,3,0,1,2)]

g = (1,2,3,4,5,6,7,8,0)

def is_valid(idx):
    return idx >= 0 and idx < 9
       
def apply_action(b):
       MOVES = {"U": -3, "D": 3, "L": -1, "R": 1}
       new_b = []
       for action in MOVES.keys():
              for state in b:
                    zero_idx = state.index(0)
                    swap_idx = zero_idx + MOVES[action]    
                    if is_valid(swap_idx):
                        new_state = list(state)
                        new_state[zero_idx], new_state[swap_idx] = new_state[swap_idx], new_state[zero_idx]
                        new_state = tuple(new_state)
                        if new_state not in new_b:
                                new_b.append(new_state)
                        new_b.append(new_state)
       return new_b
       
def goal_test(belief_set):
    return g == belief_set
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

def uninformed_search(belief_set: list, type: str):
    #global visited_nodes
    open_list = OpenList(type)
    open_list.insert(belief_set)
    close_list = []
    
    while not open_list.is_empty():
        current_b_set = open_list.pop()
        if not current_b_set in close_list:
            continue
            
        close_list.append(current_b_set)
        
        if goal_test(current_b_set):
            #visited_nodes = close_list
            #return extract_path(n)
            return "solve"
        
        new_b = apply_action(current_b_set)
        if not new_b in close_list:
            close_list.append(new_b)
        open_list.insert(new_b)
    #visited_nodes = close_list
    return None

solution = uninformed_search(b, "BFS")
if solution:
    print("Solution found:", solution)
else:
    print("No solution found")

       

# from collections import deque

# ACTIONS = ['Up', 'Down', 'Left', 'Right']

# MOVE = {
#     'Up': -3, 'Down': 3, 'Left': -1, 'Right': 1
# }

# def valid_actions(state):
#     index = state.index(0)
#     row, col = divmod(index, 3)
#     actions = []
#     if row > 0: actions.append('Up')
#     if row < 2: actions.append('Down')
#     if col > 0: actions.append('Left')
#     if col < 2: actions.append('Right')
#     return actions

# # apply action in state
# def apply_action(state, action):
#     zero_index = state.index(0)
#     swap_index = zero_index + MOVE[action]
    
#     if swap_index < 0 or swap_index >= 9:#Không hợp lệ nếu vị trí cần đổi ngoài lưới
#         return None
#     #Đang ở biên không được di chuyển ra ngoài
#     if action == 'Left' and zero_index % 3 == 0:
#         return None
#     if action == 'Right' and zero_index % 3 == 2:
#         return None
#     state = list(state)
#     state[zero_index], state[swap_index] = state[swap_index], state[zero_index]
#     return tuple(state)

# #ACTIONS(b): hội các hành động hợp lệ của mỗi trạng thái #sensorless_actions
# def actions_b(belief):
#     all_valid = [set(valid_actions(s)) for s in belief]
#     return set.union(*all_valid)

# # RESULT(s)(b, a)
# def results(belief, action):
#     new_belief = set()
#     for s in belief:
#         new_state = apply_action(s, action)#result_p = apply_action: hành động trong môi trường vật lý
#         if new_state:
#             new_belief.add(new_state)
#     return new_belief


# def goal_test(belief, goal):
#     return all(s == goal for s in belief)#Kiểm tra belief toàn goal

# goal_state = (1,2,3,4,5,6,7,8,0)

# #1. Initial state: all p state
# s1 = (1,2,3,
#       4,5,6,
#       0,7,8)
# s2 = (1,2,3,
#       4,5,6,
#       7,0,8)
# #s3 = (1,2,3,0,5,6,4,7,8)
# #belief = set([s1, s2, s3])
# belief = set([s1, s2])

# path = []
# # while not goal_test(belief, goal_state):
# #     #2. Possible actoins
# #     acts = actions_b(belief)
# #     if not acts:
# #         print("Không thể tiếp tục!")
# #         break
# #     # Chọn hành động đầu tiên có thể (tham lam)
# #     a = list(acts)[0]
# #     path.append(a)
# #     #3. Transition model
# #     belief = results(belief, a)

# print("Hành động đã chọn:", path)
# print("Belief cuối cùng:")
# for s in belief:
#     print(s)
