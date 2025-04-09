import random

def order_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    
    child = [None] * size
    
    child[start:end + 1] = parent1[start:end + 1]
    
    p2_index = 0
    for i in range(size):
        if child[i] is None:
            while parent2[p2_index] in child:
                p2_index += 1
            child[i] = parent2[p2_index]
    
    return child

parent1 = [1, 2, 3, 4, 5, 6, 7, 8, 0]
parent2 = [1, 3, 4, 8, 0, 2, 7, 6, 5]

offspring = order_crossover(parent1, parent2)
print("Parent 1:", parent1)
print("Parent 2:", parent2)
print("Offspring:", offspring)

