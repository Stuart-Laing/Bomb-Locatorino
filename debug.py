from Bomb_Locatorino import *

game_board = GameBoard("load")

print("USER_BOARD")
for row in game_board.user_board:
    for col in row:
        print(col, end="")
    print()
print()
print("HIDDEN_BOARD")
for row in game_board.hidden_board:
    for col in row:
        print(col, end="")
    print()
print()
print("TOTAL_MINES =", game_board.total_mines)
print("GAME_OVER =", game_board.game_over)
print("NEW_GAME =", game_board.new_game)
print("NUMBER_OF_FLAGS =", game_board.number_of_flags)

input()
