from sparse_matrix import DLX as Sparse
from rectangle import Rectangle
from polyomino import *

def check_total_area(task: list) -> bool:
    rectangle_area = task[0][0] * task[0][1]
    figures_total_area = sum([w * h * n for (w, h), n in task[1]])
    figures_total_area += sum([(w + h - 1) * n for (w, h), n in task[2]])
    return rectangle_area >= figures_total_area


def solve(task: list, real_dlx=True):
    table_size, rects, ls = task

    if not check_total_area(task):
        return False

    figures = []
    for size, n in rects:
        figures.extend([RectPolyomino(*size).get_rotations() for _ in range(n)])
    for size, n in ls:
        figures.extend([LPolyomino(*size).get_rotations() for _ in range(n)])

    SM = Rectangle(*table_size).fit(figures, real_dlx)
    if alg_X(SM, solution=[]):
        return True
    else:
        return False


def alg_X(matrix: Sparse, solution = [], call_counter = 0):
    # special cases
    if not matrix.has_rows():
        if len(solution) == matrix.n_figures:
            return solution
        else:
            return []
    if matrix.has_rows() and not matrix.has_cols():
        return []
    
    # select min non-zero column
    min_col = matrix.min_col()
    non_zero_rows = matrix.non_zero_rows(min_col)

    # check non-zero rows
    for current_node in non_zero_rows:
        deleted_rows = []
        deleted_cols = []
        # add to the solution
        solution.append(current_node)

        # delete rows and columns
        cols_to_remove = matrix.non_zero_cols(current_node)
        deleted_cols.extend(cols_to_remove)
        for col in cols_to_remove:
            rows_to_remove = matrix.non_zero_rows(col)
            deleted_rows.extend(rows_to_remove)
            for row in rows_to_remove:
                matrix.del_row(row)
            matrix.del_col(col)

        # delete configurations
        deleted_rows.extend(matrix.delete_configurations(current_node))

        # new recursion call
        result = alg_X(matrix, solution, call_counter)
        if result:
            return result

        # restore everything
        solution.pop()

        for col in deleted_cols[::-1]:
            matrix.restore_col(col)
        for row in deleted_rows[::-1]:
            matrix.restore_row(row)

    return []
