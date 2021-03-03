import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        for i in range(0, self.life.cols + 1):
            screen.addch(0, i, "-")
            screen.addch(self.life.rows + 1, i, "-")
        for i in range(0, self.life.rows + 1):
            screen.addch(i, 0, "|")
            screen.addch(i, self.life.cols + 1, "|")
        screen.addch(0, 0, "+")
        screen.addch(self.life.rows + 1, 0, "+")
        screen.addch(0, self.life.cols + 1, "+")
        screen.addch(self.life.rows + 1, self.life.cols + 1, "+")

    def draw_grid(self, screen) -> None:
        for i in range(0, self.life.rows):
            for j in range(0, self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    screen.addch(i + 1, j + 1, "*")
                else:
                    screen.addch(i + 1, j + 1, " ")

    def run(self) -> None:
        screen = curses.initscr()
        screen = curses.newwin(self.life.rows + 2, self.life.cols + 3, 0, 0)
        screen.move(0, 0)
        while not self.life.is_max_generations_exceeded:
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            self.life.step()
            time.sleep(0.5)
        curses.endwin()


# my_game = Console(GameOfLife((8, 8), True, 50))
# my_game.run()
