import pygame
import math
import time


class Board:
    def __init__(self, config):
        self.col = config["BOARD_COLUMN_COUNT"] 
        self.row = config["BOARD_ROW_COUNT"] 
        self.save_dir = config["SAVE_DIR"]
        self.state = []
        for _ in range(self.row):
            self.state.append('0'*self.col)

    def toggleCell(self, cell):
        if self.getCellState(cell) == '0':
            self.state[cell[1]] = self.state[cell[1]][:cell[0]]+"1"+self.state[cell[1]][cell[0]+1:]
            return self.state[cell[1]][cell[0]]
        elif self.getCellState(cell) == '1':
            self.state[cell[1]] = self.state[cell[1]][:cell[0]]+"0"+self.state[cell[1]][cell[0]+1:]
            return self.state[cell[1]][cell[0]]
        else:
            return self.getCellState(cell)

    def importBoardState(self, file_name):
        state = []
        with open(file_name, "r") as f:
            for line in f:
                line = line.replace("\n", "")
                state.append(line)
        self.state = state


    def exportBoardState(self, state=None):
        # This function is a bit of a hack. Creates new file index based on the number of files in the "saves" +1
        # This function can overwrite another save if save files are deleted

        # THIS FUNCTION CAN BE USED TO SAVE THE STATE, IT WILL CREATE A NEW TXT FILE FOR THE STATE
        cwd = os.getcwd()

        try:
            os.mkdir(cwd+self.save_dir)
        except FileExistsError:
            print("Save file already exists") 

        # Filter files based on board state naming convention [b1.txt, b2.txt, ..., bn.txt]
        files = [f for f in glob.glob(cwd + "/" + self.save_dir + "*.txt")]

        # GET CURRENT STATE
        if not state:
            state = self.state

        highest_index = len(files)+1
        new_file_name = self.save_dir + "b" + str(highest_index) + ".txt"

        '''
        # TODO: At the moment this function doesn't work properly. Most likely an issue with incrementing the highest_index after loop
        highest_index = 0
        # FIND A NEW FILE NAME
        if files:
            # Return the last saved state
            for file in files:
                print(file)
                file_name = file.split("/")[-1]
                current_index = int(file_name[1:file_name.rfind(".")])
                print("Highest_index:", highest_index)
                print("current_index:", current_index)
                if current_index > highest_index:
                    print("Updating highest index", current_index)
                    highest_index = current_index 
                print("============================")
            highest_index += 1 
        # CREATE NEW SAVE FILE
        new_file_name = 'b'+ str(highest_index) + '.txt'
        '''

        with open(new_file_name, "w") as f:
            text = "\n".join(state)
            f.write(text)
    
    def setCell(self, cell, state='0'):
        # Individual changes to animals in board
        self.state[cell[1]] = self.state[cell[1]][:cell[0]]+"1"+self.state[cell[1]][cell[0]+1:]

    def setState(self, state):
        # Bulk import of entire state of board
        self.state = state

    def getState(self, state):
        return self.state

    def getNextGeneration(self, state=[], offset = 0):
        newState = []
        startTime = time.time()
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
        endTime = time.time()
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
