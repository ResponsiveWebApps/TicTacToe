from math import inf as infinity
from random import choice
import platform
import time
from os import system

human = -1
ai = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

#Checks the state of the board and evaluates if the AI won or the human.

def evaluate(state):  
    if wins(state, ai):
        score = +1
    elif wins(state, human):
        score = -1
    else:
        score = 0

    return score

#Checks the state of the board to an array of win conditions.

def wins(state, player):
    win_conditions = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]

    if [player, player, player] in win_conditions:
        return True
    else:
        return False

#Checks if the game is won.

def game_won(state):
    return wins(state, human) or wins(state, ai)

#Makes a list of empty cells.

def empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells

#Checks if move is vlid in the empty-cells.

def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False

def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False

#Calculate the minimax for optimal move

def minimax(state, depth, player):
    if player == ai:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_won(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == ai:
            if score[2] > best[2]:
                best = score  #max value
        else:
            if score[2] < best[2]:
                best = score  #min value

    return best

#Clears consol.

def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')

#Prints the board.

def print_board(state, c_choice, h_choice):
    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n')    
    print(chars[state[0][0]], " ¦ ", chars[state[0][1]], " ¦ ", chars[state[0][2]])
    print("-------------")
    print(chars[state[1][0]], " ¦ ", chars[state[1][1]], " ¦ ", chars[state[1][2]])
    print("-------------")
    print(chars[state[2][0]], " ¦ ", chars[state[2][1]], " ¦ ", chars[state[2][2]])

def ai_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_won(board):
        return

    clean()
    print(f'The unbeatable AI\'\s turn [{c_choice}]')
    print_board(board, c_choice, h_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, ai)
        x, y = move[0], move[1]

    set_move(x, y, ai)
    time.sleep(1)

def human_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_won(board):
        return

    #Dictionary of legal moves.
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'The fallible Human\'\s  turn [{h_choice}]')
    print_board(board, c_choice, h_choice)

    while move < 1 or move > 9:
        try:
            print('\n')
            move = int(input('Pick a possition 1-9: '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], human)

            if not can_move:
                print('Illegal move.')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Byebye')
            exit()
        except (KeyError, ValueError):
            print('That was a bad choice')

#These actually run the game.

def main():
    clean()
    h_choice = ''  #X or O.
    c_choice = ''  #X or O.
    first = ''  #If human is the first.

    #Human player chooses X or O to play.

    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose marker X or O? ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Byebye')
            exit()
        except (KeyError, ValueError):
            print('This is a bad choice')

    #AI's marker. X always starts first.

    if h_choice == 'X':
        c_choice = 'O'
        first = 'Y'
    else:
        c_choice = 'X'
        first = 'N'

    #Main loop of the game.

    while len(empty_cells(board)) > 0 and not game_won(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    #If the game is won.
    
    if wins(board, human):
        clean()
        print(f'Human turn [{h_choice}]')
        print_board(board, c_choice, h_choice)
        print('Victory is upon you!')
    elif wins(board, ai):
        clean()
        print(f'Computer turn [{c_choice}]')
        print_board(board, c_choice, h_choice)
        print('The AI tastes victory. You only have shame.')
    else:
        clean()
        print_board(board, c_choice, h_choice)
        print('\n')
        print('It is a draw. :-(')

    exit()


if __name__ == '__main__':
    main()