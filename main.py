import datetime
import os
from time import time

import numpy
import pygame

from cell import Cell, index
from constants import *
from dijkstra import dijkstra

pygame.init()
pygame.TIMER_RESOLUTION = 0

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Maze Generator [{ROWS}x{COLS}] | generating...")

FONT = pygame.font.SysFont("comicsans", 15)
clock = pygame.time.Clock()

grid: list[Cell] = []
stack: list[Cell] = []
current: Cell

dur: float
done: bool
total: int
remain: int


def remove_walls(a: Cell, b: Cell) -> None:
    """
    remove walls between two given cells
    """
    x = a.i - b.i
    y = a.j - b.j

    if x == 1:
        a.walls[3] = False
        b.walls[1] = False
    elif x == -1:
        a.walls[1] = False
        b.walls[3] = False

    if y == 1:
        a.walls[0] = False
        b.walls[2] = False
    elif y == -1:
        a.walls[2] = False
        b.walls[0] = False


def create_folder(directory: str) -> None:
    """
    creates export folder
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        pass


def export() -> None:
    """
    exports the generated maze if generation is finished\\
    found under ``export/maze.txt``
    """
    global done, FPS
    if done:
        maze = numpy.ones((ROWS*2 + 1, COLS*2 + 1), dtype=int)

        for j in range(ROWS):
            for i in range(COLS):
                cell = grid[index(i, j)]
                maze[2*j + 1, 2*i + 1] = 0

                maze[2 * j, 2*i + 1] = cell.walls[0]
                maze[2*j + 1, 2 * (i+1)] = cell.walls[1]
                maze[2 * (j+1), 2*i + 1] = cell.walls[2]
                maze[2*j + 1, 2 * i] = cell.walls[3]
        a = time()
        create_folder("./export/")
        with open(f"export\maze[{ROWS}x{COLS}].txt", "w", encoding="utf-8") as f:
            f.write("\n".join((" ".join(str(e) for e in x)) for x in maze))
        b = time()
        state = f"export succesfull in {round(b-a, 3)}s"
        pygame.draw.rect(window, BG, ((MIN + 1, 110), (MAX - MIN, 50)))
        state_label = FONT.render(state, True, (255, 255, 255))
        window.blit(state_label, (SEP, 110))
        pygame.display.flip()
        FPS = 10


def duration() -> str:
    """
    gets duration of generation
    """
    global dur
    tmp = time() - dur
    a = datetime.timedelta(seconds=tmp)
    return str(a)[:-4]


def display_path() -> None:
    """
    displays path
    """
    pygame.draw.rect(window, BG, ((MIN + 1, 120), (MAX - MIN, 50)))
    file = f"export\maze[{ROWS}x{COLS}].txt"
    s = "searching path, please wait ..."
    s_label = FONT.render(s, True, (255, 255, 255))
    window.blit(s_label, (SEP, 120))
    pygame.display.flip()
    a = time()
    path = dijkstra(file)
    b = time()
    pygame.draw.rect(window, BG, ((MIN + 1, 120), (MAX - MIN, 50)))
    s = f"path of lenght {(len(path)-1)//2}"
    s_label = FONT.render(s, True, (255, 255, 255))
    window.blit(s_label, (SEP, 120))
    s = f"found in {round(b-a, 3)}s"
    s_label = FONT.render(s, True, (255, 255, 255))
    window.blit(s_label, (SEP, 130))
    pygame.display.flip()
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        pygame.draw.line(window, HG, (y1 * W / 2, x1 * W / 2), (y2 * W / 2, x2 * W / 2))
        # pygame.display.flip()


def setup() -> None:
    """
    setup function
    """
    global current, done, total, remain

    done = False
    state = "wait for generation to complete"
    total = ROWS * COLS
    remain = total

    for j in range(ROWS):
        for i in range(COLS):
            cell = Cell(window, i, j)
            grid.append(cell)

    window.fill(BG)
    for cell in grid:
        cell.show()

    pygame.draw.rect(window, BG, ((MIN + 1, 80), (MAX - MIN, 50)))
    state_label = FONT.render(state, True, (255, 255, 255))
    window.blit(state_label, (SEP, 100))
    pygame.display.flip()

    current = grid[0]


def draw() -> None:
    """
    draw function
    """
    global current, done, total, remain

    for _ in range(1_000):  # fast gen
        if not current.visited:
            remain -= 1

        if not done:
            current.visited = True
            current.show()

        next = None
        if not done:
            next = current.check_neighbors(grid)

        if next is not None:
            stack.append(current)
            remove_walls(current, next)
            current = next
            current.highlight()

        elif len(stack) > 0:
            current = stack.pop()
            current.highlight()

        else:
            if not done:
                done = True
                current.highlight()
                state = f"done generating in {duration()}"
                pygame.draw.rect(window, BG, ((MIN + 1, 80), (MAX - MIN, 50)))
                state_label = FONT.render(state, True, (255, 255, 255))
                window.blit(state_label, (SEP, 100))
                pygame.display.flip()
                pygame.display.set_caption(f"Maze Generator [{ROWS}x{COLS}] | done")
                state = "processing... please wait"
                pygame.draw.rect(window, BG, ((MIN + 1, 110), (MAX - MIN, 50)))
                state_label = FONT.render(state, True, (255, 255, 255))
                window.blit(state_label, (SEP, 110))
                pygame.display.flip()
                export()
                display_path()

    pygame.draw.rect(window, BG, ((MIN + 1, 0), (MAX - MIN, 80)))
    fps_label = FONT.render(f"fps : {round(clock.get_fps())}", True, (255, 255, 255))
    window.blit(fps_label, (SEP, 10))
    remain_label = FONT.render(f"remaining : {remain}", True, (255, 255, 255))
    window.blit(remain_label, (SEP, 50))
    total_label = FONT.render(f"progress : {round(100*(total-remain)/total)}%", True, (255, 255, 255))
    window.blit(total_label, (SEP, 60))


if __name__ == "__main__":
    run = True
    setup()
    dur = time()
    while run:
        clock.tick(FPS)
        draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()
