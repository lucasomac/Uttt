"""
@author: Lucas de Oliveira Macedo
@author: Diogo
@author: Jeferson
"""
import random
import sys
import os
import pickle
import time


class Tabuleiro:
    def __init__(self, utlimate_tic_tac_toe, tic_tac_toe, quadro_para_jogar):
        self.utlimate_tic_tac_toe = utlimate_tic_tac_toe
        self.tic_tac_toe = tic_tac_toe
        self.quadro_para_jogar = quadro_para_jogar


class UltimateTicTacToe:
    __CASA_DISPONIVEL = "0"
    __NUM_COLUNA = 3
    __NUM_LINHA = 3
    __EMPATE = "+"

    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2

        ultimate_tic_tac_toe = []
        for a in range(9):
            ultimate_tic_tac_toe.append([self.__CASA_DISPONIVEL] * (self.__NUM_COLUNA * 3))

        tic_tac_toe = [self.__CASA_DISPONIVEL] * 9
        self.tabuleiro = Tabuleiro(ultimate_tic_tac_toe, tic_tac_toe, None)

        self.player_turn = random.choice([self.player_1, self.player_2])

    def play(self):
        self.player_1.startGame()
        self.player_2.startGame()
        movimento_player_anterior = None
        while True:
            if self.player_turn == self.player_1:
                p1 = self.player_1
                p2 = self.player_2
            else:
                p1 = self.player_2
                p2 = self.player_1

            self.chars = (p1.char, p2.char)

            move = p1.move(self.tabuleiro)
            movimento_ilegal = False
            for a in range(move):
                if not a in range(9):
                    movimento_ilegal = True
            if self.tabuleiro.tic_tac_toe[move[0]] != self.__CASA_DISPONIVEL:
                movimento_ilegal = True
            if self.tabuleiro.utlimate_tic_tac_toe[move[0]][move[1]] != self.__CASA_DISPONIVEL:
                illegalMove = True
            if movimento_player_anterior and move[0] != movimento_player_anterior:
                illegalMove = True
            if movimento_ilegal:
                p1.reward(-99, self.tabuleiro)
                # if self.verbose:
                #     print("Illegal move")
                break
            self.tabuleiro.utlimate_tic_tac_toe[move[0]][move[1]] = p1.char
            self.update_tic_tac_toe()
            movimento_player_anterior = move[1]
            if self.tabuleiro.tic_tac_toe[movimento_player_anterior] != self.__CASA_DISPONIVEL:
                movimento_player_anterior = None
            self.tabuleiro.SubBoardToBePlayed = movimento_player_anterior
            result = self.the_end()
            if result[0]:
                if result[1] == self.chars[0]:
                    # if self.verbose:
                    #     self._print()
                    #     print("\n {} {} won!".format(player.type, player.char))
                    p1.reward(10, self.tabuleiro)
                    p2.reward(-10, self.tabuleiro)
                    break
                if result[1] == self.chars[1]:
                    # if self.verbose:
                    #     self._print()
                    #     print("\n {} {} won!".format(otherplayer.type, otherplayer.char))
                    p2.reward(10, self.tabuleiro)
                    p1.reward(-10, self.tabuleiro)
                    break
                else:
                    # if self.verbose:
                    #     self._print()
                    #     print("\n", "Tie!")
                    p1.reward(0.5, self.tabuleiro)
                    p2.reward(0.5, self.tabuleiro)
                    break
            else:
                p2.reward(0, self.tabuleiro)
                p1.reward(0, self.tabuleiro)

            # switch turns
            self.player1turn = not self.player1turn

    def update_tic_tac_toe(self):
        # check wins on sub-tabuleiros and transfer to miniboard
        for tic_tac_toes in range(len(self.tabuleiro.utlimate_tic_tac_toe)):
            for char in self.chars:
                if self.tic_tac_toe_win(self.tabuleiro.utlimate_tic_tac_toe[tic_tac_toes], char):
                    self.tabuleiro.tic_tac_toe[tic_tac_toes] = char
            if self.tabuleiro.utlimate_tic_tac_toe[tic_tac_toes].count(self.__CASA_DISPONIVEL) == 0:
                self.tabuleiro.tic_tac_toe[tic_tac_toes] = self.__EMPATE

    def tic_tac_toe_win(self, board, char):
        for a, b, c in [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                        (0, 3, 6), (1, 4, 7), (2, 5, 8),
                        (0, 4, 8), (2, 4, 6)]:
            if char == board[a] == board[b] == board[c]:
                return True
        return False

    def the_end(self):

        for char in self.chars:
            if self.tic_tac_toe_win(self.tabuleiro.tic_tac_toe, char):
                return (True, char)
        if self.tabuleiro.tic_tac_toe.count(self.__CASA_DISPONIVEL) > 0:
            return (False, self.__CASA_DISPONIVEL)
        else:
            return (True, self.__CASA_DISPONIVEL)


class Player():

    def __init__(self, char="O"):
        self.type = "HUMANO"
        self.char = char

    def startGame(self):
        pass

    def move(self, ultimate_tic_tac_toe):
        while True:
            try:
                move = input("(Entre com dois numeros separado por um espaço(entre 0 e 8 cada um) ou '-' para sair) ")

                if move == '-':
                    sys.exit(0)
                if len(move) != 2:
                    raise ValueError
                # print("Move after split: ", move)

            except ValueError:
                print("Movimento invalido, tente novamente!")
            else:
                break
            finally:
                print("____________________________")
        return (int(move[0]), int(move[1]))

    def reward(self, value, tabuleiro):
        pass
