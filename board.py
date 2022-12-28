import random
from typing import Final

# *****************************************************************************
#  Execution:    none
#  Dependencies: nonez
#  Representation of a n-puzzle board object
#  @author Eduardo Ch. Colorado
# ******************************************************************************/


class Board(object):
    """
    Defines a Board for the n-puzzle game
    """

    # Constructor
    def __init__(self, blocks: list[list[int]]):
        """
        Creates an instance of a board
        Internally, the content of the board is represented as 1D array
        where each row in the 2D board is append to the right, from top
        to bottom
        Also the Manhattan and Hamming are calculated as private properties of the class
        """
        self.n: Final[int] = len(blocks)
        self.linear_board: list[int] = []
        self.Manhattan: int = 0
        self.Hamming: int = 0
        for i in range(self.n):
            for j in range(self.n):
                entry = blocks[i][j]
                self.linear_board.append(entry)
                if entry != 0:
                    self.Manhattan += abs(i - (entry - 1) // self.n) + abs(
                        j - ((entry - 1) % self.n)
                    )
                    if entry != self.n * i + j + 1:
                        self.Hamming += 1

    def dimension(self):
        """Size of the board game"""
        return self.n

    def manhattan(self):
        """Manhattan distance"""
        return self.Manhattan

    def hamming(self):
        """Hamming distance"""
        return self.Hamming

    def inversions(self):
        pass

    def is_goal(self) -> bool:
        """Determine when a given board is the goal board"""
        for i in range(0, self.n * self.n - 1):
            if self.linear_board[i] != i + 1:
                return False  # if the linear array is not sorted in ascending order, then the board is not the goal board
        return True

    def __get_board(self):
        return self.linear_board

    def __swap(self, Idx: int, nIdx: int):
        """Swap one valid place in the blank tile"""
        neighbor = [
            [self.linear_board[i * self.n + j] for j in range(self.n)]
            for i in range(self.n)
        ]
        i, j = Idx // self.n, Idx % self.n
        l, m = nIdx // self.n, nIdx % self.n
        temp = self.linear_board[nIdx]
        neighbor[i][j] = temp
        neighbor[l][m] = 0
        return neighbor

    ##Overload the comparison method
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
        # if(self == other): return True
        # if(other == None): return False
        # if(not isinstance(other, Board)): return False
        # other_board = other.__get_board()
        # for i in range(self.n*self.n):
        #     if(self.linear_board[i] != other_board[i]): return False
        # return True

    # Iterate through the possibles bottom, up, left and right blank tiles moves (we called them neighbors)
    def neighbors(self):
        """
        Return the possible boards after moving the blank tile to valid positions
        with respect to the reference Board
        """
        # search where the blank space is placed
        idx = self.linear_board.index(0)
        # create a neighbor list
        L: list[Board] = []
        if idx // self.n != 0:
            L.append(Board(self.__swap(idx, idx - self.n)))  # up neighbor
        if (idx + 1) // self.n == idx // self.n:
            L.append(Board(self.__swap(idx, idx + 1)))  # right neighbor
        if idx + self.n < self.n**2:
            L.append(Board(self.__swap(idx, idx + self.n)))  # botton neighopur
        if (idx - 1) // self.n == idx // self.n and idx - 1 >= 0:
            L.append(Board(self.__swap(idx, idx - 1)))  # left neighbor

        while len(L) != 0:
            yield L.pop()

    def __str__(self) -> str:
        s = "\n".join(
            "  ".join([str(self.linear_board[i * self.n + j]) for j in range(self.n)])
            for i in range(self.n)
        )
        return s + "\n"


# n = 3
# a = list(random.sample(range(n*n),n*n))

# blocks1 = [[a[n*i+j] for j in range(n)] for i in range(n) ]

# blocks2 = [[a[n*i+j] for j in range(n)] for i in range(n) ]
# temp = blocks2[1][2]
# blocks2[1][2] = blocks2[2][1]
# blocks2[2][1] = temp
# s = "\n".join(' '.join([str(blocks[i][j]) for j in range(3)]) for i in range(3))

# board1 = Board(blocks1)
# board2 = Board(blocks2)
# print(board1)
# print()
# print(board2)
# print()
# print(board1 == board2)
# print()
# print(board1.is_goal())
# print()
# print(board1.is_goal())
# print()
# for neighbor in board1.neighbors():
#     print(neighbor)
#     print('Manhattan distannce: ' + str(neighbor.manhattan()))
#     print('Hamming distance: ' + str(neighbor.hamming()))
#     print()
