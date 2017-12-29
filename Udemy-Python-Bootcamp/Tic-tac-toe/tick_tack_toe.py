""" A standard newb 2-player tick-tack-toe game """
import random
import os
import time

def game_board_reset():
    global game_board

    game_board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]

def clear_screen():
    os.system('cls')

def game_board_print():
    for row in game_board:
        print(row)

def get_player_instruction(current_player):
    player_coordinates = ''
    print('\nIt is %s turn' %(current_player))
    print("\nEnter coordinates using rowcolumn format. e.g. '0,0' will enter the player symbol into the first tile of the board (row 0, column 0)")
    print('Type "End" to end the game')
    print('\n')

    player_coordinates = input("Player instruction:").lower()

    return player_coordinates

def game_board_assign_move(current_player, player_coordinates):
    global game_board

    if len(player_coordinates) != 3:
        print('Co-ordinates not in range')
        return False

    row_idx = int(player_coordinates[0])
    col_idx = int(player_coordinates[2])

    if row_idx not in [0,1,2] or col_idx not in [0,1,2]:
        print('Co-ordinates not in range')
        valid_move = False
    else:        
        if game_board[row_idx][col_idx] == '.':
            game_board[row_idx][col_idx] = current_player
            valid_move = True
        else:
            print('That tile already has been used!')
            valid_move = False

    return valid_move


def game_board_check_status():
    global game_board

    status = ''

    
    while status == '':
        #Check Diag
        if game_board[0][0] != '.' and game_board[0][0] == game_board[1][1] == game_board[2][2]:
            status = 'Win'
        elif game_board[0][2] != '.' and game_board[0][2] == game_board[1][1] == game_board[2][0]:
            status = 'Win'

        if status == 'Win':
            break
        else:
            #Check Rows & Columns
            for i in range(0,2):
                if game_board[i][0] != '.' and game_board[i][0] == game_board[i][1] == game_board[i][2]:
                    status = 'Win'
                    break
                elif game_board[0][i] != '.' and game_board[0][i] == game_board[1][i] == game_board[2][i]:
                    status = 'Win'
                    break
        
        if status != 'Win':
            status = 'Continue'


    return status

def play_game():
    game_board = []
    game_symbols = ['o', 'x']
    current_player = game_symbols[random.randint(0, 1)]
    game_board_reset()
    while True:
        
        clear_screen()
        game_board_print()

        player_coordinates = get_player_instruction(current_player)
        if player_coordinates == 'end':
            print('"%s" has quit the game.......' %current_player)
            break

        valid_move = game_board_assign_move(current_player, player_coordinates)

        if valid_move is False:
            print("Invalid move. Try again....")
            time.sleep(3)
            continue
        
        play_status = game_board_check_status()

        if play_status == 'Win':
            print('\n -----WE HAVE A WINNER !!!!------')
            print('The winner of this match was "%s"' %current_player)
            break

        if current_player == 'x':
            current_player = 'o'
        else:
            current_player = 'x'

play_another = 'Y'
while play_another.upper() == 'Y':
    play_game()
    play_another = input('Play another game? (Y/N)')
