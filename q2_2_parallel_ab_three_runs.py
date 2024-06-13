import threading
import time
from samples import samples

player, opponent = 'x', 'o'
nodes_visited = 0  # global var so all threads can access


# is_moves() and evaluate() left as is
def is_moves_left(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                return True
    return False


def evaluate(b):
    for row in range(3):
        if b[row][0] == b[row][1] and b[row][1] == b[row][2]:
            if b[row][0] == player:
                return 10
            elif b[row][0] == opponent:
                return -10

    for col in range(3):
        if b[0][col] == b[1][col] and b[1][col] == b[2][col]:
            if b[0][col] == player:
                return 10
            elif b[0][col] == opponent:
                return -10

    if b[0][0] == b[1][1] and b[1][1] == b[2][2]:
        if b[0][0] == player:
            return 10
        elif b[0][0] == opponent:
            return -10

    if b[0][2] == b[1][1] and b[1][1] == b[2][0]:
        if b[0][2] == player:
            return 10
        elif b[0][2] == opponent:
            return -10

    return 0


def minimax(board, depth, is_max, alpha, beta):
    global nodes_visited
    nodes_visited += 1  # increment the node count

    score = evaluate(board)

    if score == 10:
        return score  # max wins

    if score == -10:
        return score  # min wins

    if not is_moves_left(board):
        return 0  # tie

    if is_max:
        best = float('-inf')

        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = player
                    best = max(best, minimax(board, depth + 1, not is_max, alpha, beta))
                    board[i][j] = '_'
                    alpha = max(alpha, best)

                    if beta <= alpha:
                        break

        return best

    else:
        best = float('inf')

        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = opponent
                    best = min(best, minimax(board, depth + 1, not is_max, alpha, beta))
                    board[i][j] = '_'
                    beta = min(beta, best)

                    if beta <= alpha:
                        break

        return best


def find_best_move(board):
    best_val = float('-inf')
    best_move = (-1, -1)
    alpha = float('-inf')
    beta = float('inf')

    for i in range(3):
        for j in range(3):

            if board[i][j] == '_':

                board[i][j] = player

                move_val = minimax(board, 0, False, alpha, beta)

                board[i][j] = '_'

                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
                    alpha = max(alpha, best_val)

    return best_move


def display_board(board):
    for row in board:
        print(" ".join(row))
    print()


def parallel_minimax(board, depth, is_max, alpha, beta, result, lock):
    global nodes_visited
    nodes_visited += 1  # increment the node count

    score = evaluate(board)

    if score == 10:
        result[0] = score  # max wins
        return

    if score == -10:
        result[0] = score  # min wins
        return

    if not is_moves_left(board):
        result[0] = 0  # tie
        return

    if is_max:
        best = float('-inf')

        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = player
                    parallel_minimax(board, depth + 1, not is_max, alpha, beta, result, lock)
                    best = max(best, result[0])
                    board[i][j] = '_'
                    alpha = max(alpha, best)

                    if beta <= alpha:
                        break

        result[0] = best

    else:
        best = float('inf')

        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = opponent
                    parallel_minimax(board, depth + 1, not is_max, alpha, beta, result, lock)
                    best = min(best, result[0])
                    board[i][j] = '_'
                    beta = min(beta, best)

                    if beta <= alpha:
                        break

        result[0] = best


def find_best_move_parallel(board):
    best_val = float('-inf')
    best_move = (-1, -1)
    alpha = float('-inf')
    beta = float('inf')
    result = [float('-inf')]
    lock = threading.Lock()

    threads = []

    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':

                board[i][j] = player

                new_board = [row[:] for row in board]  # Create a copy of the board
                thread = threading.Thread(target=parallel_minimax, args=(new_board, 0, False, alpha, beta, result, lock))
                threads.append(thread)
                thread.start()

                board[i][j] = '_'

    for thread in threads:
        thread.join()

    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':

                board[i][j] = player

                move_val = result[0]

                board[i][j] = '_'

                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
                    alpha = max(alpha, best_val)

    return best_move


# Driver code
if __name__ == "__main__":

    for idx, sample in enumerate(samples, 1):
        nodes_visited = 0

        start_time = time.time()
        opt_move = find_best_move_parallel(sample)
        end_time = time.time()

        display_board(sample)
        print("Optimal move:", opt_move)
        print("Nodes evaluated:", nodes_visited)
        print(f"Time taken: {end_time - start_time:.4f} seconds")
        print("-" * 30)
