# MOVES = {
#     'Up': -3,
#     'Down': 3,
#     'Left': -1,
#     'Right': 1
# }
# def apply_action_for_current_state(action: str, current_state: tuple):
#     action = MOVES[action]
#     current_state = list(current_state)
#     zero_idx = current_state.index(0)
#     current_state[zero_idx], current_state[zero_idx + action] = current_state[zero_idx + action], current_state[zero_idx]
#     return tuple(current_state)
# print(apply_action_for_current_state("Down", (1,2,3,0,4,5,6,7,8)))

# path = [[1,2,3,4,5], [5,6,7,8,9]]
# print(path[1][4])

# class A:
#     def __init__(self):
#         self.a = 2
#     def c(self):
#         self.a += 1
# b = A()
# b.c()
# print(b.a)
a = []
b = (1,2)
c = (3,4)
a.append(b)
a.append(c)
print(a)