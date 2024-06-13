from samples import samples

player, opponent = 'x', 'o'
nodes_visited = 0  # global variable to count the number of nodes visited


def is_moves_left(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                return True
    return False


def evaluate(b):
    for row in range(3):
        if b[row][0] == b[row][1] == b[row][2]:
            if b[row][0] == player:
                return 10
            elif b[row][0] == opponent:
                return -10

    for col in range(3):
        if b[0][col] == b[1][col] == b[2][col]:
            if b[0][col] == player:
                return 10
            elif b[0][col] == opponent:
                return -10

    if b[0][0] == b[1][1] == b[2][2]:
        if b[0][0] == player:
            return 10
        elif b[0][0] == opponent:
            return -10

    if b[0][2] == b[1][1] == b[2][0]:
        if b[0][2] == player:
            return 10
        elif b[0][2] == opponent:
            return -10

    return 0


def evaluate_heuristic(b):
    player_score = 0
    opponent_score = 0

    # Rows and Columns
    for i in range(3):
        if b[i][0] == b[i][1] == player or b[i][0]==b[i][2]==player:
            player_score += 1
        elif b[i][0] == b[i][1] == opponent or b[i][0]==b[i][2]==opponent:
            opponent_score += 1

        if b[0][i] == b[1][i] == player or b[0][i]==b[2][i]==player:
            player_score += 1
        elif b[0][i] == b[1][i] == opponent or b[0][i]==b[2][i]==opponent:
            opponent_score += 1

    # Diagonals
    if b[0][0] == b[1][1] == player or b[0][0]==b[2][2]==player:
        player_score += 1
    elif b[0][0] == b[1][1] == opponent or b[0][0]==b[2][2]==opponent:
        opponent_score += 1

    if b[0][2] == b[1][1] == player:
        player_score += 1
    elif b[0][2] == b[1][1] == opponent:
        opponent_score += 1

    return player_score - opponent_score


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

    # Use heuristic for non-terminal states
    if depth >= 2:
        return evaluate_heuristic(board)

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


# Driver code
if __name__ == "__main__":

    for idx, sample in enumerate(samples, 1):
        nodes_visited = 0

        opt_move = find_best_move(sample)

        display_board(sample)
        print("Optimal move:", opt_move)
        print("Nodes evaluated:", nodes_visited)
