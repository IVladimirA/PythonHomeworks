import pathlib
import random
from typing import List, Optional, Tuple

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool = True,
        max_generations: Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        for i in range(0, self.rows):
            row = []
            for j in range(0, self.cols):
                if randomize:
                    row.append(random.randint(0, 1))
                else:
                    row.append(0)
            grid.append(row)
        return grid

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
                if 0 <= new_x < self.cols and 0 <= new_y < self.rows:
                    cells.append(self.curr_generation[new_y][new_x])
        return cells

    def get_next_generation(self) -> Grid:
        grid = self.create_grid()
        for i in range(self.rows):
            for j in range(self.cols):
                cnt = sum(self.get_neighbours((i, j)))
                if self.curr_generation[i][j] == 0 and cnt == 3:
                    grid[i][j] = 1
                if self.curr_generation[i][j] == 1 and (cnt == 2 or cnt == 3):
                    grid[i][j] = 1
        return grid

    def step(self) -> None:
        self.prev_generation = self.curr_generation.copy()
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        return self.prev_generation != self.curr_generation

    def from_file(self, filename: pathlib.Path) -> "GameOfLife":
        file_r = open(filename, "r")
        self.cols, self.rows = map(int, file_r.readline().split())
        self.curr_generation = self.create_grid()
        self.prev_generation = self.create_grid()
        for i in range(0, self.rows):
            curr_row = file_r.readline()
            for j in range(0, self.cols):
                self.curr_generation[i][j] = int(curr_row[j])

    def save(self, filename: pathlib.Path) -> None:
        file_w = open(filename, "w")
        print(self.cols, self.rows, file=file_w)
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                print(self.curr_generation[i][j], end="", file=file_w)
            print("", file=file_w)


my_life = GameOfLife((30, 20), True)
# my_life.from_file(pathlib.Path("grid.txt"))
# my_life.save(pathlib.Path("grid.txt"))
