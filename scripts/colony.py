from random import random
from collections import deque
from datetime import datetime
from utils import Square, Vector


class Colony:
    def __init__(self, radius: Vector, max_population_count: int, reproduce_chance: float):
        self.radius = radius
        self.starting_point = Vector(self.radius.x // 2, self.radius.y // 2)

        self.max_population_count = max_population_count
        self.reproduce_chance = reproduce_chance

        self.population_count = 1
        self.current_generation = 1

        self.colony = [[None for y in range(self.radius.y + 1)] for x in range(self.radius.x + 1)]
        self.not_reproduced_squares = deque()


    def _able_to_reproduce(self) -> bool:
        return random() < self.reproduce_chance


    def _output_debug_info(self) -> None:
        print(self.current_generation, end='\t')
        print(f'[{datetime.now().isoformat()}]', end='\t')
        print('{:.5f}'.format(self.population_count / self.max_population_count * 100), '%', end='\t')
        print(f'({self.population_count} / {self.max_population_count})')


    def _square_reproduce(self, square: Square, generation: int) -> list:
        self.population_count += 1

        x = square.x
        y = square.y

        right = Vector(x + 1, y)
        up = Vector(x, y + 1)
        left = Vector(x - 1, y)
        bottom = Vector(x, y - 1)

        neighboring_coordinates = [right, up, left, bottom]
        neighboring_squares = []

        # 'nc' stands for 'neighboring coordinate'
        for nc in neighboring_coordinates:
            if (
                nc.x <= self.radius.x
                and nc.x >= 0
                and nc.y <= self.radius.y
                and nc.y >= 0
                and self._able_to_reproduce()
            ):
                if not self.colony[nc.x][nc.y]:
                    self.colony[nc.x][nc.y] = Square(nc.x, nc.y, generation)
                    neighboring_squares.append(self.colony[nc.x][nc.y])

        return neighboring_squares


    def _get_next_generation(self, current_generation_squares: list) -> list:
        self.current_generation += 1

        next_generation_squares = []
        for square in current_generation_squares:
            next_generation_squares.extend(self._square_reproduce(square, self.current_generation))
        return next_generation_squares


    def _destroy(self) -> None:
        self.colony = [[None for y in range(self.radius.y + 1)] for x in range(self.radius.x + 1)]
        self.population_count = 1
        self.current_generation = 1
        self.not_reproduced_squares = deque()

        starting_square = Square(self.starting_point.x, self.starting_point.y, self.current_generation)
        self.colony[starting_square.x][starting_square.y] = starting_square
        self.not_reproduced_squares.append([starting_square])


    def develop(self, find_percent: float=0) -> None:
        starting_square = Square(self.starting_point.x, self.starting_point.y, self.current_generation)
        self.colony[starting_square.x][starting_square.y] = starting_square
        self.not_reproduced_squares.append([starting_square])

        if find_percent:
            while True:
                while self.not_reproduced_squares != deque([[]]) and self.population_count <= self.max_population_count:
                    self._output_debug_info()
                    current_generation_squares = self.not_reproduced_squares.popleft()
                    self.not_reproduced_squares.append(self._get_next_generation(current_generation_squares))

                    if self.population_count / self.max_population_count >= find_percent:
                        break

                if self.population_count / self.max_population_count >= find_percent:
                    break
                else:
                    self._destroy()
        else:
            while self.not_reproduced_squares != deque([[]]) and self.population_count <= self.max_population_count:
                self._output_debug_info()
                current_generation_squares = self.not_reproduced_squares.popleft()
                self.not_reproduced_squares.append(self._get_next_generation(current_generation_squares))