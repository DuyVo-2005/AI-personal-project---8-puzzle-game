import random
from collections import defaultdict
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np

actions = ['Up', 'Down', 'Left', 'Right']

MOVES = {
    'Up': -3,
    'Down': 3,
    'Left': -1,
    'Right': 1
}

def is_goal(state: tuple, end_state_tuple: tuple) -> bool:
    return state == end_state_tuple

def is_valid_move(zero_index: int, direction: str) -> bool:
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

def heuristic(state: tuple, end_state_tuple: tuple) -> int:
    h = 0
    for i in range(1, 9):
        x1, y1 = divmod(state.index(i), 3)
        x2, y2 = divmod(end_state_tuple.index(i), 3)
        h += abs(x1 - x2) + abs(y1 - y2)
    return h

def reinforcement_learning_solve(start_state_tuple: tuple, end_state_tuple: tuple, Q_list: list) -> list:
    alpha = 0.1#Tốc độ học
    gamma = 0.95#Hệ số chiết khấu: agent đến phần thưởng là bao xa.
    epsilon = 0.9#Xác suất chọn hành động ngẫu nhiên (khai thác hoặc khám phá)
    min_epsilon = 0.01
    decay_rate = 0.995#Tốc độ giảm
    episodes = 10000# Số lượng tập huấn luyện

    #Biến thống kê
    rewards_per_episode = []
    steps_per_episode = []
    successes = []
    success_count = 0

    #B1. Khởi tạo Q-table và điền giá trị ban đầu là 0 cho các vị trí
    Q = defaultdict(lambda: {a: 0.0 for a in actions})# Bảng Q: {state: {action: value}}
    for episode in range(episodes):
        #B2. Bắt đầu 1 episode
        state = deepcopy(start_state_tuple)
        steps = 0
        total_reward = 0
        MAX_STEPS = 20000
        visited_states = set()#tránh lặp vô hạn hoặc quay lại trạng thái đã thăm trong cùng một tập huấn luyện
        while not is_goal(state, end_state_tuple) and steps < MAX_STEPS:
            valid_actions = [a for a in actions if is_valid_move(state.index(0), a)]
            if not valid_actions:
                break
            #B3. Tác nhân thực hiện hành động (Chọn hành động)
            if random.uniform(0, 1) < epsilon:#Khám phá
                action = random.choice(valid_actions)
            else:#Khai thác - Chọn theo kinh nghiệm đã được học
                #Chỉ chọn hành động tốt nhất trong danh sách hợp lệ
                action = max(valid_actions, key=lambda a: Q[state][a])
            next_state = move(state, action)
            #B4. Xác định phần thưởng
            #R (reward)max -> phần thưởng càng lớn càng gần đích
            if next_state is None:
                reward = -50#Hành động không hợp lệ -> phạt nặng
                max_new_q = 0
                p = 0.0001
            else:
                if next_state not in Q:
                    Q[next_state] = {a: 0.0 for a in actions}
                #B5. Tính lại Q-value cho trạng thái mới
                h_now = heuristic(state, end_state_tuple)
                h_next = heuristic(next_state, end_state_tuple)
                reward = 100 if is_goal(next_state, end_state_tuple) else (h_now - h_next)
                max_new_q = max(Q[next_state].values())
                p = 1 - heuristic(next_state, end_state_tuple) / 41#P(s,a,s’)): xác suất đi từ trạng thái s đến s' qua hành động a (0 -> 1 – dựa vào thực tế -> setup), với 41 là chi phí ước lượng hàm heristic lớn nhất
            #Cập nhật Q-value
            Q[state][action] += alpha * (reward + gamma * p * max_new_q - Q[state][action])
            total_reward += reward
            if next_state is None or next_state in visited_states:
                break
            visited_states.add(state)
            state = next_state
            steps += 1
        if is_goal(state, end_state_tuple):
            steps_per_episode.append(steps)
            success_count += 1
        else:
            steps_per_episode.append(MAX_STEPS)
        rewards_per_episode.append(total_reward)
        if (episode + 1) % 100 == 0:
            success_rate = success_count / 100
            successes.append(success_rate)
            success_count = 0
        #Giảm epsilon theo thời gian -> buộc agent bớt hành động khám phá
        epsilon = max(min_epsilon, epsilon * decay_rate)
        #B6. Kết thúc huấn luyện nếu thực hiện đủ episode lần học
    for state in Q:
        Q_list.append(f"{state}: {Q[state]}")
        print(f"{state}: {Q[state]}")
        Q_list.append(f"{state}: {Q[state]}")
    state = deepcopy(start_state_tuple)
    steps = 1
    solution = []
    while not is_goal(state, end_state_tuple) and steps < MAX_STEPS:
        print(f"Step {steps}: {state}")
        solution.append(state)
        if state not in Q:
            print("Trạng thái chưa được học.")
            break
        valid_actions = [a for a in actions if is_valid_move(state.index(0), a)]
        action = max(valid_actions, key=lambda a: Q[state][a])
        next_state = move(state, action)
        if next_state is None:
            break
        state = next_state
        steps += 1

    """ MỞ SOURCE ĐỂ VẼ BIỂU ĐỒ
    #avg_rewards = reward trung bình mỗi 100 episode
    avg_rewards = [np.mean(rewards_per_episode[i:i+100]) for i in range(0, len(rewards_per_episode), 100)]

    plt.figure(figsize=(14, 6))
    plt.plot(range(100, len(rewards_per_episode)+1, 100), avg_rewards, color='green', label='Reward trung bình mỗi 100 episode')
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.title("Reward trung bình mỗi 100 episode")
    plt.grid(True)
    plt.legend()
    plt.show()

    avg_steps = [np.mean(steps_per_episode[i:i+100]) for i in range(0, len(steps_per_episode), 100)]
    plt.figure(figsize=(14, 6))
    plt.plot(range(100, len(steps_per_episode)+1, 100), avg_steps, color='orange', label='Số bước trung bình mỗi 100 episode')
    plt.xlabel("Episode")
    plt.ylabel("Steps to goal")
    plt.title("Số bước trung bình mỗi 100 episode")
    plt.grid(True)
    plt.legend()
    plt.show()
    
    plt.figure(figsize=(14, 6))
    plt.plot(range(100, len(successes)*100 + 1, 100), successes, linewidth=3)
    plt.title('Tỷ lệ thành công mỗi 100 episode')
    plt.xlabel('Episode')
    plt.ylabel('Success Rate')
    plt.ylim(0, 1)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    #"""
    
    if is_goal(state, end_state_tuple):
        print(f"Đã đạt trạng thái đích sau {steps} bước.")
        solution.append(end_state_tuple)
        return solution
    else:
        print("Không đạt được trạng thái đích.")
        return None

end_state_tuple = (
    1, 2, 3,
    4, 5, 6,
    7, 8, 0
    )
# start_state_tuple = (
#     2,6,5,
#     0,8,7,
#     4,3,1
#     )
start_state_tuple = (
    0,1,2,
    4,5,3,
    7,8,6
    )
Q_list = []
print(reinforcement_learning_solve(start_state_tuple, end_state_tuple, Q_list))
