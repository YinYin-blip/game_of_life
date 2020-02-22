import pygame
import math

CELL_SIZE = 10
CELL_SPACING = 1

class Board:
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.state = []
        for _ in range(self.row):
            self.state.append('0'*self.col)

    def isValidState(self):
        if self.row != len(self.state):
            return False
        for row in self.state:
            if len(row) != self.col:
                return False
            for animal in row:
                if animal != 1 or animal != 0:
                    return False
        return True

    def toggleCell(self, cell):
        if self.getCellState(cell) == '0':
            self.state[cell[1]] = self.state[cell[1]][:cell[0]]+"1"+self.state[cell[1]][cell[0]+1:]
            return self.state[cell[1]][cell[0]]
        elif self.getCellState(cell) == '1':
            self.state[cell[1]] = self.state[cell[1]][:cell[0]]+"0"+self.state[cell[1]][cell[0]+1:]
            return self.state[cell[1]][cell[0]]
        else:
            return self.getCellState(cell)

    def setState(self, state):
        self.state = state

    def getState(self, state):
        return self.state

    def getNextGeneration(self, state=[], offset = 0):
        newState = []
        for rowIndex, row in enumerate(self.state):
            newRow = ''
            for colIndex, col in enumerate(row):
                '''
                For a space that is 'populated':
                    (1) Each cell with one or no neighbors dies, as if by solitude.
                    (2) Each cell with four or more neighbors dies, as if by overpopulation.
                    (3) Each cell with two or three neighbors survives.
                For a space that is 'empty' or 'unpopulated'
                    (4) Each cell with three neighbors becomes populated.
                '''
                cell = (colIndex, rowIndex)
                if self.getCellState(cell) == '1':
                    if self.countNeighbors(cell) <= 1:
                        newRow += "0"
                    elif self.countNeighbors(cell) >= 4:
                        newRow += "0"
                    else:
                        newRow += "1"
                elif self.getCellState(cell) == '0':
                    if self.countNeighbors(cell) == 3:
                        newRow += "1"
                    else:
                        newRow += "0"
                else:
                    assert(self.getCellState(cell) == '0' or self.getCellState(cell) == "1")
            newState.append(newRow)
        print(newState)
        return newState

    def getCellState(self, cell):
        if (cell[0] >= 0) and (cell[0] < self.col) and (cell[1] >= 0) and (cell[1] < self.row):
            return self.state[cell[1]][cell[0]]
        else:
            return '2'

    def countNeighbors(self, cell):
        count = 0
        cells = getCells(cell)
        for cell in cells:
            if self.getCellState(cell) == "1":
                count+=1
        return count

def getCells(cell):
    cells = []
    for x in range(-1, 2, 1):
        for y in range(-1, 2, 1):
            cells.append((cell[0]+x,cell[1]+y))
    del cells[4]
    return cells
