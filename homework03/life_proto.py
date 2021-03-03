import random
from typing import List, Tuple

import pygame
from pygame.locals import *

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed
        self.grid = None

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE
            self.draw_grid()
            self.draw_lines()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        for i in range(0, self.cell_height):
            row = []
            for j in range(0, self.cell_width):
                if randomize:
                    row.append(random.randint(0, 1))
                else:
                    row.append(0)
            grid.append(row)
        return grid

    def draw_grid(self) -> None:
        for i in range(0, self.cell_height):
            for j in range(0, self.cell_width):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (
                            j * self.cell_size,
                            i * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (
                            j * self.cell_size,
                            i * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )
        pass

    def get_neighbours(self, cell: Cell) -> Cells:
        y, x = cell
        cells = []
        move = [-1, 0, 1]
        for i in range(0, 3):
            for j in range(0, 3):
                new_y = y + move[i]
                new_x = x + move[j]
                if x == new_x and y == new_y:
                    continue
                if 0 <= new_x < self.cell_width and 0 <= new_y < self.cell_height:
                    cells.append(self.grid[new_y][new_x])
        return cells

    def get_next_generation(self) -> Grid:
        grid = self.create_grid()
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                cnt = sum(self.get_neighbours((i, j)))
                if self.grid[i][j] == 0 and cnt == 3:
                    grid[i][j] = 1
                if self.grid[i][j] == 1 and (cnt == 2 or cnt == 3):
                    grid[i][j] = 1
        return grid


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
