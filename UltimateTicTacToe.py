LOC = {"canto": [(0, 0), (0, 2), (2, 0), (2, 2)],
       "cruz": [(0, 1), (1, 0), (1, 2), (2, 1)]}
CENTER = (1, 1)


class Tabuleiro():
    def __init__(self):
        self.vencedor = None
        self.tabuleiro = [["-", "-", "-"],
                          ["-", "-", "-"],
                          ["-", "-", "-"]]

    def check_diagonals(self, row, col):
        if self.tabuleiro[0][0] == self.tabuleiro[1][1] and self.tabuleiro[1][1] == self.tabuleiro[2][2] and \
                self.tabuleiro[0][0] == \
                self.tabuleiro[row][col]:
            return True
        if self.tabuleiro[0][2] == self.tabuleiro[1][1] and self.tabuleiro[1][1] == self.tabuleiro[2][0] and \
                self.tabuleiro[0][2] == \
                self.tabuleiro[row][col]:
            return True
        return False

    def check_row(self, row, col):
        for coluna in range(3):
            if self.tabuleiro[row][coluna] != self.tabuleiro[row][col]:
                return False
        return True

    def check_column(self, row, col):
        for linha in range(3):
            if self.tabuleiro[linha][col] != self.tabuleiro[row][col]:
                return False
        return True

    def done(self, row, col):
        if self.check_diagonals(row, col) or self.check_row(row, col) or self.check_column(row, col):
            self.vencedor = self.tabuleiro[row][col]
            return True
        return False


class Ultimate_board():
    def __init__(self, p1, p2):
        self.tabuleiro = [[Tabuleiro(), Tabuleiro(), Tabuleiro()],
                          [Tabuleiro(), Tabuleiro(), Tabuleiro()],
                          [Tabuleiro(), Tabuleiro(), Tabuleiro()]]
        self.p1 = p1
        self.p2 = p2
        self.vencedor = None

    def print_tabuleiro(self):
        string = "+---------------+---------------+---------------+\n"
        for linha in range(0, 3):
            for tabuleiro_linha in range(0, 3):
                for coluna in range(0, 3):
                    if coluna == 0:
                        string += "|   "
                    for tabuleiro_coluna in range(0, 3):
                        string += str(self.tabuleiro[linha][coluna].tabuleiro[tabuleiro_linha][tabuleiro_coluna])
                        if tabuleiro_coluna != 2:
                            string += " | "
                    string += "   |   "
                if tabuleiro_linha != 2:
                    string += "\n|   --+---+--   |   --+---+--   |   --+---+--   |\n"
                else:
                    string += "\n+---------------+---------------+---------------+\n"

        print(string)

    def print_vitorias(self):
        string = "+---+---+---+\n"
        for linha in range(0, 3):
            string += "|"
            for coluna in range(0, 3):
                if self.tabuleiro[linha][coluna].vencedor:
                    string += " " + self.tabuleiro[linha][coluna].vencedor
                else:
                    string += " -"
                string += " |"
            string += "\n+---+---+---+\n"
        print(string)

    def check_diagonals(self, row, col):
        if self.tabuleiro[0][0].vencedor == self.tabuleiro[1][1].vencedor and self.tabuleiro[1][1].vencedor == \
                self.tabuleiro[2][
                    2].vencedor and \
                self.tabuleiro[0][0].vencedor == self.tabuleiro[row][col].vencedor:
            return True
        if self.tabuleiro[0][2].vencedor == self.tabuleiro[1][1].vencedor and self.tabuleiro[1][1].vencedor == \
                self.tabuleiro[2][
                    0].vencedor and \
                self.tabuleiro[0][2].vencedor == self.tabuleiro[row][col].vencedor:
            return True
        return False

    def check_row(self, row, col):
        for coluna in range(3):
            if self.tabuleiro[row][coluna].vencedor != self.tabuleiro[row][col].vencedor:
                return False
        return True

    def check_column(self, row, col):
        for linha in range(3):
            if self.tabuleiro[linha][col].vencedor != self.tabuleiro[row][col].vencedor:
                return False
        return True

    def done(self, row, col):
        if self.check_diagonals(row, col) or self.check_row(row, col) or self.check_column(row, col):
            self.vencedor = self.tabuleiro[row][col].vencedor
            return True
        return False

    def play(self):
        p_one_play = True
        bonus = False
        row = None
        col = None
        board_row = None
        board_col = None
        local_disponivel = False
        while not self.vencedor:
            if p_one_play:
                print("Player 1")
            else:
                print("Player 2")
            if not row and not col and row != 0 and col != 0:
                print("Selecione o tabuleiro Menor")
                row = int(input("Linha: "))
                col = int(input("Coluna: "))
            if self.tabuleiro[row][col].vencedor:
                bonus = True
            while bonus:
                print("Bonus! Selecione um tabuleiro Menor")
                row = int(input("Linha: "))
                col = int(input("Coluna: "))
                if not self.tabuleiro[row][col].vencedor:
                    bonus = False
            while not local_disponivel:
                board_row = int(input("Selecione a linha do movimento: "))
                board_col = int(input("Selecione a coluna do movimento: "))
                if self.tabuleiro[row][col].tabuleiro[board_row][board_col] == "-":
                    if p_one_play:
                        self.tabuleiro[row][col].tabuleiro[board_row][board_col] = self.p1
                        self.tabuleiro[row][col].done(board_row, board_col)
                        self.done(row, col)
                    else:
                        self.tabuleiro[row][col].tabuleiro[board_row][board_col] = self.p2
                        self.tabuleiro[row][col].done(board_row, board_col)
                        self.done(row, col)
                    local_disponivel = True
                else:
                    print("Movimento nao disponivel. Tente novamente.")
            row = board_row
            col = board_col
            if p_one_play:
                p_one_play = False
            else:
                p_one_play = True
            local_disponivel = False
            self.print_tabuleiro()
            self.print_vitorias()


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
