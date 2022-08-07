import pygame
import time
import math

from config import board_conf 
from board import *

def main(config):
    print(config)
    CELL_SIZE = config["CELL_SIZE"]
    CELL_SPACING = config["CELL_SPACING"]
    col = config["BOARD_COLUMN_COUNT"]
    row = config["BOARD_ROW_COUNT"]
    sleep_time = config["SLEEP_TIME"]

    board = Board(config)

    width = col*(CELL_SIZE+CELL_SPACING)
    height = row*(CELL_SIZE+CELL_SPACING)
    gameDisplay = pygame.display.set_mode((width,height))
    gameDisplay.fill((255,255,255))
    pygame.display.set_caption("Gamolyf")

    for col in range(board.col):
        for row in range(board.row):
            pygame.draw.rect(gameDisplay, (0,0,0), ((col*(CELL_SIZE+CELL_SPACING), row*(CELL_SIZE+CELL_SPACING)), (CELL_SIZE, CELL_SIZE)))
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
                # skip event iterate on generation
                while(isPlay):
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.key.key_code("space"):
                            print("toggle isPlay:", isPlay)

                            isPlay = False
                            pygame.event.clear()
                            pygame.event.set_allowed(None)
                            break
                    board.setState(board.getNextGeneration())
                    draw(board, gameDisplay, CELL_SIZE, CELL_SPACING)
                    time.sleep(sleep_time)
            else:
                if pygame.mouse.get_pressed() == (1,0,0):
                    # ENTERING DRAW STATE
                    if (event.type == pygame.MOUSEMOTION):
                        pos = pygame.mouse.get_pos()
                        pos = fromLocationToGrid(pos, CELL_SIZE, CELL_SPACING)
                        board.setCell(cell=pos, state='1')
                        drawCell(board, gameDisplay, pos, CELL_SIZE, CELL_SPACING)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.key.key_code("return"):
                        print("Iterate board")

                        #Start event key is RETURN
                        board.setState(board.getNextGeneration())
                        draw(board, gameDisplay, CELL_SIZE, CELL_SPACING)
                    if event.key == pygame.key.key_code("p"):
                        print("Toggle isPlay:", isPlay)

                        pygame.event.clear()
                        pygame.event.set_allowed(pygame.KEYDOWN)
                        isPlay = True

def drawCell(board, display, cell, CELL_SIZE, CELL_SPACING):
    col, row = cell[0], cell[1]
    state = board.getCellState(cell) 
    
    if state == '1':
        pygame.draw.rect(display, (255,255,0), ((col*(CELL_SIZE+CELL_SPACING), row*(CELL_SIZE+CELL_SPACING)), (CELL_SIZE, CELL_SIZE)))
    elif state == '0':
        pygame.draw.rect(display, (0,0,0), ((col*(CELL_SIZE+CELL_SPACING), row*(CELL_SIZE+CELL_SPACING)), (CELL_SIZE, CELL_SIZE)))
    else:
        pygame.draw.rect(display, (0,0,255), ((col*(CELL_SIZE+CELL_SPACING), row*(CELL_SIZE+CELL_SPACING)), (CELL_SIZE, CELL_SIZE)))
    pygame.display.update()

def draw(board, display, CELL_SIZE, CELL_SPACING):
    startTime = time.time()
    if board.state == []:
        for col in range(board.col):
            for row in range(board.row):
                pygame.draw.rect(display, (0,0,0), ((col*(CELL_SIZE+CELL_SPACING), row*(CELL_SIZE+CELL_SPACING)), (CELL_SIZE, CELL_SIZE)))
    else:
            
        for col in range(board.col):
            for row in range(board.row):
                cell = (col, row)
                if board.getCellState(cell) == '1':
                    pygame.draw.rect(display, (255,255,0), ((col*(CELL_SIZE+CELL_SPACING), row*(CELL_SIZE+CELL_SPACING)), (CELL_SIZE, CELL_SIZE)))
                elif board.getCellState(cell) == '0':
                    pygame.draw.rect(display, (0,0,0), ((col*(CELL_SIZE+CELL_SPACING), row*(CELL_SIZE+CELL_SPACING)), (CELL_SIZE, CELL_SIZE)))
                else:
                    pygame.draw.rect(display, (0,0,255), ((col*(CELL_SIZE+CELL_SPACING), row*(CELL_SIZE+CELL_SPACING)), (CELL_SIZE, CELL_SIZE)))

    pygame.display.update()
    endTime = time.time()

def fromLocationToGrid(pos, CELL_SIZE, CELL_SPACING):
    x = pos[0]
    y = pos[1]
    grid = (math.floor(x/(CELL_SIZE+CELL_SPACING)),math.floor(y/(CELL_SIZE+CELL_SPACING)))

    return grid

if __name__ == "__main__":
    config = dict(board_conf.__dict__)
    pygame.init()
    main(config)
