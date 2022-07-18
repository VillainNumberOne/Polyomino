### Инструкция
```python
from solver import solve

task = [
    (3, 5), 
    [((2, 2), 1)], 
    [((3, 2), 1), ((2, 2), 2)],
]

result = solve(task)

```
Переменная task содержит лист, структура которого описана в формулировке задания.

### Комментарий и оценка сложности

Предложенная задача о существовании конфигурации опорных полиомино из заданного набора являющиейся замощением прямоугольного стола заданного размера сводится к задаче покрытия множества.
К важным особенностям данной задачи можно отнести то, при замощении стола могут оставаться свободные клетки в случае, когда суммарная площадь всех полиомино меньше площади стола. При этом каждой клетке стола может соответствовать клетка только одного полиомино и каждой каждой клетке каждого полиомино может соответствовать только одна клетка стола.
Так как задача о покрытии множества относится к классу NP-полных задач, алгоритмическая сложность решения будет экспоненциальной.

Для решения задачи был использован Алгоритм X, предложенный Д. Кнутом. Реализация находится в файле solver.py - функция alg_X(). 
Алгоритм был незначительно модифицирован для учета особенностей задачи. Оригинальный алгоритм включает этап выбора столбца с минимальным количеством ненулевых строк (соответствует клетке, покрываемой минимальным количеством полиомино); в случае, когда в выбранном столбце нет строк (т.е. данную клетку не покрывает ни одна фигура), ветвь не имеет решения. Так как по условию задачи могут существовать незаполненные клетки стола, на этом этапе выбирается минимальный ненулевой столбец.

Матрица задачи была реализована двумя способами: с помощью массива numpy (FakeSparseMatrix) и с помощью двумерного двусвязного списка Dancing Links (DLX). Оба АТД имеют одинаковые интерфейсы, таким образом, алгоритм решения задачи не зависит от конкретной реализации.
В большинстве случаев матрица задачи является разреженной, а так как для работы алгоритма необходимо быстро удалять и возвращать строки и столбцы, определять количество ненулевых элементов и наличие строк и столбцов в матрице, т.е. производить действия только с ненулевыми элементами, логичнее использовать DLX для хранения матрицы. В таком случае оценка сложности определения наличия/отстутствия строк или столбцов на определенной итерации будет O(1); операции с оценкой сложности O(n) в среднем будут занимать меньше времени, так как рассматриваются только ненулевые элементы. Однако, поскольку библиотека numpy хорошо оптимизирована, а использование Python для реализации связных списков не является оптимальным решением, фактическое время работы алгоритма с FakeSparseMatrix может быть меньше, чем с DLX для количества фигур c < некоторого c_max.
Ассимптотическая оценка используемой памяти при использовании обоих АТД будет O(c*n*m), где c - количество возможных конфигураций полиомино, n и m - размеры стола, так как на всех итерациях алгоритма хранится только один экземпляр АТД.

Задача относится к классу NP-полных и в любом случае имеет экспоненциальную сложность. Алгоритм X и Dancing Links

### Описание файлов

- main.ipynb: Блокнот с примерами
- solver.py: Содержит функции solve() и alg_X() реализующие Алгоритм X Д. Кнута.
- sparse_matrix.py: Содержит АТД FakeSparseMatrix и DLX для хранения матрицы задачи.
- polyomino.py: Содержит типы RectPolyomino и LPolyomino, необходимые для формирования матрицы задачи.
- rectangle.py: Содержит тип Rectangle, его метод fit() формирует матрицу задаыи.