import random
from Bubble import Bubble


class Level(object):
    def __init__(self, number, total=5):
        self.number = number
        self.total = total
        self.rows = 1 + number
        self.cols = Bubble.cols
        self.board = self.__gen_board(self.rows)
        self.intervals = {
            'level': 40000 + 20000 * number,
            'shot': 10000 - number * 1000,
            'descend': 30000 - - number * 2000
        }

    def __gen_board(self, rows):
        board = []
        for y in range(0, rows):
            row = []
            tmp = self.cols
            if y % 2 == 1:
                tmp = self.cols - 1
            for x in range(0, tmp):
                color = Bubble.colors[self.rand_gen()]
                row.append(color)
            board.append(row)
        return board

    def rand_gen(self):
        return random.randint(0, (len(Bubble.colors) - 1) * (self.total - self.number) * 10) % self.total

    def reinit(self, number):
        self.rows = 2 + number
        self.board = self.__gen_board(self.rows)
        self.intervals = {
            'shot': 10000 - number * 1000,
            'descend': 30000 - - number * 2000
        }

    def next(self):
        self.number += 1
        self.reinit(self.number)
