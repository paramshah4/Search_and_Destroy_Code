import random
import numpy as np
from graphics import *

class Utility:
   @staticmethod
   def matrixGenerator(row, col):
       Matrix = [[0 for x in range(col)] for y in range(row)]
       probabDistribution = [[0 for x in range(col)] for y in range(row)]
       intialProbability = 1/(row*col)
       for i in range(0, row, 1):
            for j in range(0, col, 1):
                prob = random.random()
                probabDistribution[i][j] = intialProbability
                if prob <= 0.3 :
                    Matrix[i][j]=0
                else:
                    random_number = random.randint(1, 3)
                    Matrix[i][j] = random_number
       return Matrix, probabDistribution



   def findingStartEndPoints(original_matrix,rowSize,colSize):
        flag=True
        start_x=0
        start_y=0
        target_x=rowSize-1
        target_y=colSize-1
        while flag is True:
            start_x = np.random.randint(rowSize)
            start_y = np.random.randint(colSize)
            target_x = np.random.randint(rowSize)
            target_y = np.random.randint(colSize)
            if original_matrix[start_x][start_y] !=0 and original_matrix[target_x][target_y] !=0:
                flag=False
        return (start_x,start_y),(target_x,target_y)


   #method to update the probabilities and normalizing
   @staticmethod
   def updateProbabilities(probMatrix, falseNegative, size, location_x, location_y):
       #print("UpdateProb")
       denominator = probMatrix[location_x][location_y] * falseNegative + 1 - probMatrix[location_x][location_y]
       updateInGrid = False #make it true to update the grid
       sum = 0.0
       for i in range(0, size, 1):
           for j in range(0, size, 1):
               if i==location_x and j == location_y:
                   probMatrix[i][j] = (probMatrix[location_x][location_y] * falseNegative) / denominator
               else:
                   probMatrix[i][j] = probMatrix[i][j] / denominator;
               #print(probMatrix[i][j])
               sum = sum + probMatrix[i][j]

       for i in range(0, size, 1):
           for j in range(0, size, 1):
               probMatrix[i][j] = probMatrix[i][j]*(1/sum)
           #     print(probMatrix[i][j], end=" ")
           # print("\n")

       # for i in range(size):
       #     for j in range(size):
       #         print(probMatrix[i][j], end=" ")
       #     print("\n")

   def getDistanceBetweenPoints(x1, y1, x2, y2):  # This function calculates distance of a node(x1,y1) from goal node (hn)
       return abs(x2 - x1) + abs(y2 - y1)

   #Rule 1: At any time, search the cell with the highest probability of containing the target.
   @staticmethod
   def getProbabContainTarget(probMatrix, size, start_x, start_y):
       #print("getProbabContain")
       max = -1.0
       minDist = 999999
       x_coord = 0;
       y_coord = 0;
       max_prob_coord=[]
       min_dist_from_source=[]
       for i in range(size):
           for j in range(size):
               if probMatrix[i][j] > max:
                   max = probMatrix[i][j]
                   max_prob_coord.clear()
                   max_prob_coord.append((i,j))
               elif probMatrix[i][j] == max:
                   max_prob_coord.append((i, j))

       for coord in max_prob_coord:
           coordx=coord[0]
           coordy=coord[1]
           distance=Utility.getDistanceBetweenPoints(start_x,start_y,coordx,coordy)
           if distance < minDist:
               minDist = distance
               min_dist_from_source.clear()
               min_dist_from_source.append((coordx,coordy))
           elif distance == minDist:
               min_dist_from_source.append((coordx, coordy))

       #print(min_dist_from_source)
       end_point_x,end_point_y=random.choice(min_dist_from_source)
       #print("After")


       return end_point_x,end_point_y


   #Rule 2: At any time, search the cell with the highest probability of finding the target.
   @staticmethod

   def getProbabFindingTarget(probMatrix,landscapeProbab,size,start_x, start_y):
       max = -1.0
       minDist = 999999
       x_coord = 0;
       y_coord = 0;
       max_prob_coord=[]
       min_dist_from_source=[]
       for i in range(size):
           for j in range(size):
               temp_probab = probMatrix[i][j]*(1-landscapeProbab)
               if temp_probab > max:
                  max = temp_probab
                  max_prob_coord.clear()
                  max_prob_coord.append((i, j))
               elif temp_probab == max:
                   max_prob_coord.append((i, j))

       for coord in max_prob_coord:
           coordx=coord[0]
           coordy=coord[1]
           distance=Utility.getDistanceBetweenPoints(start_x,start_y,coordx,coordy)
           if distance < minDist:
               minDist = distance
               min_dist_from_source.clear()
               min_dist_from_source.append((coordx,coordy))
           elif distance == minDist:
               min_dist_from_source.append((coordx, coordy))

       end_point_x,end_point_y=random.choice(min_dist_from_source)
       return end_point_x,end_point_y


   @staticmethod
   def getProbabFindingTargetAgent8(probMatrix,landscapeProbab,size,start_x, start_y):
       max = -1.0
       minDist = 999999
       x_coord = 0;
       y_coord = 0;
       max_prob_coord = []
       min_dist_from_source = []
       for i in range(0, size, 1):
           for j in range(0, size, 1):
               if i == start_x and j == start_y:
                   continue
               temp_probab = probMatrix[i][j]*(1-landscapeProbab)
               distance = Utility.getDistanceBetweenPoints(start_x, start_y, i, j) / 2*size
               temp_probab=temp_probab/distance
               if temp_probab > max:
                   max = temp_probab
                   max_prob_coord.clear()
                   max_prob_coord.append((i, j))
               elif temp_probab == max:
                   max_prob_coord.append((i, j))

       for coord in max_prob_coord:
           coordx = coord[0]
           coordy = coord[1]
           distance = Utility.getDistanceBetweenPoints(start_x, start_y, coordx, coordy)
           if distance < minDist:
               minDist = distance
               min_dist_from_source.clear()
               min_dist_from_source.append((coordx, coordy))
           elif distance == minDist:
               min_dist_from_source.append((coordx, coordy))

       end_point_x, end_point_y = random.choice(min_dist_from_source)
       return end_point_x, end_point_y


   @staticmethod
   def resetProbabilityDistribution(probMatrix,row,col):
       intialProbability = 1/(row*col)
       for i in range(0, row, 1):
            for j in range(0, col, 1):
                probMatrix[i][j] = intialProbability

   @staticmethod
   def calculateLocation(row, col,location_x,location_y,probOfLandScapes,originalMatrix,probMatrix):
       min = -1.0
       d = 0
       x_coord = 0;
       y_coord = 0;
       for i in range(0,row,1):
           for j in range(0,col,1):
               if i==location_x and j == location_y:
                   continue
               d = abs((i-location_x)) + abs((j-location_y))
               temp_probab = ((probMatrix[i][j]* probOfLandScapes[originalMatrix[i][j]-1]) / (d))
               if(min <  temp_probab):
                   min = temp_probab
                   x_coord = i;
                   y_coord = j;
       return x_coord,y_coord,d

   @staticmethod
   def makeTransitions(row,col,location_x, location_y,originalMatrix,transitions):
       transitions.append(originalMatrix[location_x][location_y])
       tempLandScapes = []
       if location_x - 1 >= 0 and originalMatrix[location_x-1][location_y] != originalMatrix[location_x][location_y]:
         tempLandScapes.append(originalMatrix[location_x-1][location_y])
       if location_x + 1 < row and originalMatrix[location_x+1][location_y] != originalMatrix[location_x][location_y]:
         tempLandScapes.append(originalMatrix[location_x+1][location_y])
       if location_y - 1 >= 0 and originalMatrix[location_x][location_y-1] != originalMatrix[location_x][location_y]:
         tempLandScapes.append(originalMatrix[location_x][location_y-1])
       if location_y + 1 < col and originalMatrix[location_x][location_y+1] != originalMatrix[location_x][location_y]:
         tempLandScapes.append(originalMatrix[location_x][location_y+1])
       if len(tempLandScapes)!=0:
         transitions.append(random.choice(tempLandScapes))

   @staticmethod
   def updateMovementProbability(row,col,trasitions, probMatrix,originalMatrix,temporaryProbability):
       sum = 0.0
       if len(trasitions)<=1:
           return
       for i in range(0,row,1):
          for j in range(0,col,1):
              if originalMatrix[i][j] in trasitions:
                  intermediate = float(0.0)
                  if i - 1 >= 0 :
                     if originalMatrix[i - 1][j] != originalMatrix[i][j] and originalMatrix[i - 1][j] in trasitions :
                            intermediate+=probMatrix[i-1][j]
                  if i + 1 < row:
                     if originalMatrix[i + 1][j] != originalMatrix[i][j] and originalMatrix[i + 1][j] in trasitions:
                            intermediate+=probMatrix[i+1][j]
                  if j - 1 >=0:
                     if originalMatrix[i][j-1] != originalMatrix[i][j] and originalMatrix[i][j-1] in trasitions:
                            intermediate+=probMatrix[i][j-1]
                  if j + 1 < col:
                     if originalMatrix[i][j+1] != originalMatrix[i][j] and  originalMatrix[i][j+1] in trasitions:
                            intermediate+=probMatrix[i][j+1]
                  temporaryProbability[i][j] = intermediate
                  #print("intermediate:", intermediate)
              else:
                  temporaryProbability[i][j] = 0.0

              sum+=temporaryProbability[i][j]
              #print("moving target sum :" , sum)
       #print("here")
       for i in range(0,row,1):
            for j in range(0,col,1):
                   probMatrix[i][j] = temporaryProbability[i][j]/sum
