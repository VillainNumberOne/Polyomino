import numpy as np

class SparseMatrix():
    def __init__(self, matrix: np.ndarray, row_header: list):
        self.M = matrix
        if len(self.M.shape) == 1:
            self.M = np.expand_dims(self.M, 0)

        assert len(self.M.shape) == 2
        self.H, self.W = self.M.shape

        self.row_header = row_header
        self.row_header_dict = {}
        for idx, el in enumerate(self.row_header):
            if el in self.row_header_dict.keys():
                self.row_header_dict[el].append(idx)
            else:
                self.row_header_dict[el] = [idx]
        self.n_figures = len(self.row_header_dict)

    def has_cols(self) -> bool:
        pass

    def has_rows(self) -> bool:
        pass

    def del_row(self, node):
        pass

    def restore_row(self, node):
        pass

    def del_col(self, node):
        pass

    def restore_col(self, node):
        pass

    def min_col(self):
        pass

    def non_zero_rows(self, node) -> list:
        pass

    def non_zero_cols(self, node) -> list:
        pass

    def delete_configurations(self, node):
        pass

class DLXNode():
    def __init__(self, i, j, right=None, left=None, up=None, down=None) -> None:
        self.i, self.j = i, j
        self.right, self.left, self.up, self.down = right, left, up, down
        self.deleted = False

class DLX(SparseMatrix):
    def __init__(self, matrix: np.ndarray, row_header: list):
        super().__init__(matrix, row_header)

        self.col_heads = [DLXNode(-1, j) for j in range(self.W)]
        self.row_heads = [DLXNode(i, -1) for i in range(self.H)]

        self.node_matrix = [
            [DLXNode(i, j) if self.M[i, j] == 1 else None for j in range(self.W)]
            for i in range(self.H)
        ]

        # linking columns
        for i in range(self.H):
            current = self.row_heads[i]
            for j in range(self.W):
                candidate = self.node_matrix[i][j]
                if self.node_matrix[i][j] is not None:
                    current.right = candidate
                    candidate.left = current
                    current = candidate

        # linking rows
        for j in range(self.W):
            current = self.col_heads[j]
            for i in range(self.H):
                candidate = self.node_matrix[i][j]
                if self.node_matrix[i][j] is not None:
                    current.down = candidate
                    candidate.up = current
                    current = candidate

        # linking heads
        self.root = DLXNode(-1, -1)
        current = self.root
        for i in range(self.H):
            candidate = self.row_heads[i]
            current.down = candidate
            candidate.up = current
            current = candidate

        current = self.root
        for j in range(self.W):
            candidate = self.col_heads[j]
            current.right = candidate
            candidate.left = current
            current = candidate


    def has_cols(self) -> bool:
        if self.root.right is not None:
            return True
        else:
            return False

    def has_rows(self) -> bool:
        if self.root.down is not None:
            return True
        else:
            return False

    def del_row(self, node):
        current = self.row_heads[node.i]
        while current is not None:
            if not current.deleted:
                if current.up is not None:
                    current.up.down = current.down
                if current.down is not None:
                    current.down.up = current.up
                current.deleted = True
            
            current = current.right

    def restore_row(self, node):
        if node.left is not None:
            node.left.right = node
        if node.right is not None:
            node.right.left = node

        current = self.row_heads[node.i]
        while current is not None:
            if current.up is not None:
                current.up.down = current
            if current.down is not None:
                current.down.up = current
            current.deleted = False
            current = current.right

    def del_col(self, node):
        current = self.col_heads[node.j]
        while current is not None:
            if not current.deleted:
                if current.left is not None:
                    current.left.right = current.right
                if current.right is not None:
                    current.right.left = current.left
                current.deleted = True
            current = current.down

    def restore_col(self, node):
        if node.up is not None:
            node.up.down = node
        if node.down is not None:
            node.down.up = node

        current = self.col_heads[node.j]
        while current is not None:
            if current.left is not None:
                current.left.right = current
            if current.right is not None:
                current.right.left = current
            current.deleted = False
            current = current.down

    def min_col(self):
        current_col = self.root.right
        min_value = np.inf
        min_col = None

        while current_col is not None:
            col_sum = 0
            current_node = current_col.down

            while current_node is not None:
                col_sum += 1
                current_node = current_node.down

            if col_sum < min_value and col_sum > 0:
                if col_sum == 1:
                    return current_col
                min_value = col_sum
                min_col = current_col

            current_col = current_col.right

        return min_col

    def non_zero_rows(self, node) -> list:
        head = self.col_heads[node.j]
        current = head.down
        result = []
        while current is not None:
            result.append(current)
            current = current.down
        return result

    def non_zero_cols(self, node) -> list:
        head = self.row_heads[node.i]
        current = head.right
        result = []
        while current is not None:
            result.append(current)
            current = current.right
        return result

    def delete_configurations(self, node):
        configurations_idxs = self.row_header_dict[self.row_header[node.i]]
        configurations = []

        for idx in configurations_idxs:
            if not self.row_heads[idx].deleted:
                self.del_row(self.row_heads[idx])
                configurations.append(self.row_heads[idx])

        return configurations


class FSPNode():
    def __init__(self, i, j) -> None:
        self.i, self.j = i, j


class FakeSparseMatrix(SparseMatrix):
    def __init__(self, matrix: np.ndarray, row_header: list):
        super().__init__(matrix, row_header)
        self.Mt = self.M.T
        self.row_flags = np.ones(self.H).astype(bool)
        self.col_flags = np.ones(self.W).astype(bool)

    def has_cols(self) -> bool:
        return any(self.col_flags)
    
    def has_rows(self) -> bool:
        return any(self.row_flags)

    def del_row(self, node):
        self.row_flags[node.i] = False

    def restore_row(self, node):
        self.row_flags[node.i] = True

    def del_col(self, node):
        self.col_flags[node.j] = False

    def restore_col(self, node):
        self.col_flags[node.j] = True

    def min_col(self) -> FSPNode:
        temp = np.copy(self.M)
        temp[np.logical_not(np.outer(self.row_flags, self.col_flags))] = np.NaN
        s = np.nansum(temp, 0)
        s[self.col_flags == False] = np.inf
        return FSPNode(0, np.where(s==np.min(s[np.nonzero(s)]))[0][0])

    def non_zero_rows(self, node) -> list:
        if not self.col_flags[node.j]:
            return []
        return [FSPNode(i, node.j) for i in np.nonzero(self.Mt[node.j])[0] if self.row_flags[i]]

    def non_zero_cols(self, node) -> list:
        if not self.row_flags[node.i]:
            return []
        return [FSPNode(node.i, j) for j in np.nonzero(self.M[node.i])[0] if self.col_flags[j]]

    def delete_configurations(self, node):
        configurations = [FSPNode(i, 0) for i in self.row_header_dict[self.row_header[node.i]] if self.row_flags[i]]
        for el in configurations:
            self.del_row(el)
        return configurations
