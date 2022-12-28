import minPQ
from board import Board  # from the file import the class name
import random
from heapq import heappop, heappush
from pathlib import Path
from enum import Enum, auto

# *****************************************************************************
#  Execution:    python solver.py
#  Dependencies: none
#
#  Game tree solver. The initial board is used as the root of a game tree. The child
#  nodes represents possible configurations of the initial board.
#  Using a min priority queue and the A* algorithm, this code finds the solution of
#  the n-puzzle game with the minimum number of moves and prints the steps you
#  need to follow to reach the solution in the real life.
#
#  You can build your own board of size n x n using the following example:
#
#  3
#  9  7  3
#  4  5  6
#  1  2  0
#
#  The 0 represents the black tile in the n-puzzle game
#
#  @author Eduardo Ch. Colorado
# ******************************************************************************/


# #############################################################################/
# How the algorithm works?
# To solve any given game board, a game tree is build with the initial
# board as the root of the tree

# Briefly, the solution is based on:

# A* algorithm -> to minimize f (cost function) where f = g + h
# g = number of moves (goal distance)
# h = manhattan or hamming distance (heuristic distance)

# In this code I used the word "neighbors" to named the different possible configurations
# for a board when you swap the blank tile one place to the left, right, up or bottom.
# For example:

# Initial board                                       "neighbors"
#    9  7  4                  9  0  4          9  7  4          9  7  4         9  7  4
#    1  0  3         ->       1  7  3          0  1  3          1  3  0         1  6  3
#    2  6  5                  2  6  5          2  6  5          2  6  5         2  0  5


# For further illustration, we called n1, n2 and n3 to the "neighbors" of the initial board
# and we assume n2 has the lowest h value in the following diagram:
#
#                                number of
#                                iterations          Game Tree
# _______________________________________________________________
#     MinPQ                          0             initial board
#     -----                                              |
#     -----                                          /   |    \
#   n1-----                                         /    |     \
#   n3-----   node with              1             n1    n2    n3         three different
#   n2----- <- lowest                                    ^                configurations
#              f cost                                    |
#                                    2          n1, n2, and n3 are added
#                                    .          into the minPQ but n2 will
# The MinPQ always has the           .          be pop in the next step,
# board with lower f cost            .          then its neighbors will be
# ready to be dequeued on            .          added again into the minPQ
# each iteration. Other              .          and ordered by its f cost
# added boards with slightly                    taking into account n1 and n3.
# higher f cost are "waiting"                   This process is repeated until
# its turn to be dequeued            .          the goal is reached (if it exist)
#                                    .
#
#
# the number of iterations increases on each level of the game tree. The number of
# moves is recorded internally in the node object in this implementation
##############################################################################/z


class BoardNode(object):
    """
    Recursive data structure, a wrapper for the class board to make a linked list
    current: (Board) the current board instance in the solver
    state:   (int) the current state (move) in the solver
    link:    (BoardNode) a link to the precedent BoardNode object
    """

    def __init__(self, current: Board, state: int, link: Board):
        self.current = current
        self.state = state
        self.link = link


class HeuristicDistance(Enum):
    """
    Available heuristic distances to solve the 8-puzzle game
    """

    MANHATTAN = auto()
    HAMMING = auto()


class Solver(object):
    """
    A class created to solve the 8-puzzle using a min priority queue and the
    A* algorithm. It take a two dimensional array as a representation of a
    valid game board an search the minimum number of moves to solve the puzzle
    optimizing the following cost function:

    f = g + h

    where g are the number of moves and h is either the Manhattan or
    Hamming distances
    """

    def __init__(self, boardGame: Board, heuristic: HeuristicDistance):
        self.board = boardGame
        self.heuristic = heuristic
        self.moves = 0  # counter to count the moves required to reach the solution
        self.solutions: list[Board] = []
        self.__solve()  # remember the _ and __ expresses my intent of declare this
        # variables as private

    def __solve(self):
        state = 0
        board_node = BoardNode(
            self.board, state, None
        )  # Create a node board (basically it's a linked list)
        seeker_node = self.aStar(
            board_node, self.heuristic
        )  # I wrapped immediately the initial board node
        # with the aStar class and its methods to perform calculations

        # Uncomment if you want to use my code for the min probity queue intend of the one
        # provided by the heapq library
        # pq = minPQ.MinPQ()             # you can use this minPQ instead and compare which is faster
        # pq.insert(seeker_node)

        # Uncomment the two lines below to implement min heap queue provided by the heapq library

        pq = []  # the heapq library requires an empty list to build the heap
        heappush(
            pq, seeker_node
        )  # and push the first element into this empty list using heappush
        i = 0
        while True:  # the seeker node is a search node with the A* methods
            # seeker_node = pq.delMin()   # uncomment if you are using the minPQ.py file
            # get the board node processed by the A* algorithm
            seeker_node = heappop(pq)  # uncomment if you are using the heapq library
            board_node = (
                seeker_node.get_Board_Node()
            )  # get the board node with the lowest scoring function value
            old_board_node = board_node  # We keep the previous move because inside this node there are
            state = (
                old_board_node.state + 1
            )  # an internal counter that help us to keep track the number
            # of moves for a particular node
            if board_node.link == None:
                predecessor = None  # if there isn't any link to another node, this node doesn't have a predecessor
            else:
                predecessor = (
                    board_node.link.current
                )  # else we set the current node as the predecessor for the next
            # Uncomment for debbuging
            # print("Step: " + str(i))
            # print("Priority " + str(seeker_node.get_priority()))
            # print("moves: " + str(board_node.state))
            # print("manhattan " + str(board_node.current.manhattan()))
            # print("search node: ")
            # print(board_node.current)
            # print('----------')
            # print("neighbors")

            # Game tree loop. We iterate through the neighbors
            for neighbor in board_node.current.neighbors():
                if not (
                    neighbor == predecessor
                ):  # to avoid repetitions the current neighbor must be different to the previous configuration
                    # print(neighbor)
                    board_node = BoardNode(neighbor, state, old_board_node)
                    branch = self.aStar(board_node, self.heuristic)
                    # pq.insert(branch)
                    heappush(pq, branch)
            i += 1
            if old_board_node.current.is_goal():
                break
        # uncomment to know how many iteretions were required to find the solution
        # print("iterations " + str(i))

        # Once we found the goal board we used its link to retrieve all the previous
        # steps and we store them in a list
        self.moves = state  # update the number of moves
        board_node = board_node.link
        while board_node != None:
            self.solutions.append(board_node.current)
            board_node = board_node.link

    # not all puzzles have solution, this method tell us before hand if a board is solvable
    def isSolvable(self):
        """To be implemented"""
        pass

    def __iter__(self):
        """
        Define a way to iterate on the solver
        """
        while len(self.solutions) > 0:
            yield self.solutions.pop()

    def number_of_moves(self):
        return self.moves - 1

    # @functools.total_ordering
    class aStar(object):
        """
        An extra layer for the board class. Here we are going to implement the
        aStar algorithm to solve the 8-puzzle. The priority queue will mantain
        the priorities based on this computations
        """

        def __init__(self, BoardNode: BoardNode, heuristic: HeuristicDistance):
            self.BoardNode = BoardNode
            self.heuristic_distance = self.getHeuristicDistance(
                heuristic
            )  # can be replace with the hamming distance
            self.state = self.BoardNode.state
            self.cost_function = self.heuristic_distance + self.BoardNode.state

        def getHeuristicDistance(self, heuristic: HeuristicDistance):
            match heuristic:
                case heuristic.MANHATTAN:
                    return self.BoardNode.current.manhattan()
                case heuristic.HAMMING:
                    return self.BoardNode.current.hamming()

        def get_Board_Node(self):
            return self.BoardNode

        def get_priority(self):
            return self.cost_function

        def __lt__(self, other):
            return (self.cost_function, self.heuristic_distance) < (
                other.cost_function,
                other.heuristic_distance,
            )

        def __eq__(self, other):
            return self.cost_function == other.cost_function


if __name__ == "__main__":
    # Uncomment to create the game board game from a random generator
    # n = 3   # size of the board
    # a = list(random.sample(range(n*n),n*n))
    # blocks = [[a[n*i+j] for j in range(n)] for i in range(n) ]

    # Uncomment to create the board game reading from a file
    data_folder = Path("source_data/")
    file_to_open = data_folder / "puzzle04.txt"
    f = open(file_to_open)
    z = int(f.readline())
    blocks = [[int(el) for el in line.split()] for line in f]

    board = Board(blocks)
    # print("initial board")
    # print(board)
    # print("------")
    solver = Solver(board, HeuristicDistance.MANHATTAN)

    # Check if the board is solvable and if so, show how to solve it
    print("# of move to solve the board: " + str(solver.number_of_moves()))
    for solutions in solver:
        print(solutions)
