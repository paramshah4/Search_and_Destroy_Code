import numpy as np
from Utility import *
from Analyser import *
class stationaryTarget:
    def __init__(self,matrix,probabilityDistribution,probOfLandScapes,start_x,start_y,target_x,target_y,rowSize,colSize,grid,rowWindowSize,colWindowSize,textMatrix,ruleType,landScapeType):
        print("test stationary")
        self.matrix = matrix
        self.probabilityDistribution = probabilityDistribution
        self.probOfLandScapes = probOfLandScapes #negative probab of different landscapes
        self.start_x = start_x
        self.start_y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.targetFound = False
        self.rowSize = rowSize
        self.columnSize = colSize
        self.numberOfSteps = 0
        self.grid = grid
        self.rowWindowSize = rowWindowSize
        self.colWindowSize = colWindowSize
        self.textMatrix = textMatrix
        self.ruleType = ruleType
        self.landScapeType = landScapeType
        self.isStationary = True
        self.distanceTravelled = 0
        self.trials = 25

    def distanceFromGoal(self,x1, y1):
        return abs(self.goal_x - x1) + abs(self.goal_y-y1)

    def astar(self,resultsSearches, resultsCost):



    def solve(self,resultsSearches, resultsCost):
        location_x = np.random.randint(self.rowSize)
        location_y = np.random.randint(self.columnSize)
        while not self.targetFound:
            self.numberOfSteps+=1
            landscapeProbab = self.probOfLandScapes[self.matrix[location_x][location_y]-1] #negative probab
            if location_x==self.target_x and location_y == self.target_y and np.random.uniform() > landscapeProbab:
                print("Target found at " ,location_x, location_y )
                print("Number of Steps: ", self.numberOfSteps)
                print("landscape : " , self.landScapeType)
                resultsSearches[self.landScapeType] += self.numberOfSteps
                self.targetFound = True
                Utility.resetProbabilityDistribution(self.probabilityDistribution,self.rowSize,self.columnSize)
                return Analyser(self.matrix,self.rowSize,self.columnSize,self.ruleType,self.isStationary,self.numberOfSteps,self.distanceTravelled,self.trials,self.landScapeType)
            else:
                #Bayessian updating after the target is not found
                Utility.updateProbabilities(self.probabilityDistribution,
                                               landscapeProbab,
                                               self.rowSize,
                                               self.columnSize,
                                               location_x,
                                               location_y,
                                               self.grid,
                                               self.rowWindowSize,
                                               self.colWindowSize,
                                               self.textMatrix)
                if self.ruleType == 'Rule 1':
                  location_x,location_y,d =  Utility.getProbabContainTarget(self.probabilityDistribution,self.rowSize,self.columnSize,location_x,location_y)
                  resultsCost[self.landScapeType] +=d
                elif self.ruleType == 'Rule 2':
                    location_x,location_y,d =  Utility.getProbabFindingTarget(self.probabilityDistribution,self.probOfLandScapes,self.matrix,self.rowSize,self.columnSize,location_x,location_y)
                    resultsCost[self.landScapeType] +=d
                else:
                    #(row, col,location_x,location_y,probOfLandScapes,originalMatrix,probMatrix
                    location_x,location_y,d =  Utility.calculateLocation(self.rowSize,self.columnSize,location_x,location_y,self.probOfLandScapes,self.matrix,self.probabilityDistribution)
                    resultsCost[self.landScapeType] +=d












