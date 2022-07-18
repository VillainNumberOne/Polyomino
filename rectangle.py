import numpy as np
from sparse_matrix import DLX, FakeSparseMatrix, SparseMatrix

class Rectangle():
    def __init__(self, W, H) -> None:
        self.W = W
        self.H = H

    def fit(self, figures: list, real_dlx=True) -> SparseMatrix:
        matrix = []
        row_header = []
        for idx, fig in enumerate(figures):
            for fig_configuration in fig:
                h, w = fig_configuration.shape
                for i in range(0, self.H - h + 1):
                    for j in range(0, self.W - w + 1):
                        indices = np.zeros(self.H * self.W)
                        for x in range(0, h):
                            for y in range(0, w):
                                indices[(i + x) * self.W + (j + y)] = 1 * fig_configuration[x, y]

                        row_header.append(idx)
                        matrix.append(indices)

        if real_dlx:
            return DLX(np.array(matrix), row_header)
        else:
            return FakeSparseMatrix(np.array(matrix), row_header)
