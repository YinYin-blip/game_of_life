import pygame
import time
import math

from board import *

CELL_SIZE = 10
CELL_SPACING = 1
pygame.init()

def main():
    col = 40
    row = 30
    board = Board(col, row)

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

    while not gameExit:
        gameTicker = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                grid = fromLocationToGrid(pos)
                newState = board.toggleCell(grid)
                print(newState)
                if newState == '1':
                    pygame.draw.rect(gameDisplay, (255,255,0), ((grid[0]*(CELL_SIZE+CELL_SPACING), grid[1]*(CELL_SIZE+CELL_SPACING)), (CELL_SIZE, CELL_SIZE)))
                    pygame.display.update()
                elif newState == '0':
                    pygame.draw.rect(gameDisplay, (0,0,0), ((grid[0]*(CELL_SIZE+CELL_SPACING), grid[1]*(CELL_SIZE+CELL_SPACING)), (CELL_SIZE, CELL_SIZE)))
                    pygame.display.update()

            if event.type == pygame.KEYDOWN and event.key == 276:
                board.setState(board.getNextGeneration())
                draw(board, gameDisplay)


def draw(board, display):
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

def fromLocationToGrid(pos):
    x = pos[0]
    y = pos[1]
    grid = (math.floor(x/(CELL_SIZE+CELL_SPACING)),math.floor(y/(CELL_SIZE+CELL_SPACING)))
    print(grid)

    return grid

if __name__ == "__main__":
    main()
