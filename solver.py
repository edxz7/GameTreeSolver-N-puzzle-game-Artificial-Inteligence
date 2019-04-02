import minPQ
from board import Board # from the file import the class name
import random
from heapq import heappop, heappush
from pathlib import Path

#*****************************************************************************
#  Execution:    python solver.py 
#  Dependencies: none
#
#  Game tree solver. From the initial boar game as the root of the tree, a game 
#  tree is constructed. Using a min priority queue and the A* algorithm the solution
#  with the minimum number of moves it's find and printed.
#
#  You can build your own board of size n x n using the following example format as
#  an example:
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
        self.moves = 0
        self.solutions = []
        self.__solve()

    def __solve(self): 
        state = 0
        search_node =  self.SearchNode(self.board,state,None)
        seeker_node = self.aStar(search_node)              
        # Uncomment if you want use my code for the min prority queue intead of the one
        # provided in the heapq library
        # pq = minPQ.MinPQ()
        # pq.insert(seeker_node)
        # Uncomment the two lines below to implement min heap queue provided by the heapq
        # library 
        pq = []                  # the heapq library requires an empty list to build the heap  
        heappush(pq,seeker_node) # and push the first element into this empty list using heappush 
        i = 0
        while(True):
            # seeker_node = pq.delMin()   # uncomment if you are using the minPQ
            seeker_node = heappop(pq)     # uncomment if you are using the heapq library
            search_node = seeker_node.get_Search_Node()
            old_search_node = search_node
            state = old_search_node.state + 1

            if(search_node.link == None): predecessor = None
            else: predecessor = search_node.link.current
            # Uncomment for debbuging    
            # print("Step: " + str(i))
            # print("Priority " + str(seeker_node.get_priority()))
            # print("moves: " + str(search_node.state))
            # print("manhattan " + str(search_node.current.manhattan()))
            # print("search node: ") 
            # print(search_node.current)
            # print('----------')
            # print("neighbours")

            # Game tree loop
            for neighbour in search_node.current.neighbors():
                if(not (neighbour == predecessor)):
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
n = 3   # size of the board
a = list(random.sample(range(n*n),n*n))  
blocks = [[a[n*i+j] for j in range(n)] for i in range(n) ]

# Uncomment to create the board game reading from a file
data_folder = Path("source_data/")
file_to_open = data_folder / "puzzle05.txt"
f = open(file_to_open)
n = int(f.readline())
blocks = [[ int(el) for el in line.split()] for line in f ]

board = Board(blocks)
# print(board)
solver = Solver(board)

# Check if the board is solvable and if so, show how to solve it
print("# of move to solve the board: "+  str(solver.number_of_moves()))
for solutions in solver:
    print(solutions)