import turtle
import pickle
import random
import os


class GameBoard:
    def __init__(self, mode="new"):
        if mode == "new":
            self.user_board = [["U" for _ in range(0, 20)] for _ in range(0, 20)]
            self.hidden_board = [["0" for _ in range(0, 20)] for _ in range(0, 20)]
            self.total_mines = 0
            self.game_over = False
            self.new_game = True
            self.number_of_flags = 0

            mines = random.randint(65, 75)
            while mines > 0:
                rand_col = random.randint(0, 19)
                rand_row = random.randint(0, 19)

                if self.hidden_board[rand_row][rand_col] == "B":
                    mines -= 1

                else:
                    self.hidden_board[rand_row][rand_col] = "B"
                    self.total_mines += 1
                    mines -= 1

            for row_index in range(0, 20):
                for col_index in range(0, 20):
                    if self.hidden_board[row_index][col_index] != "B":
                        square_count = 0

                        for row_difference in range(-1, 2):
                            for col_difference in range(-1, 2):
                                if 0 <= (row_difference + row_index) <= 19 and 0 <= (col_difference + col_index) <= 19:
                                    if self.hidden_board[row_difference + row_index][col_difference + col_index] == "B":
                                        square_count += 1

                        self.hidden_board[row_index][col_index] = str(square_count)

        elif mode == "load":
            with open("Game_Files/Game_Board.pkl", "rb") as f:
                new_self = pickle.load(f)
            f.close()

            self.user_board = new_self.user_board[:]
            self.hidden_board = new_self.hidden_board[:]
            self.total_mines = new_self.total_mines
            self.game_over = new_self.game_over
            self.new_game = new_self.new_game
            self.number_of_flags = new_self.number_of_flags

    def save_board(self):
        if not os.path.isdir("Game_Files"):
            os.mkdir("Game_Files")

        with open("Game_Files/Game_Board.pkl", "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    def clear_zeros(self, x_index, y_index):
        if self.user_board[x_index][y_index] == self.hidden_board[x_index][y_index]:
            return

        if self.user_board[x_index][y_index] == "F":
            return

        self.user_board[x_index][y_index] = self.hidden_board[x_index][y_index]

        draw_num(y_index, x_index, self.user_board[x_index][y_index])

        if self.hidden_board[x_index][y_index] == "0":
            for row_difference in range(-1, 2):
                for col_difference in range(-1, 2):
                    if 0 <= (row_difference + x_index) <= 19 and 0 <= (col_difference + y_index) <= 19:
                        self.clear_zeros(x_index + row_difference, y_index + col_difference)

    def check_win(self):
        if self.total_mines == self.number_of_flags:
            for row_index in range(0, 20):
                for col_index in range(0, 20):
                    if self.user_board[row_index][col_index] == "U":
                        return False

            return True

        else:
            return False


def go_to_pos(x, y):
    turtle_object.penup()
    turtle_object.setposition(x, y)
    turtle_object.pendown()


def draw_horizontal_line(start_x, start_y, colour, length):
    turtle_object.setheading(0)
    turtle_object.color(colour)
    go_to_pos(start_x, start_y)
    turtle_object.forward(length)


def draw_vertical_line(start_x, start_y, colour, length):
    turtle_object.setheading(-90)
    turtle_object.color(colour)
    go_to_pos(start_x, start_y)
    turtle_object.forward(length)


def draw_flag(x_index, y_index):
    x_dict = {x: x * 20 - 200 for x in range(19, -1, -1)}
    y_dict = {19 - y: y * 20 - 200 for y in range(19, -1, -1)}

    turtle_object.color("black")
    turtle_object.setheading(0)

    draw_horizontal_line(x_dict[x_index] + 4, y_dict[y_index] + 3, "black", 12)
    draw_horizontal_line(x_dict[x_index] + 4, y_dict[y_index] + 4, "black", 12)
    draw_horizontal_line(x_dict[x_index] + 5, y_dict[y_index] + 5, "black", 10)
    draw_horizontal_line(x_dict[x_index] + 7, y_dict[y_index] + 6, "black", 6)
    draw_horizontal_line(x_dict[x_index] + 9, y_dict[y_index] + 7, "black", 2)
    draw_horizontal_line(x_dict[x_index] + 9, y_dict[y_index] + 8, "black", 2)
    draw_horizontal_line(x_dict[x_index] + 9, y_dict[y_index] + 9, "red", 2)
    draw_horizontal_line(x_dict[x_index] + 7, y_dict[y_index] + 10, "red", 4)
    draw_horizontal_line(x_dict[x_index] + 5, y_dict[y_index] + 11, "red", 6)
    draw_horizontal_line(x_dict[x_index] + 4, y_dict[y_index] + 12, "red", 7)
    draw_horizontal_line(x_dict[x_index] + 4, y_dict[y_index] + 13, "red", 7)
    draw_horizontal_line(x_dict[x_index] + 5, y_dict[y_index] + 14, "red", 6)
    draw_horizontal_line(x_dict[x_index] + 7, y_dict[y_index] + 15, "red", 4)
    draw_horizontal_line(x_dict[x_index] + 9, y_dict[y_index] + 16, "red", 2)


def draw_win():
    window.bgcolor("orange")


def draw_unknown(x_index, y_index):
    x_dict = {x: x * 20 - 200 for x in range(19, -1, -1)}
    y_dict = {19 - y: y * 20 - 200 for y in range(19, -1, -1)}

    for row in range(0, 19):
        draw_horizontal_line(x_dict[x_index] + 1, y_dict[y_index] + 1 + row, "gray", 19)


def draw_mine_number(x_index, y_index, number):
    turtle_object.color("black")
    turtle_object.setheading(0)

    if number == "":
        pass

    elif number == "-":
        draw_horizontal_line(x_index + 6, y_index + 10, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 9, "black", 8)

    elif number == "0":
        draw_horizontal_line(x_index + 6, y_index + 15, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 14, "black", 8)

        draw_horizontal_line(x_index + 6, y_index + 5, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 4, "black", 8)

        draw_vertical_line(x_index + 6, y_index + 13, "black", 8)
        draw_vertical_line(x_index + 7, y_index + 13, "black", 8)

        draw_vertical_line(x_index + 12, y_index + 13, "black", 8)
        draw_vertical_line(x_index + 13, y_index + 13, "black", 8)

    elif number == "1":
        draw_vertical_line(x_index + 9, y_index + 15, "black", 12)
        draw_vertical_line(x_index + 10, y_index + 15, "black", 12)

    elif number == "2":
        draw_horizontal_line(x_index + 6, y_index + 15, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 14, "black", 8)

        draw_horizontal_line(x_index + 6, y_index + 10, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 9, "black", 8)

        draw_horizontal_line(x_index + 6, y_index + 5, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 4, "black", 8)

        draw_vertical_line(x_index + 12, y_index + 13, "black", 3)
        draw_vertical_line(x_index + 13, y_index + 13, "black", 3)

        draw_vertical_line(x_index + 6, y_index + 8, "black", 3)
        draw_vertical_line(x_index + 7, y_index + 8, "black", 3)

    elif number == "3":
        draw_horizontal_line(x_index + 6, y_index + 15, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 14, "black", 8)

        draw_horizontal_line(x_index + 6, y_index + 10, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 9, "black", 8)

        draw_horizontal_line(x_index + 6, y_index + 5, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 4, "black", 8)

        draw_vertical_line(x_index + 12, y_index + 13, "black", 3)
        draw_vertical_line(x_index + 13, y_index + 13, "black", 3)

        draw_vertical_line(x_index + 12, y_index + 8, "black", 3)
        draw_vertical_line(x_index + 13, y_index + 8, "black", 3)

    elif number == "4":
        draw_vertical_line(x_index + 6, y_index + 15, "black", 9)
        draw_vertical_line(x_index + 7, y_index + 15, "black", 9)

        draw_vertical_line(x_index + 10, y_index + 11, "black", 8)
        draw_vertical_line(x_index + 11, y_index + 11, "black", 8)

        draw_horizontal_line(x_index + 6, y_index + 8, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 7, "black", 8)

    elif number == "5":
        draw_horizontal_line(x_index + 6, y_index + 15, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 14, "black", 8)

        draw_horizontal_line(x_index + 6, y_index + 10, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 9, "black", 8)

        draw_horizontal_line(x_index + 6, y_index + 5, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 4, "black", 8)

        draw_vertical_line(x_index + 6, y_index + 13, "black", 3)
        draw_vertical_line(x_index + 7, y_index + 13, "black", 3)

        draw_vertical_line(x_index + 12, y_index + 8, "black", 3)
        draw_vertical_line(x_index + 13, y_index + 8, "black", 3)

    elif number == "6":
        draw_horizontal_line(x_index + 6, y_index + 15, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 14, "black", 8)

        draw_horizontal_line(x_index + 6, y_index + 10, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 9, "black", 8)

        draw_horizontal_line(x_index + 6, y_index + 5, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 4, "black", 8)

        draw_vertical_line(x_index + 6, y_index + 13, "black", 8)
        draw_vertical_line(x_index + 7, y_index + 13, "black", 8)

        draw_vertical_line(x_index + 12, y_index + 8, "black", 3)
        draw_vertical_line(x_index + 13, y_index + 8, "black", 3)

    elif number == "7":
        draw_horizontal_line(x_index + 6, y_index + 15, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 14, "black", 8)

        draw_vertical_line(x_index + 12, y_index + 15, "black", 12)
        draw_vertical_line(x_index + 13, y_index + 15, "black", 12)

    elif number == "8":
        draw_horizontal_line(x_index + 6, y_index + 15, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 14, "black", 8)

        draw_horizontal_line(x_index + 6, y_index + 10, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 9, "black", 8)

        draw_horizontal_line(x_index + 6, y_index + 5, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 4, "black", 8)

        draw_vertical_line(x_index + 6, y_index + 13, "black", 8)
        draw_vertical_line(x_index + 7, y_index + 13, "black", 8)

        draw_vertical_line(x_index + 12, y_index + 13, "black", 8)
        draw_vertical_line(x_index + 13, y_index + 13, "black", 8)

    elif number == "9":
        draw_horizontal_line(x_index + 6, y_index + 15, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 14, "black", 8)

        draw_horizontal_line(x_index + 6, y_index + 10, "black", 8)
        draw_horizontal_line(x_index + 6, y_index + 9, "black", 8)

        draw_vertical_line(x_index + 6, y_index + 13, "black", 4)
        draw_vertical_line(x_index + 7, y_index + 13, "black", 4)

        draw_vertical_line(x_index + 12, y_index + 13, "black", 10)
        draw_vertical_line(x_index + 13, y_index + 13, "black", 10)


def draw_remaning_mines_number(num_of_mines):
    for row in range(0, 12):
        draw_horizontal_line(168, 215 + row, "darkgray", 33)

    mine_number_list = [str(num_of_mines)[digit] if digit < len(str(num_of_mines)) else "" for digit in range(0, 3)]

    draw_mine_number(162, 211, mine_number_list[0])
    draw_mine_number(175, 211, mine_number_list[1])
    draw_mine_number(187, 211, mine_number_list[2])


def draw_bomb(x_index, y_index):
    x_dict = {x: x * 20 - 200 for x in range(19, -1, -1)}
    y_dict = {19 - y: y * 20 - 200 for y in range(19, -1, -1)}

    draw_horizontal_line(x_dict[x_index] + 9, y_dict[y_index] + 16, "black", 2)
    draw_horizontal_line(x_dict[x_index] + 7, y_dict[y_index] + 15, "black", 6)
    draw_horizontal_line(x_dict[x_index] + 5, y_dict[y_index] + 14, "black", 10)

    draw_horizontal_line(x_dict[x_index] + 5, y_dict[y_index] + 13, "black", 1)
    draw_horizontal_line(x_dict[x_index] + 8, y_dict[y_index] + 13, "black", 4)
    draw_horizontal_line(x_dict[x_index] + 14, y_dict[y_index] + 13, "black", 1)

    draw_horizontal_line(x_dict[x_index] + 4, y_dict[y_index] + 12, "black", 2)
    draw_horizontal_line(x_dict[x_index] + 8, y_dict[y_index] + 12, "black", 4)
    draw_horizontal_line(x_dict[x_index] + 14, y_dict[y_index] + 12, "black", 2)

    draw_horizontal_line(x_dict[x_index] + 4, y_dict[y_index] + 11, "black", 12)

    draw_horizontal_line(x_dict[x_index] + 3, y_dict[y_index] + 10, "black", 6)
    draw_horizontal_line(x_dict[x_index] + 11, y_dict[y_index] + 10, "black", 6)

    draw_horizontal_line(x_dict[x_index] + 3, y_dict[y_index] + 9, "black", 6)
    draw_horizontal_line(x_dict[x_index] + 11, y_dict[y_index] + 9, "black", 6)

    draw_horizontal_line(x_dict[x_index] + 4, y_dict[y_index] + 8, "black", 12)

    draw_horizontal_line(x_dict[x_index] + 4, y_dict[y_index] + 7, "black", 2)
    draw_horizontal_line(x_dict[x_index] + 8, y_dict[y_index] + 7, "black", 4)
    draw_horizontal_line(x_dict[x_index] + 14, y_dict[y_index] + 7, "black", 2)

    draw_horizontal_line(x_dict[x_index] + 5, y_dict[y_index] + 6, "black", 1)
    draw_horizontal_line(x_dict[x_index] + 8, y_dict[y_index] + 6, "black", 4)
    draw_horizontal_line(x_dict[x_index] + 14, y_dict[y_index] + 6, "black", 1)

    draw_horizontal_line(x_dict[x_index] + 5, y_dict[y_index] + 5, "black", 10)
    draw_horizontal_line(x_dict[x_index] + 7, y_dict[y_index] + 4, "black", 6)
    draw_horizontal_line(x_dict[x_index] + 9, y_dict[y_index] + 3, "black", 2)


def draw_exploded_bomb(x_index, y_index):
    x_dict = {x: x * 20 - 200 for x in range(19, -1, -1)}
    y_dict = {19 - y: y * 20 - 200 for y in range(19, -1, -1)}

    for row in range(0, 19):
        draw_horizontal_line(x_dict[x_index] + 1, y_dict[y_index] + 1 + row, "red", 19)

    draw_bomb(x_index, y_index)


def draw_num(x_index, y_index, number):
    x_dict = {x: x * 20 - 200 for x in range(19, -1, -1)}
    y_dict = {19 - y: y * 20 - 200 for y in range(19, -1, -1)}

    turtle_object.color("black")
    turtle_object.setheading(0)
    draw_clear(x_index, y_index)

    if number == "0":
        pass

    elif number == "1":
        draw_vertical_line(x_dict[x_index] + 9, y_dict[y_index] + 15, "black", 12)
        draw_vertical_line(x_dict[x_index] + 10, y_dict[y_index] + 15, "black", 12)

    elif number == "2":
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 15, "black", 8)
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 14, "black", 8)

        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 10, "black", 8)
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 9, "black", 8)

        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 5, "black", 8)
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 4, "black", 8)

        draw_vertical_line(x_dict[x_index] + 12, y_dict[y_index] + 13, "black", 3)
        draw_vertical_line(x_dict[x_index] + 13, y_dict[y_index] + 13, "black", 3)

        draw_vertical_line(x_dict[x_index] + 6, y_dict[y_index] + 8, "black", 3)
        draw_vertical_line(x_dict[x_index] + 7, y_dict[y_index] + 8, "black", 3)

    elif number == "3":
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 15, "black", 8)
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 14, "black", 8)

        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 10, "black", 8)
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 9, "black", 8)

        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 5, "black", 8)
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 4, "black", 8)

        draw_vertical_line(x_dict[x_index] + 12, y_dict[y_index] + 13, "black", 3)
        draw_vertical_line(x_dict[x_index] + 13, y_dict[y_index] + 13, "black", 3)

        draw_vertical_line(x_dict[x_index] + 12, y_dict[y_index] + 8, "black", 3)
        draw_vertical_line(x_dict[x_index] + 13, y_dict[y_index] + 8, "black", 3)

    elif number == "4":
        draw_vertical_line(x_dict[x_index] + 6, y_dict[y_index] + 15, "black", 9)
        draw_vertical_line(x_dict[x_index] + 7, y_dict[y_index] + 15, "black", 9)

        draw_vertical_line(x_dict[x_index] + 10, y_dict[y_index] + 11, "black", 8)
        draw_vertical_line(x_dict[x_index] + 11, y_dict[y_index] + 11, "black", 8)

        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 8, "black", 8)
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 7, "black", 8)

    elif number == "5":
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 15, "black", 8)
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 14, "black", 8)

        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 10, "black", 8)
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 9, "black", 8)

        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 5, "black", 8)
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 4, "black", 8)

        draw_vertical_line(x_dict[x_index] + 6, y_dict[y_index] + 13, "black", 3)
        draw_vertical_line(x_dict[x_index] + 7, y_dict[y_index] + 13, "black", 3)

        draw_vertical_line(x_dict[x_index] + 12, y_dict[y_index] + 8, "black", 3)
        draw_vertical_line(x_dict[x_index] + 13, y_dict[y_index] + 8, "black", 3)

    elif number == "6":
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 15, "black", 8)
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 14, "black", 8)

        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 10, "black", 8)
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 9, "black", 8)

        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 5, "black", 8)
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 4, "black", 8)

        draw_vertical_line(x_dict[x_index] + 6, y_dict[y_index] + 13, "black", 8)
        draw_vertical_line(x_dict[x_index] + 7, y_dict[y_index] + 13, "black", 8)

        draw_vertical_line(x_dict[x_index] + 12, y_dict[y_index] + 8, "black", 3)
        draw_vertical_line(x_dict[x_index] + 13, y_dict[y_index] + 8, "black", 3)

    elif number == "7":
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 15, "black", 8)
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 14, "black", 8)

        draw_vertical_line(x_dict[x_index] + 12, y_dict[y_index] + 15, "black", 12)
        draw_vertical_line(x_dict[x_index] + 13, y_dict[y_index] + 15, "black", 12)

    elif number == "8":
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 15, "black", 8)
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 14, "black", 8)

        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 10, "black", 8)
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 9, "black", 8)

        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 5, "black", 8)
        draw_horizontal_line(x_dict[x_index] + 6, y_dict[y_index] + 4, "black", 8)

        draw_vertical_line(x_dict[x_index] + 6, y_dict[y_index] + 13, "black", 8)
        draw_vertical_line(x_dict[x_index] + 7, y_dict[y_index] + 13, "black", 8)

        draw_vertical_line(x_dict[x_index] + 12, y_dict[y_index] + 13, "black", 8)
        draw_vertical_line(x_dict[x_index] + 13, y_dict[y_index] + 13, "black", 8)


def draw_clear(x_index, y_index):
    x_dict = {x: x * 20 - 200 for x in range(19, -1, -1)}
    y_dict = {19 - y: y * 20 - 200 for y in range(19, -1, -1)}

    for row in range(0, 19):
        draw_horizontal_line(x_dict[x_index] + 1, y_dict[y_index] + 1 + row, "lightgray", 19)


def square_being_clicked(x, y):
    x_dict = {x: x * 20 - 200 for x in range(19, -1, -1)}
    y_dict = {19 - y: y * 20 - 200 for y in range(19, -1, -1)}

    x_coord = 21
    y_coord = 21

    for x_key in x_dict:
        if x > x_dict[x_key]:
            x_coord = x_key
            break

    for y_key in y_dict:
        if y > y_dict[y_key]:
            y_coord = y_key
            break

    if 200 < x > -200 or 200 < y > -200:
        x_coord = 21
        y_coord = 21

    if -154 > x > -200 and 227 > y > 215:
        x_coord = 22
        y_coord = 22

    if -119 > x > -149 and 227 > y > 215:
        x_coord = 23
        y_coord = 23

    x_index = y_coord
    y_index = x_coord

    return x_index, y_index


def draw_letter(start_x, start_y, letter):
    if letter == "a":
        draw_horizontal_line(start_x + 1, start_y + 4, "black", 1)
        draw_horizontal_line(start_x + 1, start_y + 2, "black", 1)

        draw_vertical_line(start_x, start_y + 4, "black", 5)
        draw_vertical_line(start_x + 2, start_y + 4, "black", 5)

    elif letter == "b":
        pass
    elif letter == "c":
        pass
    elif letter == "d":
        pass
    elif letter == "e":
        draw_horizontal_line(start_x + 1, start_y + 4, "black", 2)
        draw_horizontal_line(start_x + 1, start_y + 2, "black", 2)
        draw_horizontal_line(start_x + 1, start_y, "black", 2)

        draw_vertical_line(start_x, start_y + 4, "black", 5)

    elif letter == "f":
        pass
    elif letter == "g":
        turtle_object.color("black")
        turtle_object.setheading(-180)

        go_to_pos(start_x + 4, start_y + 4)

        turtle_object.forward(4)
        turtle_object.left(90)

        turtle_object.forward(4)
        turtle_object.left(90)

        turtle_object.forward(4)
        turtle_object.left(90)

        turtle_object.forward(2)
        turtle_object.left(90)

        turtle_object.forward(3)
        turtle_object.left(90)

    elif letter == "h":
        pass
    elif letter == "i":
        draw_vertical_line(start_x, start_y + 4, "black", 1)
        draw_vertical_line(start_x, start_y + 2, "black", 3)

    elif letter == "j":
        pass
    elif letter == "k":
        pass
    elif letter == "l":
        pass
    elif letter == "m":
        draw_horizontal_line(start_x, start_y + 4, "black", 5)

        draw_vertical_line(start_x, start_y + 3, "black", 4)
        draw_vertical_line(start_x + 2, start_y + 3, "black", 4)
        draw_vertical_line(start_x + 4, start_y + 3, "black", 4)

    elif letter == "n":
        draw_vertical_line(start_x, start_y + 4, "black", 5)
        draw_vertical_line(start_x + 4, start_y + 4, "black", 5)

        draw_horizontal_line(start_x + 1, start_y + 3, "black", 1)
        draw_horizontal_line(start_x + 2, start_y + 2, "black", 1)
        draw_horizontal_line(start_x + 3, start_y + 1, "black", 1)
    elif letter == "o":
        pass
    elif letter == "p":
        pass
    elif letter == "q":
        pass
    elif letter == "r":
        pass
    elif letter == "s":
        turtle_object.color("black")
        turtle_object.setheading(-180)

        go_to_pos(start_x + 2, start_y + 4)

        turtle_object.forward(2)
        turtle_object.left(90)

        turtle_object.forward(2)
        turtle_object.left(90)

        turtle_object.forward(2)
        turtle_object.right(90)

        turtle_object.forward(2)
        turtle_object.right(90)

        turtle_object.forward(3)

    elif letter == "t":
        pass
    elif letter == "u":
        pass
    elif letter == "v":
        pass
    elif letter == "w":
        draw_horizontal_line(start_x, start_y, "black", 5)

        draw_vertical_line(start_x, start_y + 4, "black", 4)
        draw_vertical_line(start_x + 2, start_y + 4, "black", 4)
        draw_vertical_line(start_x + 4, start_y + 4, "black", 4)

    elif letter == "x":
        pass
    elif letter == "y":
        pass
    elif letter == "z":
        pass


def draw_mine_button():
    # Bottom Left square = -149, 215

    draw_horizontal_line(-149, 215, "black", 30)
    draw_horizontal_line(-149, 227, "black", 30)

    draw_vertical_line(-149, 227, "black", 13)
    draw_vertical_line(-119, 227, "black", 13)

    for row in range(0, 11):
        draw_horizontal_line(-148, 226 - row, "lightgrey", 29)

    draw_letter(-144, 219, "m")
    draw_letter(-138, 219, "i")
    draw_letter(-136, 219, "n")
    draw_letter(-130, 219, "e")
    draw_letter(-126, 219, "s")


def draw_new_game_button():
    draw_horizontal_line(-200, 215, "black", 46)
    draw_horizontal_line(-200, 227, "black", 46)

    draw_vertical_line(-200, 227, "black", 13)
    draw_vertical_line(-154, 227, "black", 13)

    for row in range(0, 11):
        draw_horizontal_line(-199, 226 - row, "lightgrey", 45)

    # Bottom Left square = -200, 215

    draw_letter(-196, 219, "n")
    draw_letter(-190, 219, "e")
    draw_letter(-186, 219, "w")
    draw_letter(-177, 219, "g")
    draw_letter(-171, 219, "a")
    draw_letter(-167, 219, "m")
    draw_letter(-161, 219, "e")


def draw_basic_board():
    for row in range(0, 400):
        draw_horizontal_line(-200, 200 - row, "gray", 400)

    turtle_object.color("black")

    draw_new_game_button()
    draw_mine_button()

    turtle_object.color("black")
    turtle_object.setheading(0)
    for row in range(0, 20):

        go_to_pos(-200, 200 + (-20 * row))

        for square in range(0, 20):
            for line in range(0, 4):
                turtle_object.forward(20)
                turtle_object.right(90)
            turtle_object.forward(20)


def left_click(x, y):
    game_board = GameBoard("load")

    square_coords = square_being_clicked(x, y)

    if square_coords[0] == 22 and square_coords[1] == 22:
        """
        window.clear()
        window.tracer(0, 0)
        window.bgcolor("darkgray")

        draw_basic_board()

        game_board = GameBoard()
        game_board.save_board()

        window.onscreenclick(left_click, btn=1)
        window.onscreenclick(middle_click, btn=2)
        window.onscreenclick(right_click, btn=3)

        window.update()

        window.mainloop()

        return
        

        game_board = GameBoard()
        game_board.save_board()

        draw_basic_board()

        return
        """

        os.startfile("Bomb_Locatorino.pyw")
        exit()

    if game_board.game_over:
        return

    if square_coords[0] == 21 or square_coords[1] == 21:
        return

    if square_coords[0] == 23 or square_coords[1] == 23:
        draw_remaning_mines_number(game_board.total_mines - game_board.number_of_flags)
        window.update()

        return

    if game_board.new_game:
        while game_board.hidden_board[square_coords[0]][square_coords[1]] != "0":
            game_board = GameBoard()
        game_board.new_game = False

        game_board.clear_zeros(square_coords[0], square_coords[1])
        # draw_remaning_mines_number(game_board.total_mines - game_board.number_of_flags)

    if game_board.user_board[square_coords[0]][square_coords[1]] == "U":
        if game_board.user_board[square_coords[0]][square_coords[1]] == "F":
            pass

        elif game_board.hidden_board[square_coords[0]][square_coords[1]] == "B":
            for row_index in range(0, 20):
                for col_index in range(0, 20):
                    if game_board.hidden_board[row_index][col_index] == "B" and \
                            game_board.user_board[row_index][col_index] != "F":
                        draw_bomb(col_index, row_index)

            draw_exploded_bomb(square_coords[1], square_coords[0])

            game_board.game_over = True

        elif game_board.hidden_board[square_coords[0]][square_coords[1]] == "0":
            game_board.clear_zeros(square_coords[0], square_coords[1])

            if game_board.check_win():
                game_board.game_over = True
                draw_win()

        else:
            game_board.user_board[square_coords[0]][square_coords[1]] = \
                game_board.hidden_board[square_coords[0]][square_coords[1]]

            draw_num(square_coords[1], square_coords[0], game_board.user_board[square_coords[0]][square_coords[1]])

            if game_board.check_win():
                game_board.game_over = True
                draw_win()

    game_board.save_board()
    window.update()


def middle_click(x, y):
    game_board = GameBoard("load")

    if game_board.game_over:
        return

    square_coords = square_being_clicked(x, y)
    if square_coords[0] == 21 or square_coords[1] == 21:
        return

    if square_coords[0] == 22 and square_coords[1] == 22:
        return

    if square_coords[0] == 23 and square_coords[1] == 23:
        return

    if game_board.new_game:
        return

    for row_difference in range(-1, 2):
        for col_difference in range(-1, 2):
            row_shifted = row_difference + square_coords[0]
            col_shifted = col_difference + square_coords[1]

            if 0 <= row_shifted <= 19 and 0 <= col_shifted <= 19:
                if game_board.user_board[row_shifted][col_shifted] == "F":
                    pass

                elif game_board.hidden_board[row_shifted][col_shifted] == "B":
                    for row_index in range(0, 20):
                        for col_index in range(0, 20):
                            if game_board.hidden_board[row_index][col_index] == "B" and \
                                    game_board.user_board[row_index][col_index] != "F":
                                draw_bomb(col_index, row_index)

                    draw_exploded_bomb(col_shifted, row_shifted)

                    game_board.game_over = True
                    game_board.save_board()
                    window.update()

                    return

                elif game_board.hidden_board[row_shifted][col_shifted] == "0":
                    game_board.clear_zeros(row_shifted, col_shifted)

                else:
                    game_board.user_board[row_shifted][col_shifted] = game_board.hidden_board[row_shifted][col_shifted]

                    draw_num(col_shifted, row_shifted, game_board.hidden_board[row_shifted][col_shifted])

                if game_board.check_win():
                    game_board.game_over = True
                    draw_win()

    game_board.save_board()
    window.update()


def right_click(x, y):
    game_board = GameBoard("load")

    if game_board.game_over:
        return

    square_coords = square_being_clicked(x, y)
    if square_coords[0] == 21 or square_coords[1] == 21:
        return

    if square_coords[0] == 22 and square_coords[1] == 22:
        return

    if square_coords[0] == 23 and square_coords[1] == 23:
        return

    if game_board.new_game:
        return

    if game_board.user_board[square_coords[0]][square_coords[1]] == "U":
        game_board.user_board[square_coords[0]][square_coords[1]] = "F"

        draw_flag(square_coords[1], square_coords[0])
        game_board.number_of_flags += 1

        # draw_remaning_mines_number(game_board.total_mines - game_board.number_of_flags)

        if game_board.check_win():
            game_board.game_over = True
            draw_win()

    elif game_board.user_board[square_coords[0]][square_coords[1]] == "F":
        game_board.user_board[square_coords[0]][square_coords[1]] = "U"

        draw_unknown(square_coords[1], square_coords[0])
        game_board.number_of_flags -= 1

        # draw_remaning_mines_number(game_board.total_mines - game_board.number_of_flags)

    game_board.save_board()
    window.update()


def main():
    window.setup(500, 500)
    window.tracer(0, 0)
    window.title("Bomb Locatorino")
    window.bgcolor("darkgray")

    turtle_object.speed(0)
    turtle_object.hideturtle()

    draw_basic_board()

    game_board = GameBoard()
    game_board.save_board()

    window.update()

    window.onscreenclick(left_click, btn=1)
    window.onscreenclick(middle_click, btn=2)
    window.onscreenclick(right_click, btn=3)

    window.mainloop()


if __name__ == "__main__":
    turtle_object = turtle.Turtle()
    window = turtle.Screen()
    main()
