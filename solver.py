import minPQ
from board import Board # from the file import the class name
import random
from heapq import heappop, heappush
from pathlib import Path

#*****************************************************************************
#  Execution:    python solver.py 
#  Dependencies: none
#
#  Game tree solver. The initial board is used as the root of a game tree. The child
#  nodes represents possible configurations of the initial board.
#  Using a min priority queue and the A* algorithm, this code finds the solution of
#  the the n-puzzle game with the minimum number of moves and prints the steps you 
#  need to follow to reach the soltion in the real life.
#
#  You can build your own board of size n x n using the following example:
#  
#  3
#  9  7  3
#  4  5  6
#  1  2  0
#
#  The 0 reprecents the black tile in the n-puzzle game
#
#  @author Eduardo Ch. Colorado
#******************************************************************************/


# #############################################################################/
# How the algorithm works?
# To solve any given game board, a game tree is build with the initial 
# board as the root of the tree

# Breafly the solution is based on:

# A* algorithm -> to minimize f (cost function) where f = g + h
# g = number of moves (goal distance)
# h = manhattan or hamming distance (heuristic distance)

# In this code I used the word "neighbors" to named the different possible configurations  
# for a board when you swap the blank tile one place to the left, rigth, up or bottom. 
# For example :
    
# Initial board                                       "neighbors"
#    9  7  4                  9  0  4          9  7  4          9  7  4         9  7  4
#    1  0  3         ->       1  7  3          0  1  3          1  3  0         1  6  3
#    2  6  5                  2  6  5          2  6  5          2  6  5         2  0  5


# For further ilustration, we called n1, n2 and n3 to the "neighbours" of the initial board 
# and we assume n2 has the lowest h  value in the following diagram:
#
#                                number of
#                                iterations             Game Tree
# _______________________________________________________________
#     MinPQ                          0             initial board
#     -----                                              |
#     -----                                          /   |    \
#   n1-----                                         /    |     \
#   n3-----   node with              1             n1    n2    n3         three different 
#   n2----- <- lowest                                    ^                configurations
#              f cost                                    |
#                                    2          n1, n2, and n3 are
#                                    .          added into the minPQ
# The MinPQ always has the           .          but n2 will be pop
# board with lower f cost            .          in the next step,
# ready to be dequeued on            .          then its neightbours
# each iteration. Other              .          will be added again into 
# added boards with slightly                    the minPQ and ordered by  
# higher f cost are "waiting"                   its f cost. This process 
# its turn to be dequeued            .          is repeated until 
#                                    .          the goal is reached
#    
#                                   
# the number of iterations increases on each level of the game tree. The number of   
# moves in the other hand is recorder internally in the node object in this implementation
##############################################################################/z

class Solver(object):
    '''
    A class created to solve the 8-puzzle using a min priority queue and the 
    A* algorithm. It take a two dimensional array as a representaion of a 
    valid game board an search the minimum number of moves to solve the puzzle 
    optimizing the following cost funtion:

    f = g + h  where g are the number of moves and h is either the Manhattan or 
    Hamming distance

    '''

    def __init__(self, boardGame):
        self.board = boardGame
        self.moves = 0             # counter to count the moves required to reach the solution
        self.solutions = []        
        self.__solve()             # remember with the _ and __ we want to express this variables
                                   # should be considered as private
    def __solve(self): 
        state = 0
        search_node =  self.SearchNode(self.board,state,None)  # initial search node 
        seeker_node = self.aStar(search_node)                  # the search node is inmediately 
                                                               # wrapped with the aStar class and
                                                               # its methods
        
        # Uncomment if you want to use my code for the min prority queue intead of the one
        # provided by the heapq library
        # pq = minPQ.MinPQ()             # you can use this minPQ instead and compare which is faster
        # pq.insert(seeker_node)

        # Uncomment the two lines below to implement min heap queue provided by the heapq library

        pq = []                  # the heapq library requires an empty list to build the heap  
        heappush(pq,seeker_node) # and push the first element into this empty list using heappush 
        i = 0
        while(True):
            # seeker_node = pq.delMin()   # uncomment if you are using the minPQ
            seeker_node = heappop(pq)     # uncomment if you are using the heapq library
            search_node = seeker_node.get_Search_Node()
            old_search_node = search_node       # We keep the previous move because inside this node there are 
            state = old_search_node.state + 1   # an internal counter. state help us to keep track the internal  
                                                # counter of the node
            if(search_node.link == None): predecessor = None  # if there isn't any link to another node, this node 
            else: predecessor = search_node.link.current      # doesn't have a predecessor
            # Uncomment for debbuging    
            # print("Step: " + str(i))
            # print("Priority " + str(seeker_node.get_priority()))
            # print("moves: " + str(search_node.state))
            # print("manhattan " + str(search_node.current.manhattan()))
            # print("search node: ") 
            # print(search_node.current)
            # print('----------')
            # print("neighbours")

            # Game tree loop. We itarete through the neighbors 
            for neighbour in search_node.current.neighbors():
                if(not (neighbour == predecessor)):  # to avoid repetitions the current neighbor must be different to the previous configuration
                    # print(neighbour)
                    search_node = self.SearchNode(neighbour,state,old_search_node)
                    branch = self.aStar(search_node)
                    # pq.insert(branch)
                    heappush(pq,branch)  
            i += 1
            if(old_search_node.current.is_goal()): break
        # uncomment to know how many iteretions were required to find the solution
        print("iterations " + str(i))
        #From the goal board 
        self.moves = state       
        search_node = search_node.link
        while(search_node != None):          
            self.solutions.append(search_node.current)
            search_node = search_node.link

    # not all puzzles have solution, this method tell us before hand if a board is solvable        
    def isSolvable(self):
        pass

    def __iter__(self):
        while(len(self.solutions) > 0):
            yield self.solutions.pop()

    def number_of_moves(self):
        return self.moves - 1

    class SearchNode(object):
        '''
        Recursive data structure, a wrapper for the class board to make a linked list
        current: (Board) the current board instance in the solver 
        state:   (int) the current state (move) in the solver
        link:    (SearchNode) a link to the precedent SearchNode object
        '''
        def __init__(self, current, state, link):
            self.current = current
            self.state = state
            self.link = link

    # @functools.total_ordering
    class aStar(object):
        '''
        An extra layer for the board class. Here we are going to implement the
        aStar algorithm to solve the 8-puzzle. The priority queue will mantain 
        the priorities based on this computations
        '''
        def __init__(self, searchNode):
            self.sn = searchNode
            self.heuristic_distance = searchNode.current.manhattan() # can be replace with the hamming distance
            self.state = searchNode.state
            self.cost_function = self.heuristic_distance + searchNode.state

        def get_Search_Node(self):
            return self.sn
        
        def get_priority(self):
            return self.cost_function

        def __lt__(self, other):
            return (self.cost_function, self.heuristic_distance) < (other.cost_function, other.heuristic_distance)

        def __eq__(self, other):
            return self.cost_function == other.cost_function 

# Uncomment to create the game board game from a random generator
# n = 3   # size of the board
# a = list(random.sample(range(n*n),n*n))  
# blocks = [[a[n*i+j] for j in range(n)] for i in range(n) ]

# Uncomment to create the board game reading from a file
data_folder = Path("source_data/")
file_to_open = data_folder / "puzzle04.txt"
f = open(file_to_open)
n = int(f.readline())
blocks = [[ int(el) for el in line.split()] for line in f ]

board = Board(blocks)
# print("initial board")
# print(board)
# print("------")
solver = Solver(board)

# Check if the board is solvable and if so, show how to solve it
print("# of move to solve the board: "+  str(solver.number_of_moves()))
for solutions in solver:
    print(solutions)