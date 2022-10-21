import pygame
import math

from config import board_conf 
from board import *

def main(config):
    print(config)
    if config["BOARD_ROW_COUNT"] > config["MAX_BOARD_SIZE"] or config["BOARD_COLUMN_COUNT"] > config["MAX_BOARD_SIZE"]:
        print(f"Board dimensions must be within {config['MAX_BOARD_SIZE']}x{config['MAX_BOARD_SIZE']}")

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
    gameDisplay.fill((255, 255, 255))
    pygame.display.set_caption("Gamolyf")

    # For each cell, draw a rectangle
    for row in board.state:
        for cell in row:
            coordinates = cell.get_coordinates()
            col, row = coordinates[0], coordinates[1]
            pygame.draw.rect(gameDisplay, (0, 0, 0), ((col * square_space, row * square_space), (CELL_SIZE, CELL_SIZE)))

    pygame.display.update()
    gameExit = False
    isPlay = False
    is_heat_map = False

    while not gameExit:
        toggle_draw = False
        game_ticker = False
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
                    board.set_next_generation()
                    draw(board, gameDisplay, square_space, CELL_SIZE)
                    time.sleep(sleep_time)
            else:
                if pygame.mouse.get_pressed() == (1,0,0):

                    # ENTERING DRAW STATE
                    if (event.type == pygame.MOUSEMOTION):
                        pos = pygame.mouse.get_pos()
                        pos = fromLocationToGrid(pos, square_space)
                        board.get_cell(pos).set_is_alive(new_is_alive=True)
                        drawCell(board, gameDisplay, pos, square_space, CELL_SIZE)
                if event.type == pygame.KEYDOWN:

                    # Manual board iteration
                    if event.key == pygame.key.key_code("return"):
                        if not is_initial_state_saved and is_save_mode:
                            # COPY THE EXISTING STATE
                            board.export_board_state()
                            
                        print("Iterate board")

                        #Start event key is RETURN
                        board.set_next_generation()
                        draw(board, gameDisplay, square_space, CELL_SIZE)

                    # Start auto-run board setting 
                    if event.key == pygame.key.key_code("p"):
                        if not is_initial_state_saved and is_save_mode:
                            # Save initial board state
                            board.export_board_state()

                        print("Toggle isPlay:", isPlay)

                        pygame.event.clear()
                        pygame.event.set_allowed(pygame.KEYDOWN)
                        isPlay = True

                    #draw as heatmap
                    if event.key == pygame.key.key_code("x"):
                        # This section will toggle the heat_map view
                        is_heat_map = not is_heat_map
                        draw(board, gameDisplay, square_space, CELL_SIZE)
                        heat_map = board.heatmap.set_as_colour_map()
                        if is_heat_map:
                            draw_heat_map(heat_map, gameDisplay, square_space, CELL_SIZE)
                        else:
                            draw(board, gameDisplay, square_space, CELL_SIZE)


def drawCell(board, display, cell_coordinates, square_space, CELL_SIZE):
    col, row = cell_coordinates[0], cell_coordinates[1]
    cell = board.get_cell(cell_coordinates)
    
    if cell.get_is_alive():
        pygame.draw.rect(display, (255,255,0), ((col*(square_space), row*(square_space)), (CELL_SIZE, CELL_SIZE)))
    else:
        pygame.draw.rect(display, (0,0,0), ((col*(square_space), row*(square_space)), (CELL_SIZE, CELL_SIZE)))
    pygame.display.update()


def draw(board, display, square_space, CELL_SIZE):
    startTime = time.time()
    for row in board.state:
        for cell in row:
            coordinates = cell.get_coordinates()
            col, row = coordinates[0], coordinates[1]
            if cell.get_is_alive():
                pygame.draw.rect(display, (255, 255, 0), ((col * (square_space), row * (square_space)), (CELL_SIZE, CELL_SIZE)))
            else:
                pygame.draw.rect(display, (0, 0, 0), ((col * (square_space), row * (square_space)), (CELL_SIZE, CELL_SIZE)))

    pygame.display.update()
    endTime = time.time()


def fromLocationToGrid(pos, square_space):
    x = pos[0]
    y = pos[1]
    grid = (math.floor(x/(square_space)),math.floor(y/(square_space)))

    return grid

def draw_heat_map(colour_map, display, square_space, CELL_SIZE):
    startTime = time.time()
    for y, row in enumerate(colour_map.state):
        for x, cell_rgb in enumerate(row):
            coordinates = (y, x)
            x, y = coordinates[1], coordinates[0]
            pygame.draw.rect(display, cell_rgb, ((x * (square_space), y * (square_space)), (CELL_SIZE, CELL_SIZE)))

    pygame.display.update()
    endTime = time.time()


if __name__ == "__main__":
    config = dict(board_conf.__dict__)
    pygame.init()
    main(config)
