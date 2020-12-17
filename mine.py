import random
import sys
import pygame
import numpy


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.colors = [(255, 255, 255), "white"]

    # настройка внешнего вида
    def generate(self):
        self.board = [[1] * self.width for _ in range(self.height)]

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        pass

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        for i in range(self.height):
            for j in range(self.width):
                if ((x > j * self.cell_size + self.top) and (x <= (j + 1) * self.cell_size + self.top) and
                        (y > i * self.cell_size + self.left) and ((y <= (i + 1) * self.cell_size + self.left))):
                    r = i, j
                    return r

    def on_click(self, cell):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


class Minesweeper(Board):
    def __init__(self, width, height, num_mins=10):
        super(Minesweeper, self).__init__(width, height)
        self.num_mins = num_mins
        self.generate()

    def generate(self):
        self.board = [10] * self.num_mins + [0] * (self.width * self.height - self.num_mins)
        random.shuffle(self.board)
        self.board = numpy.array(self.board)
        self.board = self.board.reshape(self.height, self.width)
        self.is_showing = [[self.board[i][j] == 10 for j in range(len(self.board[i]))] for i in range(len(self.board))]

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, ({10: "red"}).get(self.board[i, j], "white"), (self.left + self.cell_size * i,
                                                                                       self.top + self.cell_size * j,
                                                                                       self.cell_size,
                                                                                       self.cell_size),
                                 width=({10: 0}).get(self.board[i][j], 1))
                if self.is_showing[i][j] and self.board[i][j] != 10:
                    draw_text(sc, str(self.board[i][j]), 16, self.left + self.cell_size * i + 10,
                              self.top + self.cell_size * j)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        for i in range(self.height):
            for j in range(self.width):
                if ((x > j * self.cell_size + self.top) and (x <= (j + 1) * self.cell_size + self.top) and
                        (y > i * self.cell_size + self.left) and ((y <= (i + 1) * self.cell_size + self.left))):
                    r = i, j
                    return r

    def on_click(self, cell):
        y, x = cell[1], cell[0]
        if not(self.is_showing[y][x]):
            try:
                self.board[y][x] += self.board[y - 1][x]
            except:
                pass
            try:
                self.board[y][x] += self.board[y + 1][x]
            except:
                pass
            try:
                self.board[y][x] += self.board[y][x - 1]
            except:
                pass
            try:
                self.board[y][x] += self.board[y][x + 1]
            except:
                pass
            try:
                self.board[y][x] += self.board[y - 1][x + 1]
            except:
                pass
            try:
                self.board[y][x] += self.board[y + 1][x - 1]
            except:
                pass
            try:
                self.board[y][x] += self.board[y - 1][x - 1]
            except:
                pass
            try:
                self.board[y][x] += self.board[y + 1][x + 1]
            except:
                pass
            self.board[y][x] /= 10
            self.is_showing[y][x] = True

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, "green")
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


pygame.init()
sc = pygame.display.set_mode((320, 320))

board = Minesweeper(10, 10)
running = True

font_name = pygame.font.match_font('arial')
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    sc.fill((0, 0, 0))
    board.render(sc)
    pygame.display.flip()
