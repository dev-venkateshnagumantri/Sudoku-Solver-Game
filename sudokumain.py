from sudokutools import valid, solve, find_empty
from copy import deepcopy
from sys import exit
import pygame
import time
import random
pygame.init()


def generate():

    while True:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        board = [[0 for i in range(9)] for j in range(9)]

        for i in range(9):
            for j in range(9):
                if random.randint(1, 10) >= 5:
                    board[i][j] = random.randint(1, 9) 
                    if valid(board, (i, j), board[i][j]):
                        continue
                    else:
                        board[i][j] = 0
        partialBoard = deepcopy(board)  
        if solve(board):
            return partialBoard


class Board:

    def __init__(self, window):
        self.board = generate()
        self.solvedBoard = deepcopy(self.board)
        solve(self.solvedBoard)
        self.tiles = [[Tile(self.board[i][j], window, i * 60, j * 60)
                      for j in range(9)] for i in range(9)]
        self.window = window

    def draw_board(self):

        for i in range(9):
            for j in range(9):
                if j % 3 == 0 and j != 0:  
                    pygame.draw.line(self.window, (0, 0, 0), (j // 3
                            * 180, 0), (j // 3 * 180, 540), 4)

                if i % 3 == 0 and i != 0: 
                    pygame.draw.line(self.window, (0, 0, 0), (0, i // 3
                            * 180), (540, i // 3 * 180), 4)

                self.tiles[i][j].draw((0, 0, 0), 1)

                if self.tiles[i][j].value != 0:  
                    self.tiles[i][j].display(self.tiles[i][j].value,
                            (21 + j * 60, 16 + i * 60), (0, 0, 0))  


        pygame.draw.line(self.window, (0, 0, 0), (0, (i + 1) // 3
                         * 180), (540, (i + 1) // 3 * 180), 4)

    def deselect(self, tile):

        for i in range(9):
            for j in range(9):
                if self.tiles[i][j] != tile:
                    self.tiles[i][j].selected = False

    def redraw(
        self,
        keys,
        wrong,
        time,
        ):

        self.window.fill((255, 255, 255))
        self.draw_board()
        for i in range(9):
            for j in range(9):
                if self.tiles[j][i].selected: 
                    self.tiles[j][i].draw((50, 205, 50), 4)
                elif self.tiles[i][j].correct:

                    self.tiles[j][i].draw((34, 139, 34), 4)
                elif self.tiles[i][j].incorrect:

                    self.tiles[j][i].draw((255, 0, 0), 4)

        if len(keys) != 0:  
            for value in keys:
                self.tiles[value[0]][value[1]].display(keys[value], (21
                        + value[0] * 60, 16 + value[1] * 60), (128,
                        128, 128))

        if wrong > 0:
            font = pygame.font.SysFont('Bauhaus 93', 30) 
            text = font.render('X', True, (255, 0, 0))
            self.window.blit(text, (10, 554))

            font = pygame.font.SysFont('Bahnschrift', 40)  
            text = font.render(str(wrong), True, (0, 0, 0))
            self.window.blit(text, (32, 542))

        font = pygame.font.SysFont('Bahnschrift', 40)  
        text = font.render(str(time), True, (0, 0, 0))
        self.window.blit(text, (388, 542))
        pygame.display.flip()

    def visualSolve(self, wrong, time):

        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                exit()

        empty = find_empty(self.board)
        if not empty:
            return True

        for nums in range(9):
            if valid(self.board, (empty[0], empty[1]), nums + 1):
                self.board[empty[0]][empty[1]] = nums + 1
                self.tiles[empty[0]][empty[1]].value = nums + 1
                self.tiles[empty[0]][empty[1]].correct = True
                pygame.time.delay(63)  
                self.redraw({}, wrong, time)

                if self.visualSolve(wrong, time):
                    return True

                self.board[empty[0]][empty[1]] = 0
                self.tiles[empty[0]][empty[1]].value = 0
                self.tiles[empty[0]][empty[1]].incorrect = True
                self.tiles[empty[0]][empty[1]].correct = False
                pygame.time.delay(63)
                self.redraw({}, wrong, time)



pygame.quit()