import random

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

initial_state = (1, 2, 3, 4, 5, 6, 0, 7, 8)

problem = {'initial': initial_state}
plan = AND_OR_SEARCH(problem)

print("Conditional Plan:")
print(plan)
