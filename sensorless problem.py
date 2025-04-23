from collections import deque
import random

ACTIONS = ['Up', 'Down', 'Left', 'Right']

MOVE = {
    'Up': -3, 'Down': 3, 'Left': -1, 'Right': 1
}

def valid_actions(state):
    index = state.index(0)
    row, col = divmod(index, 3)
    actions = []
    if row > 0: actions.append('Up')
    if row < 2: actions.append('Down')
    if col > 0: actions.append('Left')
    if col < 2: actions.append('Right')
    return actions

# apply action in state
def apply_action(state, action):
    zero_index = state.index(0)
    swap_index = zero_index + MOVE[action]
    
    if swap_index < 0 or swap_index >= 9:#Không hợp lệ nếu vị trí cần đổi ngoài lưới
        return None
    #Đang ở biên không được di chuyển ra ngoài
    if action == 'Left' and zero_index % 3 == 0:
        return None
    if action == 'Right' and zero_index % 3 == 2:
        return None
    state = list(state)
    state[zero_index], state[swap_index] = state[swap_index], state[zero_index]
    return tuple(state)

#ACTIONS(b): hội các hành động hợp lệ của mỗi trạng thái #sensorless_actions
def actions_b(belief):
    all_valid = [set(valid_actions(s)) for s in belief]
    return set.union(*all_valid)

# RESULT(s)(b, a)
def results(belief, action):
    new_belief = set()
    for s in belief:
        new_state = apply_action(s, action)#result_p = apply_action: hành động trong môi trường vật lý
        if new_state:
            new_belief.add(new_state)
    return new_belief


def goal_test(belief, goal):
    return all(s == goal for s in belief)#Kiểm tra belief toàn goal

goal_state = (1,2,3,4,5,6,7,8,0)

#1. Initial state: all p state
# s1 = (1,2,3,
#       4,5,6,
#       0,7,8)
# s2 = (1,2,3,
#       4,5,6,
#       7,0,8)
# s3 = (1,2,3,
#       0,5,6,
#       4,7,8)
#belief = set([s1])
#belief = set([s1, s2, s3])
#belief = set([s1, s2])

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

belief = generate_unique_puzzle_states(1000)

path = []
while not goal_test(belief, goal_state):
    #2. Possible actions
    acts = actions_b(belief)
    if not acts:
        print("Không thể tiếp tục!")
        break
    
    a = list(acts)[0]
    path.append(a)
    #3. Transition model
    belief = results(belief, a)

print("Hành động đã chọn:", path)
print("Belief cuối cùng:")
for s in belief:
    print(s)

#áp dụng duyệt sâu, rộng:
#từ b' xét duyệt sâu (duyệt rộng) ra trạng thái đích [càng nhiều b' tính ra -> thành công càng cao]