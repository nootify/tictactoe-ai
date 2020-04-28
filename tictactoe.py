"""
Adapted from The Coding Train's Tic-Tac-Toe Minimax implementation

However, this version contains additional features such as:
# terminal compatibility
# randomized starting players
# randomized starting piece
"""
import random
import sys


def setup_board():
    n = 3
    grid = [[' '] * n for _ in range(n)]  # Create an n by n matrix
    return grid


def setup_players():
    ai = random.choice(['X', 'O'])
    human = 'X'
    if ai == human:
        human = 'O'
    return ai, human


def setup_scores(ai):
    if ai == 'X':
        return {'X': 10, 'O': -10, 'tie': 0}
    else:
        return {'X': -10, 'O': 10, 'tie': 0}


# Global variables
board = setup_board()
cpu, player = setup_players()
scores = setup_scores(cpu)


def player_move():
    # Get correctly formatted input from user and modify the board at the given position
    while True:
        user_input = input('Input coords: ').split(',')
        try:
            coords = (int(user_input[0]), int(user_input[1]))
        except (IndexError, ValueError):
            print("Error: Input must be given in the following form: x,y")
        else:
            if (coords[0] < -2 or coords[0] > 2) or (coords[1] < -2 or coords[1] > 2):
                print("Error: One or more indices given exceed board size.")
            elif board[coords[0]][coords[1]] != ' ':
                print("Error: This spot is already taken.")
            else:
                board[coords[0]][coords[1]] = player
                break


def cpu_move():
    move = None
    best_score = -sys.maxsize - 1
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = cpu
                score = minimax(board, 0, False)
                board[i][j] = ' '  # Undo changes to the board
                if score > best_score:
                    best_score = score
                    move = (i, j)

    if move is not None:
        board[move[0]][move[1]] = cpu


def minimax(board, depth, is_maximizing):
    result = check_winner()
    if result is not None:
        return scores[result]

    if is_maximizing:
        best_score = -sys.maxsize - 1
    else:
        best_score = sys.maxsize

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                if is_maximizing:
                    board[i][j] = cpu
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '  # Set back to empty spot
                    best_score = max(score, best_score)
                else:
                    board[i][j] = player
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '  # Set back to empty spot
                    best_score = min(score, best_score)

    return best_score


def empty(value):
    return value == ' '


def check_winner():
    winner = None

    # Horizontal
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and not empty(board[i][0]):
            winner = board[i][0]

    # Vertical
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and not empty(board[0][i]):
            winner = board[0][i]

    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] and not empty(board[0][0]):
        winner = board[0][0]
    if board[2][0] == board[1][1] == board[0][2] and not empty(board[2][0]):
        winner = board[2][0]

    open_spots = sum(row.count(' ') for row in board)

    if winner is None and open_spots == 0:
        return 'tie'
    else:
        return winner


def draw_board():
    print("-------------")
    for row in board:
        print(f"| {' | '.join(row)} |")
        print("-------------")


def draw_spacer():
    print()


def print_current_player(current_player):
    if current_player == cpu:
        print(f"Current player: {current_player} (CPU)")
    elif current_player == player:
        print(f"Current player: {current_player} (You)")
    else:
        raise ValueError("An unknown third player has joined the match.")


def print_winner(current_player):
    if current_player == cpu:
        print(f"The CPU won!")
    elif current_player == player:
        print(f"You won!")
    else:
        raise ValueError("An unknown third player has won the match.")


def main():
    current_player = random.choice([cpu, player])
    print(f"CPU: {cpu} | Player: {player}")

    if current_player == cpu:
        print_current_player(current_player)
        draw_board()
        draw_spacer()
        cpu_move()

    while True:
        current_player = player
        print_current_player(current_player)
        draw_board()
        player_move()
        draw_spacer()

        current_player = cpu
        cpu_move()
        print_current_player(current_player)
        draw_board()
        draw_spacer()

        result = check_winner()
        if result is not None:
            print("[Match Result]")
            draw_board()
            if result == 'tie':
                print("It's a tie!")
                break
            else:
                print_winner(result)
                break


if __name__ == "__main__":
    main()
