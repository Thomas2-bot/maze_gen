import random

import pygame

from constants import *


def index(i: int, j: int) -> int:
    """
    index on flat list
    """
    if i < 0 or j < 0 or i > COLS - 1 or j > ROWS - 1:
        return None
    return i + j*COLS


class Cell:
    def __init__(self, window, i: int, j: int) -> None:
        self.window = window
        self.i = i
        self.j = j

        self.walls = [True, True, True, True]
        self.visited = False

    def check_neighbors(self, grid: list):
        neighbors = []

        try:
            top = grid[index(self.i, self.j - 1)]
        except TypeError:
            top = None
        try:
            right = grid[index(self.i + 1, self.j)]
        except TypeError:
            right = None
        try:
            bottom = grid[index(self.i, self.j + 1)]
        except TypeError:
            bottom = None
        try:
            left = grid[index(self.i - 1, self.j)]
        except TypeError:
            left = None

        if top is not None and not top.visited:
            neighbors.append(top)
        if right is not None and not right.visited:
            neighbors.append(right)
        if bottom is not None and not bottom.visited:
            neighbors.append(bottom)
        if left is not None and not left.visited:
            neighbors.append(left)

        if (i := len(neighbors)) > 0:
            r = random.randint(0, i - 1)
            return neighbors[r]

    def highlight(self) -> None:
        x = self.i * W
        y = self.j * W

        pygame.draw.rect(self.window, HG, ((x, y), (W, W)))

    def show(self) -> None:
        x = self.i * W
        y = self.j * W

        if self.visited:
            pygame.draw.rect(self.window, FG, ((x, y), (W + 1, W + 1)))

        if self.walls[0]:
            pygame.draw.line(self.window, (155, 155, 155), (x, y), (x + W, y))
        if self.walls[1]:
            pygame.draw.line(self.window, (155, 155, 155), (x + W, y), (x + W, y + W))
        if self.walls[2]:
            pygame.draw.line(self.window, (155, 155, 155), (x + W, y + W), (x, y + W))
        if self.walls[3]:
            pygame.draw.line(self.window, (155, 155, 155), (x, y + W), (x, y))
