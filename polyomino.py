import numpy as np

class Polyomino():
    def __init__(self) -> None:
        pass

    def get_rotations(self) -> list:
        pass

class RectPolyomino(Polyomino):
    def __init__(self, S1, S2) -> None:
        super().__init__()
        self.figure = np.ones((S1, S2))
        if S1 == S2:
            self.square = True
        else:
            self.square = False

    def get_rotations(self):
        if self.square:
            return [self.figure]
        else:
            return [np.rot90(self.figure, k) for k in range(0, 2)]

class LPolyomino(Polyomino):
    def __init__(self, Q1, Q2) -> None:
        super().__init__()
        self.figure = np.zeros((Q1, Q2))
        self.figure[-1] = 1
        self.figure[:, 0] = 1

    def get_rotations(self) -> list:
        return [np.rot90(self.figure, k) for k in range(0, 4)]
