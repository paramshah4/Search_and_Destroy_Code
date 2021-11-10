#This is the POJO class for the analysing purpose
class Analyser:
    def __init__(self,originalMatrix,row,col,ruleName,isStationary,numberOfSearch,distanceTravelled,numberOfIteration,typeOflandScape):
        self.originalMatrix=originalMatrix
        self.sizeOfBoard = row*col
        self.ruleName = ruleName
        self.isStationary = isStationary
        self.numberOfSearch = numberOfSearch
        self.distanceTravelled = distanceTravelled
        self.numberOfIteration = numberOfIteration
        self.typeOflandScape = typeOflandScape


    def to_dict(self):
        return {
            'Board Size':self.sizeOfBoard,
            'Rule Name' : self.ruleName,
            'Is Stationary':self.isStationary,
            'Number of Search':self.numberOfSearch,
            'Distance Travelled' : self.distanceTravelled,
            'Landscape' : self.typeOflandScape
        }
