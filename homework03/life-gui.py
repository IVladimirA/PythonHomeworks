import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen_size = self.life.cols * cell_size, self.life.cols * cell_size
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        for x in range(0, self.screen_size[0], self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.screen_size[0]))
        for y in range(0, self.screen_size[1], self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.screen_size[1], y))

    def draw_grid(self) -> None:
        for i in range(0, self.life.rows):
            for j in range(0, self.life.cols):
                if self.life.curr_generation[i][j] == 1:
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

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток

        running = True
        pause = False
        while running:
            if not pause:
                self.draw_grid()
                self.draw_lines()
                self.life.step()
                pygame.display.flip()
                clock.tick(self.speed)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == K_p:
                    pause = not pause
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    x, y = pos
                    row = y // self.cell_size
                    col = x // self.cell_size
                    self.life.curr_generation[row][col] = 1 - self.life.curr_generation[row][col]
                    if self.life.curr_generation[row][col] == 1:
                        pygame.draw.rect(
                            self.screen,
                            pygame.Color("green"),
                            (
                                col * self.cell_size,
                                row * self.cell_size,
                                self.cell_size,
                                self.cell_size,
                            ),
                        )
                    else:
                        pygame.draw.rect(
                            self.screen,
                            pygame.Color("white"),
                            (
                                col * self.cell_size,
                                row * self.cell_size,
                                self.cell_size,
                                self.cell_size,
                            ),
                        )
                    self.draw_lines()
                    pygame.display.flip()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE

        pygame.quit()


if __name__ == "__main__":
    game = GUI(GameOfLife((30, 20), True), 20)
    game.run()
