LOC = {"canto": [(0, 0), (0, 2), (2, 0), (2, 2)],
       "cruz": [(0, 1), (1, 0), (1, 2), (2, 1)]}
CENTER = (1, 1)


class Board():
    def __init__(self):
        self.winner = None
        self.board = [["-", "-", "-"],
                      ["-", "-", "-"],
                      ["-", "-", "-"]]

    def check_diagonals(self, row, col):
        if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[0][0] == \
                self.board[row][col]:
            return True
        if self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0] and self.board[0][2] == \
                self.board[row][col]:
            return True
        return False

    def check_row(self, row, col):
        for column in range(3):
            if self.board[row][column] != self.board[row][col]:
                return False
        return True

    def check_column(self, row, col):
        for r in range(3):
            if self.board[r][col] != self.board[row][col]:
                return False
        return True

    def done(self, row, col):
        if self.check_diagonals(row, col) or self.check_row(row, col) or self.check_column(row, col):
            self.winner = self.board[row][col]
            return True
        return False


class Ultimate_board():
    def __init__(self, p_one, p_two):
        self.board = [[Board(), Board(), Board()],
                      [Board(), Board(), Board()],
                      [Board(), Board(), Board()]]
        self.p_one = p_one
        self.p_two = p_two
        self.winner = None

    def display_board(self):
        string = "+---------------+---------------+---------------+\n"
        for row in range(0, 3):
            for board_row in range(0, 3):
                for col in range(0, 3):
                    if col == 0:
                        string += "|   "
                    for board_col in range(0, 3):
                        string += str(self.board[row][col].board[board_row][board_col])
                        if board_col != 2:
                            string += " | "
                    string += "   |   "
                if board_row != 2:
                    string += "\n|   --+---+--   |   --+---+--   |   --+---+--   |\n"
                else:
                    string += "\n+---------------+---------------+---------------+\n"

        print(string)

    def display_wins(self):
        string = "+---+---+---+\n"
        for row in range(0, 3):
            string += "|"
            for col in range(0, 3):
                if self.board[row][col].winner:
                    string += " " + self.board[row][col].winner
                else:
                    string += " -"
                string += " |"
            string += "\n+---+---+---+\n"
        print(string)

    def check_diagonals(self, row, col):
        if self.board[0][0].winner == self.board[1][1].winner and self.board[1][1].winner == self.board[2][2].winner and \
                self.board[0][0].winner == self.board[row][col].winner:
            return True
        if self.board[0][2].winner == self.board[1][1].winner and self.board[1][1].winner == self.board[2][0].winner and \
                self.board[0][2].winner == self.board[row][col].winner:
            return True
        return False

    def check_row(self, row, col):
        for column in range(3):
            if self.board[row][column].winner != self.board[row][col].winner:
                return False
        return True

    def check_column(self, row, col):
        for r in range(3):
            if self.board[r][col].winner != self.board[row][col].winner:
                return False
        return True

    def play(self):
        p_one_play = True
        freebie = False
        row = None
        col = None
        board_row = None
        board_col = None
        play_made = False
        while not self.winner:
            if p_one_play:
                print("Player 1")
            else:
                print("Player 2")
            if not row and not col and row != 0 and col != 0:
                print("Select a board")
                row = int(input("Row: "))
                col = int(input("Column: "))
            if self.board[row][col].winner:
                freebie = True
            while freebie:
                print("Freebie! Select a board")
                row = int(input("Row: "))
                col = int(input("Column: "))
                if not self.board[row][col].winner:
                    freebie = False
            while not play_made:
                board_row = int(input("Select row: "))
                board_col = int(input("Select col: "))
                if self.board[row][col].board[board_row][board_col] == "-":
                    if p_one_play:
                        self.board[row][col].board[board_row][board_col] = self.p_one
                        if self.board[row][col].check_column(board_row, board_col) or self.board[row][col].check_row(
                                board_row, board_col) or self.board[row][col].check_diagonals(board_row, board_col):
                            self.board[row][col].winner = self.p_one
                        # if self.check_column(row, col) or self.check_row(
                        #         row, col) or self.check_diagonals(row, col):
                        #     self.winner = self.p_one
                    else:
                        self.board[row][col].board[board_row][board_col] = self.p_two
                        if self.board[row][col].check_column(board_row, board_col) or self.board[row][col].check_row(
                                board_row, board_col) or self.board[row][col].check_diagonals(board_row, board_col):
                            self.board[row][col].winner = self.p_two
                        # if self.check_column(row, col) or self.check_row(
                        #         row, col) or self.check_diagonals(row, col):
                        #     self.winner = self.p_two
                    play_made = True
                else:
                    print("Spot taken. Try again.")
            row = board_row
            col = board_col
            if p_one_play:
                p_one_play = False
            else:
                p_one_play = True
            play_made = False
            self.display_board()
            self.display_wins()


def main():
    p_one = input("Player One, X or O: ")
    p_two = None
    while p_one != "X" and p_one != "O":
        print("Invalid letter")
        p_one = input("Player One, X or O: ")
    if p_one == "X":
        p_two = "O"
        print("Player 1: X")
        print("Player 2: O")
    else:
        p_two = "X"
        print("Player 1: O")
        print("Player 2: X")
    print("Game Start!")
    ult_board = Ultimate_board(p_one, p_two)
    ult_board.play()


main()
