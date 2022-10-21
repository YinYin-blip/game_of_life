import time
import os
import glob

# TODO: test that heatmap works by adding a way to render the heatmap on the frontend code
class Cell:
    # Cell has location and coordinates
    # Coordinates are private variables
    # Setting state can be done directly: cell.is_alive = not cell.is_alive
    # Function call for coordinates 

    def __init__(self, coordinates, CELL_SIZE, is_alive=False):
        self._cell_size = CELL_SIZE
        self._coordinates = coordinates
        self._is_alive = is_alive

    def __mul__(self, x):
        return [Cell((_, self._coordinates[1]), self._cell_size, is_alive=self._is_alive) for _ in range(x)]

    def set_is_alive(self, new_is_alive):
        self._is_alive = new_is_alive

    def get_is_alive(self):
        return self._is_alive

    def get_coordinates(self):
        return self._coordinates

    def get_board_surface_area(self):
        return tuple(self._cell_size*x for x in self._coordinates)


class Board:
    def __init__(self, config):
        self.col = config["BOARD_COLUMN_COUNT"] 
        self.row = config["BOARD_ROW_COUNT"]
        self._cell_size = config["CELL_SIZE"]
        self.save_dir = config["SAVE_DIR"]
        self.state = []
        self.heatmap = HeatMap(config)
        for _ in range(self.row):
            self.state.append(Cell((0, _), CELL_SIZE=self._cell_size)*self.col)

    def __str__(self):
        # Returns a string representation of state of the board
        delim = ','
        state = ''
        for row in self.state:
            for cell in row:
                if cell.get_is_alive():
                    state += "1"
                else:
                    state += "0"
            state += delim
        return state[:-1]

    #def import_heatmap_state(self, file_name):

    #def export_heatmap_state(self, delim=","):

    def import_board_state(self, file_name):
        # :param: FILE_NAME str - name of file that stores string representation of board state
        state = ''
        with open(file_name, "r") as f:
            for line in f:
                state += line
        state.replace("\n", ",")
        self.set_board_state(state)

    def export_board_state(self, delim=","):
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

        highest_index = len(files)+1
        new_file_name = self.save_dir + "b" + str(highest_index) + ".txt"

        with open(new_file_name, "w") as f:
            text = str(self).replace(",", "\n")
            f.write(text)

    def set_board_state(self, state):
        # :param: STATE str - list of string values to represent is_alive values.
        # STATE format: default delim
        assert(isinstance(state, str))
        state = state.split(",")
        for row in self.state:
            for cell in row:
                coordinates = cell.get_coordinates()
                row, col = coordinates[1], coordinates[0]

                if state[row][col] == '1':
                    cell.set_is_alive(True)
                else:
                    cell.set_is_alive(False)

    def toggle_cell(self, coordinates):
        cell = self.get_cell(coordinates)
        cell.set_is_alive(not cell.get_is_alive())

    def set_next_generation(self):
        start_time = time.time()
        temp_state = ''
        self.heatmap + self.state

        for row in self.state:
            for cell in row:
                temp_state += self.get_next_generation_cell_is_alive(current_cell=cell)
            temp_state += ","

        self.set_board_state(temp_state)
        end_time = time.time()
        return temp_state

    def get_next_generation_cell_is_alive(self, current_cell):
        # Return new is alive state
        '''
        For a space that is 'populated':
            (1) Each cell with one or no neighbors dies, as if by solitude.
            (2) Each cell with four or more neighbors dies, as if by overpopulation.
            (3) Each cell with two or three neighbors survives.
        For a space that is 'empty' or 'unpopulated'
            (4) Each cell with three neighbors becomes populated.
        '''
        neighbor_count = self.count_living_neighbors(current_cell)
        if current_cell.get_is_alive():
            if neighbor_count <= 1:
                return "0"
            elif neighbor_count >= 4:
                return "0"
            else:
                return "1"
        else:
            if neighbor_count == 3:
                return "1"
            else:
                return "0"

    def get_cell(self, coordinates):
        # Return cell object based on coordinates. Returns False for invalid coordinates
        if coordinates[0] < 0 or coordinates[0] > (self.col - 1):
            return False
        if coordinates[1] < 0 or coordinates[1] > (self.row - 1):
            return False

        x = coordinates[0]
        y = coordinates[1]
        return self.state[y][x]

    def count_living_neighbors(self, cell):
        # Check distance of 1 from given cell and count all cells where is_alive is True
        count = 0
        coordinates = cell.get_coordinates()

        for x_displacement in range(-1, 2, 1):
            for y_displacement in range(-1, 2, 1):
                neighbor_coordinates = (coordinates[0]+x_displacement, coordinates[1]+y_displacement)
                if neighbor_coordinates == coordinates:
                    continue
                cell = self.get_cell(neighbor_coordinates)
                if cell and cell.get_is_alive():
                    count += 1
        return count


class HeatMap():
    def __init__(self, config):
        self.row = config["BOARD_ROW_COUNT"]
        self.col = config["BOARD_COLUMN_COUNT"]
        self.state = [[0]*self.col for _ in range(self.row)]
        self.config = config

    def _generation_loader(self, new_generation):
        binary_matrix = []
        if isinstance(new_generation, str):
            generation = new_generation.split(",")
            for row in generation:
                row_matrix = []
                for cell in row:
                    if cell == "0":
                        row_matrix.append(0)
                    else:
                        row_matrix.append(1)

                if len(row_matrix) > 0:
                    binary_matrix.append(row_matrix)

        elif isinstance(new_generation, list):
            if isinstance(new_generation[0][0], Cell):
                for row in new_generation:
                    row_matrix = []
                    for cell in row:
                        if cell.get_is_alive():
                            row_matrix.append(1)
                        else:
                            row_matrix.append(0)

                    if len(row_matrix) > 0:
                        binary_matrix.append(row_matrix)
        assert len(binary_matrix) == self.row
        assert len(binary_matrix[0]) == self.col
        return binary_matrix

    def __str__(self):
        # Returns a string representation of state of the board
        delim = ','
        state = ''
        for row in self.state:
            for cell in row:
                state += f"({cell[0]},{cell[1]},{cell[2]})"
            state += delim
        return state[:-1]

    def __add__(self, new_generation):
        generation = self._generation_loader(new_generation)
        for y, row in enumerate(self.state):
            for x, cell in enumerate(row):
                #print(f"{(y, x)} {self.state[y][x]} {generation[y][x]}")
                self.state[y][x] += generation[y][x]

        self.set_as_colour_map()

    def min_max(self):
        low = min([min(row) for row in self.state])
        high = max([max(row) for row in self.state])
        return low, high

    def set_as_colour_map(self):
        mini_max = self.min_max()
        low, high = mini_max[0], mini_max[1]
        colour_map = HeatMap(self.config)
        for y in range(self.row):
            for x in range(self.col):
                ratio = 2 * (self.state[y][x] - low) / (high - low)
                b = int(max(0, 255 * (1 - ratio)))
                r = int(max(0, 255 * (ratio - 1)))
                g = 255 - b - r
                colour_map.state[y][x] = (r, g, b)

        return colour_map
