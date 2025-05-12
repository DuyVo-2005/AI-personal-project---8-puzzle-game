def backtracking_search(board:list, pos: int, used, goal, path: list):
    """_summary_

    Args:
        board (list): _description_
        pos (int): _description_
        element pos idx
        0 1 2
        3 4 5
        6 7 8
        used (_type_): _description_
        goal (int): 
        
        path (list): _description_
    """
    if pos == 9:
        if board == goal:
            print("Found goal state:")
            for board in path:
                print_board(board)
        return

    for num in range(9):
        if not used[num]:
            board[pos] = num
            used[num] = True
            path.append(board[:])#bản sao
            backtracking_search(board, pos + 1, used, goal, path)
            path.pop()
            used[num] = False
            board[pos] = -1#quay lui

def print_board(board):
    for i in range(0, 9, 3):
        print(board[i:i+3])
    print()
    print("--------------------")
    print()
        #print(board)

initial_board = [-1] * 9
used = [False] * 9#ràng buộc không trùng giá trị trong trạng thái
# goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
goal_state = [6, 7, 8, 0, 1, 2, 3, 4, 5]
path = []

backtracking_search(initial_board, 0, used, goal_state, path)
