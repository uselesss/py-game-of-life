import pathlib
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
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
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
        # Copy from previous assignment
        return [[random.randint(0,1) if randomize else 0 for _ in range(self.rows)] for _ in range(self.cols)]

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        x = cell[0]
        y = cell[1]
        cells = []
        for i in range(-1, 2):
            for j in range(-1, 2):  
                if (0 <= x+j < self.rows) and (0 <= y+i < self.cols) and (i!=0 or j!=0):
                    currcell = self.curr_generation[y+i][x+j]
                    cells.append(currcell)
        return cells

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        newGrid = deepcopy(self.curr_generation)
        for i in range(self.cols):
            for j in range(self.rows):
                n = self.get_neighbours([j,i])
                if (self.curr_generation[i][j] == 0) and sum(n) == 3:
                    newGrid[i][j] = 1
                if (self.curr_generation[i][j] == 1) and (sum(n) < 2 or sum(n) > 3):
                    newGrid[i][j] = 0
        return newGrid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.step < self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation == self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []
        with open(filename, 'r') as file:
            for line in file:
                grid.append(list(map(int, list(line[:-1]))))
        grid = grid[:-1]
        game = GameOfLife((len(grid), len(grid[0])))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, 'w') as file:
            for line in self.curr_generation:
                file.write(''.join(list(map(str, line)))+'\n')
        
   