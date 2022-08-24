import pygame
import time
import math

from config import board_conf 
from board import *

def main(config):
    print(config)
    CELL_SIZE = config["CELL_SIZE"]
    CELL_SPACING = config["CELL_SPACING"]
    square_space = CELL_SIZE + CELL_SPACING
    col = config["BOARD_COLUMN_COUNT"]
    row = config["BOARD_ROW_COUNT"]
    sleep_time = config["SLEEP_TIME"]

    # SAVE VARIABLES
    is_save_mode = config["IS_SAVE_MODE"]
    to_save = False
    is_initial_state_saved = False

    board = Board(config)

    width = col*(square_space)
    height = row*(square_space)
    gameDisplay = pygame.display.set_mode((width,height))
    gameDisplay.fill((255,255,255))
    pygame.display.set_caption("Gamolyf")

    # For each cell, draw a rectangle
    for col in range(board.col):
        for row in range(board.row):
            pygame.draw.rect(gameDisplay, (0,0,0), ((col*(square_space), row*(square_space)), (CELL_SIZE, CELL_SIZE)))

    pygame.display.update()
    gameExit = False
    isPlay = False

    while not gameExit:
        toggleDraw = False
        gameTicker = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if isPlay:
                # Auto-run setting loop 
                while(isPlay):
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.key.key_code("space"):
                            print("toggle isPlay:", isPlay)

                            isPlay = False
                            pygame.event.clear()
                            pygame.event.set_allowed(None)
                            break
                    board.setState(board.getNextGeneration())
                    draw(board, gameDisplay, square_space, CELL_SIZE)
                    time.sleep(sleep_time)
            else:
                if pygame.mouse.get_pressed() == (1,0,0):

                    # ENTERING DRAW STATE
                    if (event.type == pygame.MOUSEMOTION):
                        pos = pygame.mouse.get_pos()
                        pos = fromLocationToGrid(pos, square_space)
                        board.setCell(cell=pos, state='1')
                        drawCell(board, gameDisplay, pos, square_space, CELL_SIZE)
                if event.type == pygame.KEYDOWN:

                    # Manual board iteration
                    if event.key == pygame.key.key_code("return"):
                        if not is_initial_state_saved and is_save_mode:
                            # COPY THE EXISTING STATE
                            copy_state = board.state.copy()
                            board.exportBoardState(state=copy_state)
                            
                        print("Iterate board")

                        #Start event key is RETURN
                        board.setState(board.getNextGeneration())
                        draw(board, gameDisplay, square_space, CELL_SIZE)

                    # Start auto-run board setting 
                    if event.key == pygame.key.key_code("p"):
                        if not is_initial_state_saved and is_save_mode:
                            # COPY THE EXISTING STATE
                            copy_state = board.state.copy()
                            board.exportBoardState(state=copy_state)

                        print("Toggle isPlay:", isPlay)

                        pygame.event.clear()
                        pygame.event.set_allowed(pygame.KEYDOWN)
                        isPlay = True
            
                        


def drawCell(board, display, cell, square_space, CELL_SIZE):
    col, row = cell[0], cell[1]
    state = board.getCellState(cell) 
    
    if state == '1':
        pygame.draw.rect(display, (255,255,0), ((col*(square_space), row*(square_space)), (CELL_SIZE, CELL_SIZE)))
    elif state == '0':
        pygame.draw.rect(display, (0,0,0), ((col*(square_space), row*(square_space)), (CELL_SIZE, CELL_SIZE)))
    else:
        pygame.draw.rect(display, (0,0,255), ((col*(square_space), row*(square_space)), (CELL_SIZE, CELL_SIZE)))
    pygame.display.update()

def draw(board, display, square_space, CELL_SIZE):
    startTime = time.time()
    if board.state == []:
        for col in range(board.col):
            for row in range(board.row):
                pygame.draw.rect(display, (0,0,0), ((col*(square_space), row*(square_space)), (CELL_SIZE, CELL_SIZE)))
    else:
        for col in range(board.col):
            for row in range(board.row):
                cell = (col, row)
                if board.getCellState(cell) == '1':
                    pygame.draw.rect(display, (255,255,0), ((col*(square_space), row*(square_space)), (CELL_SIZE, CELL_SIZE)))
                elif board.getCellState(cell) == '0':
                    pygame.draw.rect(display, (0,0,0), ((col*(square_space), row*(square_space)), (CELL_SIZE, CELL_SIZE)))
                else:
                    pygame.draw.rect(display, (0,0,255), ((col*(square_space), row*(square_space)), (CELL_SIZE, CELL_SIZE)))

    pygame.display.update()
    endTime = time.time()

def fromLocationToGrid(pos, square_space):
    x = pos[0]
    y = pos[1]
    grid = (math.floor(x/(square_space)),math.floor(y/(square_space)))

    return grid

if __name__ == "__main__":
    config = dict(board_conf.__dict__)
    pygame.init()
    main(config)
