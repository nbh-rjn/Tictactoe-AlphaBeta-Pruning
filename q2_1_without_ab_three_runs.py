from samples import samples

player, opponent = 'x', 'o'


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


def minimax(board, depth, is_max):
    score = evaluate(board)
    global nodes_visited
    nodes_visited += 1

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
                    best = max(best, minimax(board, depth + 1, not is_max))
                    board[i][j] = '_'

        return best

    else:
        best = float('inf')

        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = opponent
                    best = min(best, minimax(board, depth + 1, not is_max))
                    board[i][j] = '_'

        return best


def find_best_move(board):
    best_val = float('-inf')
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):

            if board[i][j] == '_':

                board[i][j] = player

                move_val = minimax(board, 0, False)

                board[i][j] = '_'

                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    # print("The value of the best Move is :", best_val)
    print()
    return best_move


def display_board(board):
    for row in board:
        print(" ".join(row))
    print()


# Driver code
if __name__ == "__main__":

    for sample in samples:
        nodes_visited = 0
        opt_move = find_best_move(sample)

        display_board(sample)
        print("optimal move: ", opt_move)
        print("nodes evaluated: ", nodes_visited)
