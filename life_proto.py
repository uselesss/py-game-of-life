import random
import typing as tp
from copy import deepcopy

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]

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
        
        # Стоит ли игра на паузе
        self.pause = False

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                if event.type == MOUSEBUTTONDOWN and self.pause:
                    grid_x = list(event.pos)[0]//self.cell_size
                    grid_y = list(event.pos)[1]//self.cell_size
                    self.grid[grid_y][grid_x] = not self.grid[grid_y][grid_x]
                    
                    self.draw_lines()
                    self.draw_grid()
                    pygame.display.flip()
            
            if not self.pause:
                self.draw_lines()

                # Отрисовка списка клеток
                # Выполнение одного шага игры (обновление состояния ячеек)
                self.grid = self.get_next_generation()
                self.draw_grid()
                pygame.display.flip()
                clock.tick(self.speed)
    
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        return [[random.randint(0,1) if randomize else 0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                rect = pygame.Rect(j*self.cell_size+1, i*self.cell_size+1, self.cell_size-1, self.cell_size-1)
                if self.grid[i][j]:
                    pygame.draw.rect(self.screen, pygame.Color("Green"), rect)
                else:
                    pygame.draw.rect(self.screen, pygame.Color("White"), rect)

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        x = cell[0]
        y = cell[1]
        Cells = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (0 <= x+j < self.cell_width) and (0 <= y+i < self.cell_height) and (i!=0 or j!=0):
                    Currcell = self.grid[y+i][x+j]
                    Cells.append(Currcell)
        return Cells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        newGrid = deepcopy(self.grid)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                n = self.get_neighbours([j,i])
                if (self.grid[i][j] == 0) and sum(n) == 3:
                    newGrid[i][j] = 1
                if (self.grid[i][j] == 1) and (sum(n) < 2 or sum(n) > 3):
                    newGrid[i][j] = 0
        
        return newGrid
    
if __name__ == '__main__':
    game = GameOfLife(1000, 800, 20, 5)
    game.run()
