""" A standard 2-player tick-tack-toe game """
import random


def game_board_reset():
    """assign empty values to the game board"""
    global game_board
    game_board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]


def game_board_print():
    for row in game_board:
        print(row)

def get_player_instruction(current_player):
    player_coordinates = ''
    print('\nIt is %s turn' %(current_player))
    print("\nEnter coordinates using rowcolumn format. e.g. '0,0' will enter the player symbol into the first tile of the board (row 0, column 0)")
    print('Type "End" to end the game')
    print('\n')
    while True:
        player_coordinates = input("Player instruction:").lower()

        if player_coordinates == 'end':
            break

        if int(player_coordinates[0]) in range(0, 9) and player_coordinates[1] == ',' \
                and int(player_coordinates[2]) in range(0, 9):
            break
        else:
            continue

    return player_coordinates

def game_board_assign_move(current_player,player_coordinates):
    global game_board

    game_board[int(player_coordinates[0])][int(player_coordinates[2])] = current_player
    print('game_board_assign_move......')
    return False


def play_game():
    game_board = []
    game_symbols = ['o', 'x']
    current_player = game_symbols[random.randint(0, 1)]
    game_board_reset()
    while True:
        
        player_coordinates = get_player_instruction(current_player)
        if player_coordinates == 'end':
            print('"%s" has quit the game.......' %current_player)
            break

        end_game_check = game_board_assign_move(current_player,player_coordinates)

        game_board_print()

        if current_player == 'x':
            current_player = 'o'
        else:
            current_player = 'x'


    
play_game()        
        







