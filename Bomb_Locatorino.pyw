import turtle
import random


class GameBoard:
    def __init__(self):
        self.user_board = [["U" for _ in range(0, 20)] for _ in range(0, 20)]
        self.hidden_board = [["0" for _ in range(0, 20)] for _ in range(0, 20)]
        self.total_mines = 0
        self.game_over = False
        self.new_game = True
        self.number_of_flags = 0
        self.selected_square = SelectedSquare()

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

    def clear_zeros(self, row_index, col_index):
        if self.user_board[row_index][col_index] == self.hidden_board[row_index][col_index]:
            return

        if self.user_board[row_index][col_index] == "F":
            return

        self.user_board[row_index][col_index] = self.hidden_board[row_index][col_index]

        draw_number(row_index, col_index, self.user_board[row_index][col_index])

        if self.hidden_board[row_index][col_index] == "0":
            for row_difference in range(-1, 2):
                for col_difference in range(-1, 2):
                    if 0 <= (row_difference + row_index) <= 19 and 0 <= (col_difference + col_index) <= 19:
                        self.clear_zeros(row_index + row_difference, col_index + col_difference)

    def check_win(self):
        if self.total_mines == self.number_of_flags:
            for row_index in range(0, 20):
                for col_index in range(0, 20):
                    if self.user_board[row_index][col_index] == "U":
                        return False

            return True

        else:
            return False

    def new_board(self):
        self.__init__()

    def move_selected_square(self, direction):
        if direction == "up":
            if self.selected_square.location[0] > 0:
                self.selected_square.go_up()

                if self.user_board[self.selected_square.location[0] + 1][self.selected_square.location[1]] == "U":
                    draw_unknown(self.selected_square.location[0] + 1, self.selected_square.location[1])

                elif self.user_board[self.selected_square.location[0] + 1][self.selected_square.location[1]] == "F":
                    draw_unknown(self.selected_square.location[0] + 1, self.selected_square.location[1])
                    draw_flag(self.selected_square.location[0] + 1, self.selected_square.location[1])

                else:
                    draw_number(self.selected_square.location[0] + 1, self.selected_square.location[1],
                                self.user_board[self.selected_square.location[0] + 1][self.selected_square.location[1]])

        elif direction == "down":
            if self.selected_square.location[0] < 19:
                self.selected_square.go_down()

                if self.user_board[self.selected_square.location[0] - 1][self.selected_square.location[1]] == "U":
                    draw_unknown(self.selected_square.location[0] - 1, self.selected_square.location[1])

                elif self.user_board[self.selected_square.location[0] - 1][self.selected_square.location[1]] == "F":
                    draw_unknown(self.selected_square.location[0] - 1, self.selected_square.location[1])
                    draw_flag(self.selected_square.location[0] - 1, self.selected_square.location[1])

                else:
                    draw_number(self.selected_square.location[0] - 1, self.selected_square.location[1],
                                self.user_board[self.selected_square.location[0] - 1][self.selected_square.location[1]])

        elif direction == "left":
            if self.selected_square.location[1] > 0:
                self.selected_square.go_left()

                if self.user_board[self.selected_square.location[0]][self.selected_square.location[1] + 1] == "U":
                    draw_unknown(self.selected_square.location[0], self.selected_square.location[1] + 1)

                elif self.user_board[self.selected_square.location[0]][self.selected_square.location[1] + 1] == "F":
                    draw_unknown(self.selected_square.location[0], self.selected_square.location[1] + 1)
                    draw_flag(self.selected_square.location[0], self.selected_square.location[1] + 1)

                else:
                    draw_number(self.selected_square.location[0], self.selected_square.location[1] + 1,
                                self.user_board[self.selected_square.location[0]][self.selected_square.location[1] + 1])

        elif direction == "right":
            if self.selected_square.location[1] < 19:
                self.selected_square.go_right()

                if self.user_board[self.selected_square.location[0]][self.selected_square.location[1] - 1] == "U":
                    draw_unknown(self.selected_square.location[0], self.selected_square.location[1] - 1)

                elif self.user_board[self.selected_square.location[0]][self.selected_square.location[1] - 1] == "F":
                    draw_unknown(self.selected_square.location[0], self.selected_square.location[1] - 1)
                    draw_flag(self.selected_square.location[0], self.selected_square.location[1] - 1)

                else:
                    draw_number(self.selected_square.location[0], self.selected_square.location[1] - 1,
                                self.user_board[self.selected_square.location[0]][self.selected_square.location[1] - 1])


class SelectedSquare:
    def __init__(self):
        self.location = [0, 0]

    def draw_selected_square(self):
        row_to_y_dict = {y: y * -20 + 180 for y in range(0, 20)}
        col_to_x_dict = {x: x * 20 - 200 for x in range(0, 20)}

        draw_horizontal_line(col_to_x_dict[self.location[1]] + 1, row_to_y_dict[self.location[0]] + 1, "blue", 19)
        draw_horizontal_line(col_to_x_dict[self.location[1]] + 1, row_to_y_dict[self.location[0]] + 2, "blue", 19)
        draw_horizontal_line(col_to_x_dict[self.location[1]] + 1, row_to_y_dict[self.location[0]] + 3, "blue", 19)

        draw_horizontal_line(col_to_x_dict[self.location[1]] + 1, row_to_y_dict[self.location[0]] + 19, "blue", 19)
        draw_horizontal_line(col_to_x_dict[self.location[1]] + 1, row_to_y_dict[self.location[0]] + 18, "blue", 19)
        draw_horizontal_line(col_to_x_dict[self.location[1]] + 1, row_to_y_dict[self.location[0]] + 17, "blue", 19)

        draw_vertical_line(col_to_x_dict[self.location[1]] + 1, row_to_y_dict[self.location[0]] + 16, "blue", 13)
        draw_vertical_line(col_to_x_dict[self.location[1]] + 2, row_to_y_dict[self.location[0]] + 16, "blue", 13)
        draw_vertical_line(col_to_x_dict[self.location[1]] + 3, row_to_y_dict[self.location[0]] + 16, "blue", 13)

        draw_vertical_line(col_to_x_dict[self.location[1]] + 19, row_to_y_dict[self.location[0]] + 16, "blue", 13)
        draw_vertical_line(col_to_x_dict[self.location[1]] + 18, row_to_y_dict[self.location[0]] + 16, "blue", 13)
        draw_vertical_line(col_to_x_dict[self.location[1]] + 17, row_to_y_dict[self.location[0]] + 16, "blue", 13)

    def go_up(self):
        self.location[0] -= 1
        self.draw_selected_square()

    def go_down(self):
        self.location[0] += 1
        self.draw_selected_square()

    def go_left(self):
        self.location[1] -= 1
        self.draw_selected_square()

    def go_right(self):
        self.location[1] += 1
        self.draw_selected_square()


def go_to_pos(x, y):
    """Move the turtle to the coordinates given

    Keyword arguments:
    x -- the x coordinate
    y -- the y coordinate
    """

    turtle_object.penup()
    turtle_object.setposition(x, y)
    turtle_object.pendown()


def check_square_selected(row_index, col_index):
    """Check if the current square being drawn is also where the selected square pointer is,
    and if so draws the pointer

    Keyword arguments:
    row_index -- the row index
    col_index -- the col index
    """
    if row_index == game_board.selected_square.location[0] and col_index == game_board.selected_square.location[1]:
        game_board.selected_square.draw_selected_square()


def draw_horizontal_line(start_x, start_y, colour, length):
    """Draws a horizontal line from left to right

    Keyword arguments:
    start_x -- the starting x coordinate of the line
    start_y -- the starting y coordinate of the line
    colour -- the colour of the line, expressed as a string
    length -- the length of the line in pixels
    """
    turtle_object.setheading(0)
    turtle_object.color(colour)
    go_to_pos(start_x, start_y)
    turtle_object.forward(length)


def draw_vertical_line(start_x, start_y, colour, length):
    """Draws a vertical line from top to bottom

    Keyword arguments:
    start_x -- the starting x coordinate of the line
    start_y -- the starting y coordinate of the line
    colour -- the colour of the line, expressed as a string
    length -- the length of the line in pixels
    """

    turtle_object.setheading(-90)
    turtle_object.color(colour)
    go_to_pos(start_x, start_y)
    turtle_object.forward(length)


def draw_flag(row_index, col_index):
    """Draws the flag symbol at the correct grid point

    Keyword arguments:
    row_index -- the row index
    col_index -- the col index
    """

    row_to_y_dict = {y: y * -20 + 180 for y in range(0, 20)}
    col_to_x_dict = {x: x * 20 - 200 for x in range(0, 20)}

    draw_horizontal_line(col_to_x_dict[col_index] + 4, row_to_y_dict[row_index] + 3, "black", 12)
    draw_horizontal_line(col_to_x_dict[col_index] + 4, row_to_y_dict[row_index] + 4, "black", 12)
    draw_horizontal_line(col_to_x_dict[col_index] + 5, row_to_y_dict[row_index] + 5, "black", 10)
    draw_horizontal_line(col_to_x_dict[col_index] + 7, row_to_y_dict[row_index] + 6, "black", 6)
    draw_horizontal_line(col_to_x_dict[col_index] + 9, row_to_y_dict[row_index] + 7, "black", 2)
    draw_horizontal_line(col_to_x_dict[col_index] + 9, row_to_y_dict[row_index] + 8, "black", 2)
    draw_horizontal_line(col_to_x_dict[col_index] + 9, row_to_y_dict[row_index] + 9, "red", 2)
    draw_horizontal_line(col_to_x_dict[col_index] + 7, row_to_y_dict[row_index] + 10, "red", 4)
    draw_horizontal_line(col_to_x_dict[col_index] + 5, row_to_y_dict[row_index] + 11, "red", 6)
    draw_horizontal_line(col_to_x_dict[col_index] + 4, row_to_y_dict[row_index] + 12, "red", 7)
    draw_horizontal_line(col_to_x_dict[col_index] + 4, row_to_y_dict[row_index] + 13, "red", 7)
    draw_horizontal_line(col_to_x_dict[col_index] + 5, row_to_y_dict[row_index] + 14, "red", 6)
    draw_horizontal_line(col_to_x_dict[col_index] + 7, row_to_y_dict[row_index] + 15, "red", 4)
    draw_horizontal_line(col_to_x_dict[col_index] + 9, row_to_y_dict[row_index] + 16, "red", 2)

    check_square_selected(row_index, col_index)


def draw_win():
    """Draws the word "Congratulations" to the screen"""
    # TODO
    window.bgcolor("green")


def draw_unknown(row_index, col_index):
    """Draws the grid point to be "unknown"

    Keyword arguments:
    row_index -- the row index
    col_index -- the col index
    """

    row_to_y_dict = {y: y * -20 + 180 for y in range(0, 20)}
    col_to_x_dict = {x: x * 20 - 200 for x in range(0, 20)}

    for row in range(0, 19):
        draw_horizontal_line(col_to_x_dict[col_index] + 1, row_to_y_dict[row_index] + 1 + row, "gray", 19)

    check_square_selected(row_index, col_index)


def draw_symbol(start_x, start_y, symbol):
    """Draws the symbol given at the coordinates, used for the board and the mines remaining

    Keyword arguments:
    start_x -- the starting x coordinate of the symbol
    start_y -- the starting y coordinate of the symbol
    symbol -- the symbol to be drawn
    """

    if symbol == "":
        pass

    elif symbol == "-":
        draw_horizontal_line(start_x + 6, start_y + 10, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 9, "black", 8)

    elif symbol == "0":
        draw_horizontal_line(start_x + 6, start_y + 15, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 14, "black", 8)

        draw_horizontal_line(start_x + 6, start_y + 5, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 4, "black", 8)

        draw_vertical_line(start_x + 6, start_y + 13, "black", 8)
        draw_vertical_line(start_x + 7, start_y + 13, "black", 8)

        draw_vertical_line(start_x + 12, start_y + 13, "black", 8)
        draw_vertical_line(start_x + 13, start_y + 13, "black", 8)

    elif symbol == "1":
        draw_vertical_line(start_x + 9, start_y + 15, "black", 12)
        draw_vertical_line(start_x + 10, start_y + 15, "black", 12)

    elif symbol == "2":
        draw_horizontal_line(start_x + 6, start_y + 15, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 14, "black", 8)

        draw_horizontal_line(start_x + 6, start_y + 10, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 9, "black", 8)

        draw_horizontal_line(start_x + 6, start_y + 5, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 4, "black", 8)

        draw_vertical_line(start_x + 12, start_y + 13, "black", 3)
        draw_vertical_line(start_x + 13, start_y + 13, "black", 3)

        draw_vertical_line(start_x + 6, start_y + 8, "black", 3)
        draw_vertical_line(start_x + 7, start_y + 8, "black", 3)

    elif symbol == "3":
        draw_horizontal_line(start_x + 6, start_y + 15, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 14, "black", 8)

        draw_horizontal_line(start_x + 6, start_y + 10, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 9, "black", 8)

        draw_horizontal_line(start_x + 6, start_y + 5, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 4, "black", 8)

        draw_vertical_line(start_x + 12, start_y + 13, "black", 3)
        draw_vertical_line(start_x + 13, start_y + 13, "black", 3)

        draw_vertical_line(start_x + 12, start_y + 8, "black", 3)
        draw_vertical_line(start_x + 13, start_y + 8, "black", 3)

    elif symbol == "4":
        draw_vertical_line(start_x + 6, start_y + 15, "black", 9)
        draw_vertical_line(start_x + 7, start_y + 15, "black", 9)

        draw_vertical_line(start_x + 10, start_y + 11, "black", 8)
        draw_vertical_line(start_x + 11, start_y + 11, "black", 8)

        draw_horizontal_line(start_x + 6, start_y + 8, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 7, "black", 8)

    elif symbol == "5":
        draw_horizontal_line(start_x + 6, start_y + 15, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 14, "black", 8)

        draw_horizontal_line(start_x + 6, start_y + 10, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 9, "black", 8)

        draw_horizontal_line(start_x + 6, start_y + 5, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 4, "black", 8)

        draw_vertical_line(start_x + 6, start_y + 13, "black", 3)
        draw_vertical_line(start_x + 7, start_y + 13, "black", 3)

        draw_vertical_line(start_x + 12, start_y + 8, "black", 3)
        draw_vertical_line(start_x + 13, start_y + 8, "black", 3)

    elif symbol == "6":
        draw_horizontal_line(start_x + 6, start_y + 15, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 14, "black", 8)

        draw_horizontal_line(start_x + 6, start_y + 10, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 9, "black", 8)

        draw_horizontal_line(start_x + 6, start_y + 5, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 4, "black", 8)

        draw_vertical_line(start_x + 6, start_y + 13, "black", 8)
        draw_vertical_line(start_x + 7, start_y + 13, "black", 8)

        draw_vertical_line(start_x + 12, start_y + 8, "black", 3)
        draw_vertical_line(start_x + 13, start_y + 8, "black", 3)

    elif symbol == "7":
        draw_horizontal_line(start_x + 6, start_y + 15, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 14, "black", 8)

        draw_vertical_line(start_x + 12, start_y + 15, "black", 12)
        draw_vertical_line(start_x + 13, start_y + 15, "black", 12)

    elif symbol == "8":
        draw_horizontal_line(start_x + 6, start_y + 15, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 14, "black", 8)

        draw_horizontal_line(start_x + 6, start_y + 10, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 9, "black", 8)

        draw_horizontal_line(start_x + 6, start_y + 5, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 4, "black", 8)

        draw_vertical_line(start_x + 6, start_y + 13, "black", 8)
        draw_vertical_line(start_x + 7, start_y + 13, "black", 8)

        draw_vertical_line(start_x + 12, start_y + 13, "black", 8)
        draw_vertical_line(start_x + 13, start_y + 13, "black", 8)

    elif symbol == "9":
        draw_horizontal_line(start_x + 6, start_y + 15, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 14, "black", 8)

        draw_horizontal_line(start_x + 6, start_y + 10, "black", 8)
        draw_horizontal_line(start_x + 6, start_y + 9, "black", 8)

        draw_vertical_line(start_x + 6, start_y + 13, "black", 4)
        draw_vertical_line(start_x + 7, start_y + 13, "black", 4)

        draw_vertical_line(start_x + 12, start_y + 13, "black", 10)
        draw_vertical_line(start_x + 13, start_y + 13, "black", 10)


def draw_remaining_mines_number(num_of_mines):
    """Draws the number of mines remaining

    Keyword arguments:
    num_of_mines -- the number of mines remaining on the board
    """

    for row in range(0, 12):
        draw_horizontal_line(168, 215 + row, "darkgray", 33)

    mine_number_list = [str(num_of_mines)[digit] if digit < len(str(num_of_mines)) else "" for digit in range(0, 3)]

    draw_symbol(162, 211, mine_number_list[0])
    draw_symbol(175, 211, mine_number_list[1])
    draw_symbol(187, 211, mine_number_list[2])


def draw_bomb(row_index, col_index):
    """Draws the bomb symbol at the correct grid point

    Keyword arguments:
    row_index -- the row index
    col_index -- the col index
    """

    row_to_y_dict = {y: y * -20 + 180 for y in range(0, 20)}
    col_to_x_dict = {x: x * 20 - 200 for x in range(0, 20)}

    draw_horizontal_line(col_to_x_dict[col_index] + 9, row_to_y_dict[row_index] + 16, "black", 2)
    draw_horizontal_line(col_to_x_dict[col_index] + 7, row_to_y_dict[row_index] + 15, "black", 6)
    draw_horizontal_line(col_to_x_dict[col_index] + 5, row_to_y_dict[row_index] + 14, "black", 10)

    draw_horizontal_line(col_to_x_dict[col_index] + 5, row_to_y_dict[row_index] + 13, "black", 1)
    draw_horizontal_line(col_to_x_dict[col_index] + 8, row_to_y_dict[row_index] + 13, "black", 4)
    draw_horizontal_line(col_to_x_dict[col_index] + 14, row_to_y_dict[row_index] + 13, "black", 1)

    draw_horizontal_line(col_to_x_dict[col_index] + 4, row_to_y_dict[row_index] + 12, "black", 2)
    draw_horizontal_line(col_to_x_dict[col_index] + 8, row_to_y_dict[row_index] + 12, "black", 4)
    draw_horizontal_line(col_to_x_dict[col_index] + 14, row_to_y_dict[row_index] + 12, "black", 2)

    draw_horizontal_line(col_to_x_dict[col_index] + 4, row_to_y_dict[row_index] + 11, "black", 12)

    draw_horizontal_line(col_to_x_dict[col_index] + 3, row_to_y_dict[row_index] + 10, "black", 6)
    draw_horizontal_line(col_to_x_dict[col_index] + 11, row_to_y_dict[row_index] + 10, "black", 6)

    draw_horizontal_line(col_to_x_dict[col_index] + 3, row_to_y_dict[row_index] + 9, "black", 6)
    draw_horizontal_line(col_to_x_dict[col_index] + 11, row_to_y_dict[row_index] + 9, "black", 6)

    draw_horizontal_line(col_to_x_dict[col_index] + 4, row_to_y_dict[row_index] + 8, "black", 12)

    draw_horizontal_line(col_to_x_dict[col_index] + 4, row_to_y_dict[row_index] + 7, "black", 2)
    draw_horizontal_line(col_to_x_dict[col_index] + 8, row_to_y_dict[row_index] + 7, "black", 4)
    draw_horizontal_line(col_to_x_dict[col_index] + 14, row_to_y_dict[row_index] + 7, "black", 2)

    draw_horizontal_line(col_to_x_dict[col_index] + 5, row_to_y_dict[row_index] + 6, "black", 1)
    draw_horizontal_line(col_to_x_dict[col_index] + 8, row_to_y_dict[row_index] + 6, "black", 4)
    draw_horizontal_line(col_to_x_dict[col_index] + 14, row_to_y_dict[row_index] + 6, "black", 1)

    draw_horizontal_line(col_to_x_dict[col_index] + 5, row_to_y_dict[row_index] + 5, "black", 10)
    draw_horizontal_line(col_to_x_dict[col_index] + 7, row_to_y_dict[row_index] + 4, "black", 6)
    draw_horizontal_line(col_to_x_dict[col_index] + 9, row_to_y_dict[row_index] + 3, "black", 2)

    check_square_selected(row_index, col_index)


def draw_correct_flag(row_index, col_index):
    """Draws on top of current flags to be green

    Keyword arguments:
    row_index -- the row index
    col_index -- the col index
    """

    row_to_y_dict = {y: y * -20 + 180 for y in range(0, 20)}
    col_to_x_dict = {x: x * 20 - 200 for x in range(0, 20)}

    draw_horizontal_line(col_to_x_dict[col_index] + 9, row_to_y_dict[row_index] + 9, "green", 2)
    draw_horizontal_line(col_to_x_dict[col_index] + 7, row_to_y_dict[row_index] + 10, "green", 4)
    draw_horizontal_line(col_to_x_dict[col_index] + 5, row_to_y_dict[row_index] + 11, "green", 6)
    draw_horizontal_line(col_to_x_dict[col_index] + 4, row_to_y_dict[row_index] + 12, "green", 7)
    draw_horizontal_line(col_to_x_dict[col_index] + 4, row_to_y_dict[row_index] + 13, "green", 7)
    draw_horizontal_line(col_to_x_dict[col_index] + 5, row_to_y_dict[row_index] + 14, "green", 6)
    draw_horizontal_line(col_to_x_dict[col_index] + 7, row_to_y_dict[row_index] + 15, "green", 4)
    draw_horizontal_line(col_to_x_dict[col_index] + 9, row_to_y_dict[row_index] + 16, "green", 2)

    check_square_selected(row_index, col_index)


def draw_exploded_bomb(row_index, col_index):
    """Draws a normal bomb with a red background

    Keyword arguments:
    row_index -- the row index
    col_index -- the col index
    """

    row_to_y_dict = {y: y * -20 + 180 for y in range(0, 20)}
    col_to_x_dict = {x: x * 20 - 200 for x in range(0, 20)}

    for row in range(0, 19):
        draw_horizontal_line(col_to_x_dict[col_index] + 1, row_to_y_dict[row_index] + 1 + row, "red", 19)

    draw_bomb(row_index, col_index)

    check_square_selected(row_index, col_index)


def draw_number(row_index, col_index, number):
    """Draws a number on a given grid point

    Keyword arguments:
    row_index -- the row index
    col_index -- the col index
    number -- the number being drawn
    """
    row_to_y_dict = {y: y * -20 + 180 for y in range(0, 20)}
    col_to_x_dict = {x: x * 20 - 200 for x in range(0, 20)}

    turtle_object.color("black")
    turtle_object.setheading(0)
    draw_clear(row_index, col_index)

    if number == "0":
        draw_clear(row_index, col_index)

    else:
        draw_symbol(col_to_x_dict[col_index], row_to_y_dict[row_index], number)

    check_square_selected(row_index, col_index)


def draw_clear(row_index, col_index):
    """Draws a clear square on the given grid point

    Keyword arguments:
    row_index -- the row index
    col_index -- the col index
    """

    row_to_y_dict = {y: y * -20 + 180 for y in range(0, 20)}
    col_to_x_dict = {x: x * 20 - 200 for x in range(0, 20)}

    for row in range(0, 19):
        draw_horizontal_line(col_to_x_dict[col_index] + 1, row_to_y_dict[row_index] + 1 + row, "lightgray", 19)

    check_square_selected(row_index, col_index)


def square_being_clicked(x, y):
    """Returns the row index and the col index for a given coordinate

    Keyword arguments:
    x -- the x coordinate
    y -- the y coordinate
    """

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
    """Draws a letter of the alphabet at the given coordinates

    Keyword arguments:
    start_x -- the starting x coordinate
    start_y -- the starting y coordinate
    letter -- the letter being drawn
    """

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
    """Draws the button used to display the remaining mines"""

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
    """Draws the button used to start a new game"""
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
    """Draws the beginning board and buttons"""
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
    game_board.selected_square.draw_selected_square()


def left_click(x, y):
    """Handles the event when the left mouse button is clicked

    Keyword arguments:
    x -- the x coordinate that was clicked
    y -- the y coordinate that was clicked
    """

    square_coords = square_being_clicked(x, y)
    if square_coords[0] == 22 and square_coords[1] == 22:

        game_board.new_board()
        draw_basic_board()
        window.update()
        return

    if game_board.game_over:
        return

    if square_coords[0] == 21 or square_coords[1] == 21:
        return

    if square_coords[0] == 23 or square_coords[1] == 23:
        draw_remaining_mines_number(game_board.total_mines - game_board.number_of_flags)
        window.update()

        return

    if game_board.new_game:
        while game_board.hidden_board[square_coords[0]][square_coords[1]] != "0":
            game_board.new_board()
        game_board.new_game = False

        game_board.clear_zeros(square_coords[0], square_coords[1])
        draw_remaining_mines_number(game_board.total_mines - game_board.number_of_flags)

    if game_board.user_board[square_coords[0]][square_coords[1]] == "U":
        if game_board.user_board[square_coords[0]][square_coords[1]] == "F":
            pass

        elif game_board.hidden_board[square_coords[0]][square_coords[1]] == "B":
            for row_index in range(0, 20):
                for col_index in range(0, 20):
                    if game_board.hidden_board[row_index][col_index] == "B" and \
                            game_board.user_board[row_index][col_index] != "F":
                        draw_bomb(row_index, col_index)

                    elif game_board.hidden_board[row_index][col_index] == "B" and \
                            game_board.user_board[row_index][col_index] == "F":
                        draw_correct_flag(row_index, col_index)

            draw_exploded_bomb(square_coords[0], square_coords[1])

            game_board.game_over = True

        elif game_board.hidden_board[square_coords[0]][square_coords[1]] == "0":
            game_board.clear_zeros(square_coords[0], square_coords[1])

            if game_board.check_win():
                game_board.game_over = True
                draw_win()

        else:
            game_board.user_board[square_coords[0]][square_coords[1]] = \
                game_board.hidden_board[square_coords[0]][square_coords[1]]

            draw_number(square_coords[0], square_coords[1], game_board.user_board[square_coords[0]][square_coords[1]])

            if game_board.check_win():
                game_board.game_over = True
                draw_win()

    window.update()


def middle_click(x, y):
    """Handles the event when the middle mouse button is clicked

    Keyword arguments:
    x -- the x coordinate that was clicked
    y -- the y coordinate that was clicked
    """
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
                                draw_bomb(row_index, col_index)

                            elif game_board.hidden_board[row_index][col_index] == "B" and \
                                    game_board.user_board[row_index][col_index] == "F":
                                draw_correct_flag(row_index, col_index)

                    draw_exploded_bomb(row_shifted, col_shifted)

                    game_board.game_over = True
                    window.update()

                    return

                elif game_board.hidden_board[row_shifted][col_shifted] == "0":
                    game_board.clear_zeros(row_shifted, col_shifted)

                else:
                    game_board.user_board[row_shifted][col_shifted] = game_board.hidden_board[row_shifted][col_shifted]

                    draw_number(row_shifted, col_shifted, game_board.hidden_board[row_shifted][col_shifted])

                if game_board.check_win():
                    game_board.game_over = True
                    draw_win()

    window.update()


def right_click(x, y):
    """Handles the event when the right mouse button is clicked

    Keyword arguments:
    x -- the x coordinate that was clicked
    y -- the y coordinate that was clicked
    """
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

        draw_flag(square_coords[0], square_coords[1])
        game_board.number_of_flags += 1

        # draw_remaning_mines_number(game_board.total_mines - game_board.number_of_flags)

        if game_board.check_win():
            game_board.game_over = True
            draw_win()

    elif game_board.user_board[square_coords[0]][square_coords[1]] == "F":
        game_board.user_board[square_coords[0]][square_coords[1]] = "U"

        draw_unknown(square_coords[0], square_coords[1])
        game_board.number_of_flags -= 1

    window.update()


def w_key():
    """Handles the event when the "w" key is pressed"""
    if game_board.game_over:
        return
    game_board.move_selected_square("up")
    window.update()


def a_key():
    """Handles the event when the "a" key is pressed"""
    if game_board.game_over:
        return
    game_board.move_selected_square("left")
    window.update()


def s_key():
    """Handles the event when the "s" key is pressed"""
    if game_board.game_over:
        return
    game_board.move_selected_square("down")
    window.update()


def d_key():
    """Handles the event when the "d" key is pressed"""
    if game_board.game_over:
        return
    game_board.move_selected_square("right")
    window.update()


def i_key():
    """Handles the event when the "i" key is pressed"""
    row_to_y_dict = {y: y * -20 + 180 for y in range(0, 20)}
    col_to_x_dict = {x: x * 20 - 200 for x in range(0, 20)}

    row_index = game_board.selected_square.location[0]
    col_index = game_board.selected_square.location[1]

    left_click(col_to_x_dict[col_index] + 10, row_to_y_dict[row_index] + 10)

    window.update()


def o_key():
    """Handles the event when the "o" key is pressed"""
    row_to_y_dict = {y: y * -20 + 180 for y in range(0, 20)}
    col_to_x_dict = {x: x * 20 - 200 for x in range(0, 20)}

    row_index = game_board.selected_square.location[0]
    col_index = game_board.selected_square.location[1]

    right_click(col_to_x_dict[col_index] + 10, row_to_y_dict[row_index] + 10)

    window.update()


def p_key():
    """Handles the event when the "p" key is pressed"""
    row_to_y_dict = {y: y * -20 + 180 for y in range(0, 20)}
    col_to_x_dict = {x: x * 20 - 200 for x in range(0, 20)}

    row_index = game_board.selected_square.location[0]
    col_index = game_board.selected_square.location[1]

    middle_click(col_to_x_dict[col_index] + 10, row_to_y_dict[row_index] + 10)

    window.update()


def main():
    window.setup(500, 500)
    window.tracer(0, 0)
    window.title("Bomb Locatorino")
    window.bgcolor("darkgray")

    turtle_object.speed(0)
    turtle_object.pensize(1)
    turtle_object.hideturtle()

    draw_basic_board()

    window.update()

    window.onscreenclick(left_click, btn=1)
    window.onscreenclick(middle_click, btn=2)
    window.onscreenclick(right_click, btn=3)

    window.onkey(w_key, key="w")
    window.onkey(a_key, key="a")
    window.onkey(s_key, key="s")
    window.onkey(d_key, key="d")

    window.onkey(i_key, key="i")
    window.onkey(o_key, key="o")
    window.onkey(p_key, key="p")

    window.listen()
    window.mainloop()


if __name__ == "__main__":
    turtle_object = turtle.Turtle()
    window = turtle.Screen()
    game_board = GameBoard()
    main()
else:
    turtle_object = turtle.Turtle()
    window = turtle.Screen()
    game_board = GameBoard()
    main()