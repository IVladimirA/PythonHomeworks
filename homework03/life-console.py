import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife, sleeptime: int = 1000) -> None:
        super().__init__(life)
        self.sleeptime = sleeptime

    def draw_borders(self, window) -> None:
        for i in range(0, self.life.cols + 1):
            window.addch(0, i, "-")
            window.addch(self.life.rows + 1, i, "-")
        for i in range(0, self.life.rows + 1):
            window.addch(i, 0, "|")
            window.addch(i, self.life.cols + 1, "|")
        window.addch(0, 0, "+")
        window.addch(self.life.rows + 1, 0, "+")
        window.addch(0, self.life.cols + 1, "+")
        window.addch(self.life.rows + 1, self.life.cols + 1, "+")

    def draw_grid(self, window) -> None:
        for i in range(0, self.life.rows):
            for j in range(0, self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    window.addch(i + 1, j + 1, "*")
                else:
                    window.addch(i + 1, j + 1, " ")

    def run(self) -> None:
        curses.initscr()
        curses.noecho()
        curses.cbreak()
        window = curses.newwin(self.life.rows + 2, self.life.cols + 3, 0, 0)
        window.nodelay(True)
        pause = False
        while True:
            key = window.getch()
            if key == ord("q") or key == ord("Q"):
                break
            if key == ord("p") or key == ord("P"):
                pause = not pause
            if not pause:
                self.draw_borders(window)
                self.draw_grid(window)
                window.refresh()
                self.life.step()
                curses.napms(self.sleeptime)
        curses.endwin()


# my_game = Console(GameOfLife((8, 8), True, 10), 1000)
# my_game.run()
