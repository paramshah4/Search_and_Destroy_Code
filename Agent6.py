import numpy as np

from sortedcontainers import SortedSet
import sys, threading
# sys.setrecursionlimit(10**7) # max depth of recursion
# threading.stack_size(2**27)  # new thread will get stack of such size
from Utility import *
from Analyser import *


class Agent6:
    x_cord = [0, 1, 0, -1]               #Coordinates acting as field of view for the agent-up, down, left,right
    y_cord = [1, 0, -1, 0]
    def __init__(self, matrix, probabilityDist, landscapeProbability, start_x, start_y, target_x, target_y, size,agentType):
        self.matrix = matrix
        self.probabilityDist = probabilityDist
        self.landscapeProbability = landscapeProbability
        self.size=size
        self.start_x = start_x
        self.start_y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.isEndPointReachable = False
        self.targetFound = False
        self.stepCount = 0
        self.examineCount = 0
        self.agentType = agentType
        self.probabilityInitialized = False
        self.queue = SortedSet()    # SortedSet acting as PRIORITY QUEUE
        self.parent = {}              # Maps Child -> Parent (with least distance from source node)
        self.discovered_grid = [[1 for x in range(size)] for y in range(size)]  # Knowledge grid of the agent while traversing
        self.dict_poppedpq = {}       # To keep a track of all cell being enetered into priority queue along with its fn,gn,hn values
        self.map = {}


    def distanceFromGoal(self, x1, y1,end_point_x,end_point_y):  # This function calculates distance of a node(x1,y1) from goal node (hn)
        return abs(end_point_x - x1) + abs(end_point_y - y1)

    def distanceFromSource(self, x_parent, y_parent, x_current,y_current):  # This function calculates least distance of a cell from source node
        if self.map.get(tuple([x_current,y_current])) == None:  # This checks whether this cell has already been in the queue or not
            self.map[tuple([x_current, y_current])] = self.map.get(tuple([x_parent, y_parent])) + 1
            self.parent[(x_current, y_current)] = (x_parent, y_parent)
            # If not then its distance from source node will be distance of parent node from source node +1
        else:
            # If yes then, we compare the value which is already present and the distance of source node(parent)+1, and assign the least one
            # and update the parent of the cell which has travelled the least distance from source node
            if (self.map.get(tuple([x_parent, y_parent])) + 1 > self.map.get(tuple([x_current, y_current]))):
                self.map[tuple([x_current, y_current])] = self.map.get(tuple([x_current, y_current]))
            else:
                self.map[tuple([x_current, y_current])] = self.map.get(tuple([x_parent, y_parent])) + 1
                self.parent[(x_current, y_current)] = (x_parent, y_parent)

        return self.map.get(tuple([x_current, y_current]))  # return gn value of the node (distance from source)

    def aStar(self, matrix, x, y, end_point_x,end_point_y):  # Main Function of A* Algorithm starting from node(x,y)
 
        self.parent={}
        self.map={}
        self.dict_poppedpq = {}
        self.queue.clear()
        visited = [[0 for x in range(self.size)] for y in range(self.size)]  # initializing visited matrix to keep track
        # of all nodes which have been expanded
        self.map[tuple([x, y])] = 0  # Adding source node in map and updating its gn value to 0
        self.queue.add((self.distanceFromGoal(x, y,end_point_x,end_point_y), self.distanceFromGoal(x, y,end_point_x,end_point_y), 0, x,y))  # Adding source to queue
        while self.queue.__len__() > 0:  # Loop runs until queue is empty
            #print("check")
            #print(self.queue)
            curr_fn, curr_hn, curr_gn, curr_x, curr_y = self.queue.pop(0)  # popping node with priority in order of fn,hn,gn
            #print("start1")
            if (curr_x == end_point_x and curr_y == end_point_y):  # Checks whether popped node is goal node
                return True

            if visited[curr_x][curr_y] == 1:  # If already node has been expanded we dont expand that node again and continue
                continue

            #self.nodeExplored += 1  # Increment the nodes explored

            visited[curr_x][curr_y] = 1  # Mark the node that has expanded as visited

            for i in range(0, 4):  # This loop generates the children of the node popped from the queue

                x_temp = Agent6.x_cord[i] + curr_x
                y_temp = Agent6.y_cord[i] + curr_y

                if (x_temp >= 0 and x_temp < self.size and y_temp >= 0 and y_temp < self.size
                        and visited[x_temp][y_temp] == 0 and matrix[x_temp][y_temp] != 0):  # Check if index is in the range

                    # If the child is unblocked , calculate fn,gn and hn and check whether it is present in the queue
                    # If yes then we remove the old node and enter the same node with the least fn value among the two
                    # If no then we just add the node into the queue along with its fn,gn.hn value

                    hn = self.distanceFromGoal(x_temp, y_temp, end_point_x, end_point_y)
                    gn = self.distanceFromSource(curr_x, curr_y, x_temp, y_temp)
                    fn = gn + hn

                    #print(self.dict_poppedpq)
                    if (x_temp, y_temp) in self.dict_poppedpq:  # Check if child is already in the queue
                        fnold, hnold, gnold = self.dict_poppedpq[(x_temp, y_temp)]
                        self.queue.remove((fnold, hnold, gnold, x_temp, y_temp))

                        # removing node to prevent same node with different fn value to exists in queue

                    self.dict_poppedpq[(x_temp, y_temp)] = (fn, hn, gn)  # Updating map to keep track of old fn,gn,hn values

                    self.queue.add((fn, hn, gn, x_temp, y_temp))
        return False  # Function returns false if all possible path are traversed and we do not reach the goal node

    def aStarUtil(self):  # Function to call main A* algorithm function
        #self.isEndPointReachable = self.aStar(self.start_x, self.start_y,self.start_x,self.start_y)
        #if self.isEndPointReachable is True:

        #self.traversingPath(self.start_x, self.start_y)


        self.mainAstarProb(self.size)
        return self.examineCount,self.stepCount




    def mainAstarProb(self,dim):

        landscapeProbab = self.landscapeProbability[self.matrix[self.start_x][self.start_y]]
        Utility.updateProbabilities(self.probabilityDist, landscapeProbab, dim, self.start_x, self.start_y)

        while(1):
            encounteredBlock = False
            if self.agentType == "agent6":
                endx,endy=Utility.getProbabContainTarget(self.probabilityDist, dim, self.start_x, self.start_y)
            elif self.agentType == "agent7":
                endx, endy = Utility.getProbabFindingTarget(self.probabilityDist, landscapeProbab, dim, self.start_x, self.start_y)
            else:
                endx, endy =Utility.getProbabFindingTargetAgent8(self.probabilityDist, landscapeProbab, dim, self.start_x, self.start_y)

            foundPath=self.aStar(self.discovered_grid,self.start_x,self.start_y,endx,endy)
            landscapeProbab = self.landscapeProbability[self.matrix[endx][endy]]
            if foundPath is False:
                Utility.updateProbabilities(self.probabilityDist,0,dim,endx,endy)
                continue
            else:
                path=self.getAstarPath(endx,endy)
                for coord in path:
                    c_x=coord[0]
                    c_y=coord[1]
                    if self.matrix[c_x][c_y]==0:
                        self.discovered_grid[c_x][c_y]=0
                        self.examineCount+=1
                        Utility.updateProbabilities(self.probabilityDist, 0, dim, c_x, c_y)
                        self.start_x=self.parent[(c_x,c_y)][0]
                        self.start_y=self.parent[(c_x,c_y)][1]
                        encounteredBlock=True
                        break
                    else:
                        self.discovered_grid[c_x][c_y]=self.matrix[c_x][c_y]
                        self.stepCount+=1

                if encounteredBlock is False:
                    c_x=path[-1][0]
                    c_y=path[-1][1]
                    self.examineCount += 1
                    if c_x == self.target_x and c_y == self.target_y and np.random.uniform() > landscapeProbab:
                        break

                    Utility.updateProbabilities(self.probabilityDist, landscapeProbab, dim, c_x, c_y)
                    self.start_x=c_x
                    self.start_y=c_y
                    continue

        return



    def getAstarPath(self,end_point_x,end_point_y):
        currnode = (end_point_x, end_point_y)
        findpath = []
        findpath.append(currnode)
        while currnode != (self.start_x, self.start_y):
            findpath.append(self.parent[currnode])
            currnode = self.parent[currnode]
        findpathrev = findpath[::-1]  # reversing path to start traversing from source node
        return findpathrev


    # def getPathlength(self):  # Function to get the shortest path length from source node to goal node
    #     currnode = (self.goal_x, self.goal_y)  # Set the current nide as the goal node
    #     findpath = []  # list to store path from source node to goal node
    #     findpath.append(currnode)
    #
    #     pathCount = 0  # Variable to calculateshortest path length
    #     while (currnode != (self.x, self.y)):  # We backtrack the path from goal node until we reach the start node
    #
    #         pathCount += 1
    #         findpath.append(self.parent[
    #                             currnode])  # We append the parent of each node and update the currnode with its parent node.
    #         currnode = self.parent[currnode]
    #     return pathCount  # return total nodes which lie in the shortest path
    #
    # def traversingPath(self, end_point_x, end_point_y):
    #     currnode = (end_point_x, end_point_y)
    #     findpath = []
    #     findpath.append(currnode)
    #     res = True
    #     trajectoryCount = 0
    #     while currnode != (self.start_x, self.start_y):
    #         findpath.append(self.parent[currnode])
    #         currnode = self.parent[currnode]
    #     findpathrev = findpath[::-1]  # reversing path to start traversing from source node
    #     # print("Path is:")
    #     # print(findpathrev)
    #     flag = False  # Used to perform action when we encounter a block node
    #     blockx = 0
    #     blocky = 0
    #     for tuplecoord in findpathrev:  # Traversing the path
    #         coordx = tuplecoord[0]
    #         coordy = tuplecoord[1]
    #         if self.matrix[coordx][coordy] == 0:  # If the cell is blocked, we break out of the loop and call Astar from its parent node.
    #             self.discovered_grid[coordx][coordy] = self.matrix[coordx][coordy]  # Update the discovered grid.
    #             self.examineCount += 1;
    #             flag = True
    #             blockx = coordx  # Storing the coordinates of the node which is blocked
    #             blocky = coordy
    #             break
    #         else:
    #             # If the cell is unblocked , we increase our field of view by updating its child in discovered grid world.
    #             trajectoryCount = trajectoryCount + 1  # Increment the trajectory length
    #             self.discovered_grid[coordx][coordy] = self.matrix[coordx][coordy]  # Update the discovered gridworld Update the final discovered gridworld
    #
    #
    #
    #     # adding trajectory length up and subtracting -1 to avoid repeatation of same cell
    #     self.stepCount = self.stepCount + trajectoryCount - 1
    #     if (flag is True):  # this is true when we encounter a block cell in the path so we call astar again from current node's parent
    #         #print("1stPart")
    #         self.updateProbablity(0, self.parent[(blockx, blocky)][0], self.parent[(blockx, blocky)][1], blockx, blocky)
    #     else:
    #         self.examineCount += 1
    #         landscapeProbab = self.landscapeProbability[self.matrix[end_point_x][end_point_y] - 1]
    #         #print(landscapeProbab,self.matrix[end_point_x][end_point_y])
    #         if end_point_x == self.target_x and end_point_y == self.target_y and np.random.uniform() > landscapeProbab:
    #             self.targetFound = True
    #             return True
    #         else:
    #             #print("2ndPart")
    #             self.updateProbablity(landscapeProbab, end_point_x,end_point_y,end_point_x,end_point_y)
    #
    #     return res  # Returns whether path was found or not
    #
    #
    #
    # def updateProbablity(self,landscapeProbab,astar_start_x,astar_start_y,examine_coord_x,examine_coord_y):
    #     #print("MainUpdateProbab")
    #     Utility.updateProbabilities(self.probabilityDist, landscapeProbab, self.size, examine_coord_x, examine_coord_y)
    #     if self.agentType=="agent6":
    #         #print("CHECKING")
    #         maxP_x, maxP_y = Utility.getProbabContainTarget(self.probabilityDist, self.size, astar_start_x, astar_start_y)
    #         #print(maxP_x, maxP_y)
    #     elif self.agentType=="agent7":
    #         maxP_x, maxP_y = Utility.getProbabFindingTarget(self.probabilityDist,self.landscapeProbability, self.matrix, self.size,astar_start_x, astar_start_y)
    #     else:
    #         maxP_x, maxP_y = Utility.getProbabFindingTargetAgent8(self.probabilityDist,self.landscapeProbability, self.matrix, self.size, astar_start_x, astar_start_y)
    #     #print("Examining Coodrinates")
    #     # print(examine_coord_x,examine_coord_y)
    #     # print("Maximum probablity coordinates")
    #     # print(maxP_x,maxP_y)
    #     res = self.aStar(self.discovered_grid,astar_start_x, astar_start_y, maxP_x, maxP_y)
    #     #print("astar1")
    #     if (res is True):
    #         #print("astar2")
    #         # If we found the path , we recursively call the findPath() function until we get a path with all unblocked nodes in full gridworld.
    #         return self.traversingPath(maxP_x, maxP_y)
    #     else:
    #         print("astar3")
    #         #print("3rdPart")
    #         self.updateProbablity(0,astar_start_x,astar_start_y ,maxP_x, maxP_y)
    #
