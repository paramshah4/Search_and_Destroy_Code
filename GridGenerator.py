import random
#This file generates in the grip
from graphics import *
class GridGenerator:
    def __init__(self,matrix,originalRowWindowSize,originalColWindowSize, probabilityDistribution):
        self.matrix =  matrix
        self.originalRowWindowSize = originalRowWindowSize
        self.originalColWindowSize = originalColWindowSize
        self.probabilityDistribution = probabilityDistribution

    def generate_grid(self,rowSize,colSize,rowWindowSize,colWindowSize):
        win = GraphWin("Agent Solver",self.originalRowWindowSize, self.originalColWindowSize)
        matrix = self.matrix
        textMatrix =  [[0 for x in range(rowSize)] for y in range(colSize)]
        for i in range(0, rowSize, 1):
            for j in range(0, colSize, 1):
                rect = Rectangle(Point(j*colWindowSize, i*rowWindowSize), Point((j+1)*colWindowSize, (i+1)*rowWindowSize))
                rect.setWidth(3)
                text = format(self.probabilityDistribution[i][j], '0.2f')
                if matrix[i][j] ==1:
                    rect.setFill("Lime Green")
                    Mines = Text(Point((j+0.5)*colWindowSize, (i+0.5)*rowWindowSize),text )
                elif matrix[i][j] ==2:
                    rect.setFill("sky blue")
                    Mines = Text(Point((j+0.5)*colWindowSize, (i+0.5)*rowWindowSize), text)
                elif matrix[i][j] ==3:
                    rect.setFill("Pink")
                    Mines = Text(Point((j+0.5)*colWindowSize, (i+0.5)*rowWindowSize), text)
                else:
                    rect.setFill("medium purple")
                    Mines = Text(Point((j+0.5)*colWindowSize, (i+0.5)*rowWindowSize), text)

                rect.draw(win)
                Mines.setTextColor("Black")
                Mines.draw(win)
                textMatrix[i][j] = Mines
        return win,textMatrix
