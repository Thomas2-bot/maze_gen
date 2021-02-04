from queue import PriorityQueue

import numpy

from constants import *


class Node:
    """
    data struct for dikkstra
    """
    def __init__(self, i: int, j: int) -> None:
        """
        Node at ``i``, ``j``

        Parameters
        ----------
            i : int
                i index
            j : int
                j index
        """
        self.i = i
        self.j = j

        self.w = 0
        self.parent: Node = None

    def __hash__(self) -> int:
        """
        unique id
        """
        return self.i + self.j * COLS

    def __eq__(self, o: object) -> bool:
        """
        overload of ``==``
        """
        return self.i == o.i and self.j == o.j

    def __ne__(self, o: object) -> bool:
        """
        overload of ``!=``
        """
        return self.i != o.i or self.j != o.j

    def __lt__(self, o: object) -> bool:
        """
        overload of ``<``
        """
        return self.w < o.w

    def __le__(self, o: object) -> bool:
        """
        overload of ``<=``
        """
        return self.w <= o.w

    def __gt__(self, o: object) -> bool:
        """
        overload of ``>``
        """
        return self.w > o.w

    def __ge__(self, o: object) -> bool:
        """
        overload of ``>=``
        """
        return self.w >= o.w


def get_children(node: Node, arr: numpy.ndarray) -> set[Node]:
    """
    gets all children
    """
    s: set[Node] = set()
    dir = ((0, -1), (1, 0), (0, 1), (-1, 0))
    for index in dir:
        a = node.i + index[0]
        b = node.j + index[1]
        val = arr[a, b]
        if val == 0:
            child = Node(a, b)
            child.parent = node
            s.add(child)
    return s


def get_path(node: Node) -> list[tuple[int, int]]:
    """
    recursivly getting path
    """
    path = [node]
    current = node
    while current.parent is not None:
        current = current.parent
        path.append(current)
    return [(node.i, node.j) for node in path][::-1]


def dijkstra(file: str) -> list[tuple[int, int]]:
    """
    modified dijkstra when unique path
    """
    with open(file, "r", encoding="utf-8") as f:
        l = f.readlines()
    arr = []
    for e in l:
        k = e.split(" ")
        for j in k:
            try:
                arr.append(int(j))
            except:
                pass
    arr = numpy.reshape(numpy.array(arr, dtype=int), (2*ROWS + 1, 2*COLS + 1))

    open_queue: PriorityQueue[Node] = PriorityQueue()
    closed_set: set[Node] = set()

    start = Node(1, 1)
    end = Node(2*ROWS - 1, 2*COLS - 1)
    current = start

    open_queue.put(current)

    while not open_queue.empty():
        current = open_queue.get()
        closed_set.add(current)

        if current == end:
            return get_path(current)

        for child in get_children(current, arr):
            if child in closed_set:
                continue
            child.w = current.w + 1
            open_queue.put(child)
