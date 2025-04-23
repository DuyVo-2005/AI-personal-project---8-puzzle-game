def is_valid(idx):
       return idx >= 0 and idx < 9

def is_near_goal(state):
    return state[:3] == end_state_tuple[:3]
   
end_state_tuple = (1,2,3,4,5,6,7,8,0)
b = [(8,7,6,5,4,3,2,1,0),(1,2,3,5,7,4,6,8,0)]

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
                        if (is_near_goal(new_state)):
                                new_b.append(new_state)
       return new_b

print(apply_action(b))