#******************************************************************************/
#  Max priority queue
#
#  @author Eduardo Ch. Colorado
#******************************************************************************/

#   PRIORITY QUEUES 
# API principal ops:
# Insert an element into the heap
# Remove the minimum/maximum (like a queue remove the oldest and a stack remove the newest)
# A priority queue get items on the fly and dispach the largest(smallest) on demand.
# In this implementation of a min priority queue, a heap is used. 
# A heap is conceptualized as a complete binary tree that satisfy the heap ordered property 
#
# DEF: A binary tree is heap ordered if any key in a node is greater (smaller) than its two child nodes 
#
# Each entry in the array is thought of as a leaf of a binary tree. The largest(smallest) key is
# always put in the root. For convenience the zero entry is ignore
#
#   Conceptual visualization of a priority queue.
#     0   1   2   3   4   5   6   7   8   9
#   null  T   S   R   P   N   O   A   E   I
#
#                           1 | T
#                         /       \                  This arragement allows us 
#                        /         \                 find the parent of each leaf 
#                   2 | S           3 | R            using integer division
#                  /     \         /     \           for example  6//2 = 3 , 7//2 = 3,  
#                 /       \       /       \          the entries 6 and 7 have 3 as its paren 
#            4 | P    5 | N      6 | O     7 | A
#          /       \
#         /         \
#    8 | E          9 | I
#        
#        A heap-ordered complete binary three


class MaxPQ(object):
    def __init__(self):
        self.pq = [0]
        self.N = 0
    
    def delMax(self):
        #raise a underflow exception if the priority queue is empty
        if(self.N == 0): raise Exception("Underflow")
        #Save the root value
        max_el = self.pq[1]
        #put the last element in the root
        try:self.pq[1] = self.pq.pop()
        except: pass
        self.N -= 1
        #"sink" the element to its rigth place
        self.__sink(1)
        
        return max_el
    
    def max(self):
        return self.pq[self.N]

    def insert(self,x):
        self.N += 1
        self.pq.append(x)
        self.__swim(self.N)
        

    def size(self):
        return self.N    

    def __sink(self,k):
        # Last entry on the list
        N = self.N
        #we can sink the node k up to the last leaf (which is in the last entry of the list)
        while(2*k <= N): 
            j = 2*k
            # First we select the greatest of the two childs of the node k
            if(j < N and self.__less(j,j+1)): j += 1
            # If the value of node k is not less than the value of the selected node we break the loop (the node k obey the heap oreder)
            if(not self.__less(k,j)): break
            # if we don't break thw loop, we exchange the value of the child node with the value of the parent
            self.__exch(j,k)
            # finally we go up one level on the tree and repeate the process util we reach the root of the tree
            k = 2*k
            #when we left this iteration we will end up with a complete oredered binary heap


    def __swim(self, k):
        while(k>1 and self.__less(k//2,k)): 
            self.__exch(k//2,k)
            k = k//2

    def __less(self, i, j):
        return self.pq[i] <= self.pq[j]

    def __exch(self, i, j):
        temp = self.pq[i]
        self.pq[i] = self.pq[j]
        self.pq[j] = temp
        

pq = MaxPQ()

pq.insert(2)
pq.insert(20)
pq.insert(200)
pq.insert(100)
pq.insert(245)
pq.insert(1)
print(pq.delMax())
print(pq.delMax())
print(pq.delMax())
print(pq.delMax())
print(pq.delMax())
print(pq.delMax())
