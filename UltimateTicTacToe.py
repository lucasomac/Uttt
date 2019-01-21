import random

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
        if self.tabuleiro[0][0] == self.tabuleiro[1][1] == self.tabuleiro[2][2] == self.tabuleiro[row][col]:
            return True
        if self.tabuleiro[0][2] == self.tabuleiro[1][1] == self.tabuleiro[2][0] == self.tabuleiro[row][col]:
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

    def get_movimentos_disponiveis(self):
        disponiveis = []
        for linha in range(3):
            for coluna in range(3):
                if self.tabuleiro[linha][coluna] == "-":
                    disponiveis.append((linha, coluna))
        return disponiveis


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
        if self.tabuleiro[0][0].vencedor == self.tabuleiro[1][1].vencedor == self.tabuleiro[2][2].vencedor == \
                self.tabuleiro[row][col].vencedor:
            return True
        if self.tabuleiro[0][2].vencedor == self.tabuleiro[1][1].vencedor == self.tabuleiro[2][0].vencedor == \
                self.tabuleiro[row][col].vencedor:
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

    def get_movimentos_disponiveis(self):
        disponiveis = []
        for linha in range(3):
            for coluna in range(3):
                if not self.tabuleiro[linha][coluna].vencedor:
                    disponiveis.append((linha, coluna))
        return disponiveis

    def play(self):
        p_one_play = True
        bonus = False
        row = None
        col = None
        board_row = None
        board_col = None
        local_disponivel = False
        # Enquanto nao houver vencedor no tabuleiro maior
        while not self.vencedor:
            if p_one_play:
                print("Player 1")
                # Se gor um humano ele pede os dados para fazer movimento
                if isinstance(self.p1, Player):
                    # Se for a primeira jogada ele pede qual tabuleiro menor deseja jogar
                    if not row and not col and row != 0 and col != 0:
                        print("Selecione o tabuleiro Menor")
                        row = int(input("Linha: "))
                        col = int(input("Coluna: "))
                        # Se o tabuleiro menor ja foi ganho, voce pode escolher outro.
                    if self.tabuleiro[row][col].vencedor:
                        bonus = True
                    while bonus:
                        print("Bonus! Selecione um tabuleiro Menor")
                        row = int(input("Linha: "))
                        col = int(input("Coluna: "))
                        # Verifica se o novo tabuleiro menor escolhido nao teve vencedor.
                        if not self.tabuleiro[row][col].vencedor:
                            bonus = False
                    while not local_disponivel:
                        board_row = int(input("Selecione a linha do movimento: "))
                        board_col = int(input("Selecione a coluna do movimento: "))
                        if self.tabuleiro[row][col].tabuleiro[board_row][board_col] == "-":
                            self.tabuleiro[row][col].tabuleiro[board_row][board_col] = self.p1.symbol
                            # Verifica vitoria no tabuleiro menor
                            self.tabuleiro[row][col].done(board_row, board_col)
                            # Verifica vitoria no tabuleiro maior
                            self.done(row, col)
                            local_disponivel = True
                        else:
                            print("Movimento nao disponivel. Tente novamente.")
                    row = board_row
                    col = board_col
                    p_one_play = False
                    local_disponivel = False
                if isinstance(self.p1, PlayerRandom):
                    if (not row and not col and row != 0 and col != 0) or self.tabuleiro[row][col].vencedor:
                        row = (random.choice(self.get_movimentos_disponiveis()))[0]
                        col = (random.choice(self.get_movimentos_disponiveis()))[1]
                    board_row = (random.choice(self.tabuleiro[row][col].get_movimentos_disponiveis()))[0]
                    board_col = (random.choice(self.tabuleiro[row][col].get_movimentos_disponiveis()))[1]
                    # print(board_row, board_col)
                    self.tabuleiro[row][col].tabuleiro[board_row][board_col] = self.p1.symbol
                    self.tabuleiro[row][col].done(board_row, board_col)
                    self.done(row, col)
                    row = board_row
                    col = board_col
                    p_one_play = False
            else:
                print("Player 2")
                if isinstance(self.p2, Player):
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
                            self.tabuleiro[row][col].tabuleiro[board_row][board_col] = self.p2.symbol
                            self.tabuleiro[row][col].done(board_row, board_col)
                            self.done(row, col)
                            local_disponivel = True
                        else:
                            print("Movimento nao disponivel. Tente novamente.")
                    row = board_row
                    col = board_col
                    p_one_play = True
                    local_disponivel = False
                if isinstance(self.p2, PlayerRandom):
                    if (not row and not col and row != 0 and col != 0) or self.tabuleiro[row][col].vencedor:
                        row = (random.choice(self.get_movimentos_disponiveis()))[0]
                        col = (random.choice(self.get_movimentos_disponiveis()))[1]
                    board_row = (random.choice(self.tabuleiro[row][col].get_movimentos_disponiveis()))[0]
                    board_col = (random.choice(self.tabuleiro[row][col].get_movimentos_disponiveis()))[1]
                    self.tabuleiro[row][col].tabuleiro[board_row][board_col] = self.p2.symbol
                    self.tabuleiro[row][col].done(board_row, board_col)
                    self.done(row, col)
                    row = board_row
                    col = board_col
                    p_one_play = True
            self.print_tabuleiro()
            self.print_vitorias()


def main(p1, p2):
    p_one = p1
    p_two = p2
    if p_one.symbol == "X":
        print("Player 1: X")
        print("Player 2: O")
    else:
        print("Player 1: O")
        print("Player 2: X")
    print("Game Start!")
    ult_board = Ultimate_board(p_one, p_two)
    ult_board.play()


class Player():

    def __init__(self, symbol, tipo="HUMANO"):
        self.symbol = symbol
        self.tipo = tipo


class Minimax(Player):
    recompensa = 0

    def __init__(self):
        self.tipo = "AI"


class PlayerRandom():

    def __init__(self, symbol):
        self.tipo = "RANDOM"
        self.symbol = symbol


# Defina dois players para iniciar o jogo. Para jogar contra a maquina defina um player na classe Player e um na classe PlayerRandom
p1 = PlayerRandom("X")
p2 = PlayerRandom("O")

main(p1, p2)
