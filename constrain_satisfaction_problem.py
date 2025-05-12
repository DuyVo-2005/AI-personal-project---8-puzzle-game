# Tìm kiếm có ràng buộc

import math
import random

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
    

# end = (1,2,3,4,5,6,7,8,0)
# start = (-1,-1,-1,-1,-1,-1,-1,-1,-1)#không biết giá trị từng ô
    
# def test_search(end):#Tìm kiếm kiểm thử
#     visited = set()
#     start = None
#     while start != end:
#         new_state = generate_random_state()
#         if not is_violate_constrain(new_state) and new_state == end:
#             return "Solved"
#         visited.add(new_state)
        
def print_state(state):
    for i in range(0, 9, 3):
        print(state[i], state[i+1], state[i+2])
    print("-" * 10)          

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

test_search()
        
    
#print(len(generate_unique_can_solved_puzzle_states(math.factorial(9))))