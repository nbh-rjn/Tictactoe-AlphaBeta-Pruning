import random

player, opponent = 'x', 'o'


def is_moves_left(b):
    for i in range(3):
        for j in range(3):
            if b[i][j] == '_':
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


def display_board(board):
    for row in board:
        print(" ".join(row))
    print()


def weak_player_move(board, random_tile):
    i, j = random.randint(0, 2), random.randint(0, 2)
    while board[i][j] != '_' or (i, j) == random_tile:
        i, j = random.randint(0, 2), random.randint(0, 2)
    board[i][j] = opponent


def play_game(board):
    random_tile = random.randint(0, 2), random.randint(0, 2)

    display_board(board)

    while is_moves_left(board) and not evaluate(board):
        # Player's move
        i, j = map(int, input("Enter your move (row[1-3] column[1-3]): ").split())
        while board[i - 1][j - 1] != '_' or (i < 1 or j < 1 or i > 3 or j > 3):
            print("Invalid move. Try again.")
            i, j = map(int, input("Enter your move (row[1-3] column[1-3]): ").split())
        board[i - 1][j - 1] = player

        display_board(board)

        if not is_moves_left(board) or evaluate(board):
            break

        # Weak player's move
        weak_player_move(board, random_tile)

        display_board(board)

    result = evaluate(board)
    if result == 10:
        print("you win")
    elif result == -10:
        print("weak player wins")
    else:
        print("it's a tie")


if __name__ == "__main__":

    game = [
        ['_', '_', '_'],
        ['_', '_', '_'],
        ['_', '_', '_']
    ]
    play_game(game)
