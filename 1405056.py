import math
player = 'x'
opponent = 'o'
board_size = 3


def is_move_left(board):
    for x in range(board_size):
        for y in range(board_size):
            if board[x][y] == '.':
                return True
    return False


def heuristic_score(board):
    diagonal_mismatch = 0
    for row in range(board_size):
        count = 0
        for col in range(board_size-1):
            if board[row][col] == board[row][col + 1]:
                count += 1
        if count == board_size - 1:
            if board[row][0] == player:
                return 5
            elif board[row][0] == opponent:
                return -5

    for col in range(board_size):
        count = 0
        for row in range(board_size-1):
            if board[row][col] == board[row + 1][col]:
                count += 1
        if count == board_size - 1:
            if board[0][col] == player:
                return 5
            elif board[0][col] == opponent:
                return -5

    diagonal_one = [(x, y) for x in range(board_size) for y in range(board_size) if x == y]
    diagonal_two = [(x, y) for x in range(board_size) for y in range(board_size) if x + y == board_size - 1]

    refer_d_one = diagonal_one.pop(0)
    for pos in diagonal_one:
        if board[pos[0]][pos[1]] != board[refer_d_one[0]][refer_d_one[1]]:
            diagonal_mismatch = 1
            break
    if diagonal_mismatch == 0:
        if board[0][0] == player:
            return 5
        elif board[0][0] == opponent:
            return -5

    refer_d_two = diagonal_two.pop(0)
    diagonal_mismatch = 0
    for pos in diagonal_two:
        if board[pos[0]][pos[1]] != board[refer_d_two[0]][refer_d_two[1]]:
            diagonal_mismatch = 1
            break
    if diagonal_mismatch == 0:
        if board[0][2] == player:
            return 5
        elif board[0][2] == opponent:
            return -5
    return 0


def mini_max(board, depth, isMax):
    score = heuristic_score(board)

    global number_of_nodes
    # winner --> maximizer or minimizer
    if score == 5 or score == -5:
        # number_leaf_nodes += 1
        # print(score)
        return score
    # tie
    if not is_move_left(board):
        return 0
    if isMax:
        best = -9999
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] == '.':
                    board[i][j] = player
                    number_of_nodes += 1
                    best = max(best, mini_max(board, depth + 1, not isMax))
                    board[i][j] = '.'
        return best
    else:
        best = 9999
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] == '.':
                    board[i][j] = opponent
                    number_of_nodes += 1
                    best = min(best, mini_max(board, depth + 1, not isMax))
                    board[i][j] = '.'
        return best


def print_board(board, player_sign):
    if player_sign == 'x':
        print("Player 1 moves:")
    elif player_sign == 'o':
        print("Computer moves:")
    for i in range(board_size):
        for j in range(board_size):
            print(board[i][j], end="")
        print()
    print()


def convert_2d_to_1d(board):
    board_1D = []
    for i in range(board_size):
        for j in range(board_size):
            board_1D.append(board[i][j])
    return board_1D


def free_moves(board):
    moves = []
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == '.':
                moves.append((i, j))
    return moves


def best_move(board):
    best = -9999
    best_moves = (-1, -1)
    global number_of_nodes
    game_over = False
    while not game_over:
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] == '.':
                    # print((i, j))
                    board[i][j] = opponent
                    number_of_nodes += 1
                    new_best = mini_max(board, 0, True)
                    board[i][j] = '.'
                    if new_best > best:
                        best = new_best
                        best_moves = (i, j)
        print("best move: " + str(best_moves))
        board[best_moves[0]][best_moves[1]] = opponent
        best = -9999
        best_moves = (-1, -1)
        print_board(board, opponent)
        print("Explored nodes for this move: " + str(number_of_nodes))
        number_of_nodes = 0
        score = heuristic_score(board)
        print("score: " + str(score))
        if score == -5:
            game_over = True
            print("Computer wins!!!")
            break

        elif score == 0 and '.' not in convert_2d_to_1d(board):
            game_over = True
            print([[board[x][y] for x in range(board_size)] for y in range(board_size)])
            print("Draw!!!")
            break

        print("Please enter sign:")
        user_input_x = int(input())
        user_input_y = int(input())
        while board[user_input_x][user_input_y] != '.':
            user_input_x = int(input())
            user_input_y = int(input())
        board[user_input_x][user_input_y] = player
        print_board(board, player)
        score = heuristic_score(board)
        print("score: " + str(score))
        if score == 5:
            game_over = True
            print("Player 1 wins!!!")

        elif score == 0 and '.' not in convert_2d_to_1d(board):
            game_over = True
            print([[board[x][y] for x in range(board_size)] for y in range(board_size)])
            print("Draw!!!")


min_val = -math.inf
max_val = math.inf
number_of_nodes_abp = 0


def mini_max_with_pruning(board, depth, is_Max, alpha, beta):
    score = heuristic_score(board)
    global number_of_nodes_abp
    if score == 5 or score == -5:
        return score
    if not is_move_left(board):
        return 0
    if is_Max:
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] == '.':
                    board[i][j] = player
                    number_of_nodes_abp += 1
                    alpha = max(alpha, mini_max_with_pruning(board, depth + 1, not is_Max, alpha, beta))
                    board[i][j] = '.'
                    if beta <= alpha:
                        return alpha
        return alpha
    else:
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] == '.':
                    board[i][j] = opponent
                    number_of_nodes_abp += 1
                    beta = min(beta, mini_max_with_pruning(board, depth + 1, not is_Max, alpha, beta))
                    board[i][j] = '.'
                    if beta <= alpha:
                        return beta
        return beta


def best_move_abp(board):
    best = -9999
    best_moves = (-1, -1)
    global number_of_nodes
    game_over = False
    while not game_over:
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] == '.':
                    # print((i, j))
                    board[i][j] = opponent
                    number_of_nodes += 1
                    new_best = mini_max_with_pruning(board, 0, True, min_val, max_val)
                    board[i][j] = '.'
                    if new_best > best:
                        best = new_best
                        best_moves = (i, j)
        print("best move: " + str(best_moves))
        board[best_moves[0]][best_moves[1]] = opponent
        best = -9999
        best_moves = (-1, -1)
        print_board(board, opponent)
        print("Explored nodes for this move: " + str(number_of_nodes))
        number_of_nodes = 0
        score = heuristic_score(board)
        print("score: " + str(score))
        if score == -5:
            game_over = True
            print("Computer wins!!!")
            break

        elif score == 0 and '.' not in convert_2d_to_1d(board):
            game_over = True
            print([[board[x][y] for x in range(board_size)] for y in range(board_size)])
            print("Draw!!!")
            break

        print("Please enter sign:")
        user_input_x = int(input())
        user_input_y = int(input())
        while board[user_input_x][user_input_y] != '.':
            user_input_x = int(input())
            user_input_y = int(input())
        board[user_input_x][user_input_y] = player
        print_board(board, player)
        score = heuristic_score(board)
        print("score: " + str(score))
        if score == 5:
            game_over = True
            print("Player 1 wins!!!")

        elif score == 0 and '.' not in convert_2d_to_1d(board):
            game_over = True
            # print([[board[x][y] for x in range(board_size)] for y in range(board_size)])
            print("Draw!!!")


def construct_board():
    return [['.' for x in range(board_size)] for y in range(board_size)]


board = construct_board()
# print(board)
number_of_nodes = 0
print("Without alpha-beta pruning:")
best_move(board)


board = construct_board()
number_of_nodes = 0
print("With alpha-beta pruning:")
best_move_abp(board)
