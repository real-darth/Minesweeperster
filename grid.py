import numpy as np
from PIL import Image
from cell import Cell
#import colorama
from colorama import Fore, Style, Back


class Grid:
    def __init__(self, width: int, height: int, cell_scale: tuple, coordinates: tuple) -> None:
        # assing board scale
        self.rows, self.columns = width, height
        self.cell_scale = cell_scale

        # Initialize board
        # Create the grid represented by a matrix
        self.matrix = self.create_matrix(coordinates)

        # Set all cells neighbors
        self.set_cell_neighbors()

        # set the matrix of colors
        self.colors = np.asarray([
            [189, 189, 189], # 0
            [0, 33, 245], # 1
            [53, 120, 32], # 2
            [246, 0, 17], # 3
            [5, 0, 123], # 4
            [123, 0, 4], # 5
            [255, 255, 255] # white, for the left region of unclicked piece
        ])

        # set termcolor dictionary
        self.colorWord = {
            '0' : Fore.LIGHTWHITE_EX,
            '1' : Fore.BLUE,
            '2' : Fore.GREEN,
            '3' : Fore.RED,
            '4' : Fore.BLUE,
            '5' : Fore.RED,
            '6' : Fore.MAGENTA,
            'F' : Fore.YELLOW,
            'X' : Fore.WHITE
        }

        self.clicked_on_mine = False
    
    def update(self, img):
        # load the image once
        #im = Image.open(img)
        px = img.load()
        #print(type(px))

        for r in range(self.rows):
            for c in range(self.columns):
                cell = self.get_cell((r, c))

                msg = None
                if cell.flagged:
                    msg = 'F'
                else:
                    msg = self.get_cell_data(px, r, c)
                    if msg != 'X':
                        cell.clicked = True
                        cell.mines_around = msg
                msg = str(msg)
                print(self.colorWord[msg] + msg, end=" ")
            print()
        print()

        path = r'C:\Users\Elliot Darth\Documents\GitHub\Minesweeper AI\bang.png'
        img.save(path)

    def get_cell_data(self, px, r, c):

        def get_number_from_color(color_pixel) -> int:
            # convert from tuple to array
            color_array = np.asarray(color_pixel)
            # get the difference of all colors, the closest color will be closer to zero
            diff = abs(self.colors - color_array)
            # sum the 3 RGB values
            diff_sum = diff.sum(axis=1)
            # return the index smallest difference, that is our key / number
            return np.argmin(diff_sum)
        
        pixel_pos = [self.cell_scale[0] * c, self.cell_scale[1] * r]

        # let's try just checking two pixels in total!!
        x, y = round(pixel_pos[0] + self.cell_scale[0] / 2), round(pixel_pos[1] + self.cell_scale[1] / 2 + 2)

        color_pixel_1 = px[x, y]
        if color_pixel_1 == (0, 0, 0):
            self.clicked_on_mine = True

        color_pixel_2 = px[pixel_pos[0] + self.cell_scale[0] / 2 , pixel_pos[1]  + self.cell_scale[1] / 2]

        test_1 = get_number_from_color(color_pixel_1)
        test_2 = get_number_from_color(color_pixel_2)

        # get the largest number
        result = max(test_1, test_2)

        #test = min(sum(self.colors), key=lambda x: sum(color_pixel))
        #test_sum = sum(testis)
        #num = self.number_dict[test_sum]
        
        # DEBUG COLORS
        px[x, y] = (255, 0, 0)
        px[pixel_pos[0] + self.cell_scale[0] / 2 , pixel_pos[1]  + self.cell_scale[1] / 2] = (0, 255, 0)

        # if number is zero, we check for unclicked (white)
        if result == 0:
            white_pixel_1 = px[x, pixel_pos[1] + 2]
            #white_pixel_2 = px[pixel_pos[0], y]

            # DEBUG COLOR
            px[x, pixel_pos[1]] = (0, 0, 0)
            #px[pixel_pos[0], y] = (0, 0, 0)

            # TODO: testa också bara jämföra direkt...
            if (np.asarray(white_pixel_1) == [255, 255, 255]).all():
                return 'X'

            #if (np.asarray(white_pixel_2) == [255, 255, 255]).all():
            #    return 'X'

        return result

    def create_matrix(self, cell_attributes) -> np.ndarray:
        """
        Creates a matrix filled with cells, representing the grid.

        :param width: type{int}, width of grid
        :param height: type{int}, height of grid
        :return: grid type{np.ndarray}, matrix filled with cells
        """
        # Generate empty grid
        grid = np.zeros((self.rows, self.columns), dtype=Cell)

        # Fill grid with cells, set relevant coordinates too
        index = 0
        for r in range(self.rows):
            for c in range(self.columns):
                grid[r][c] = Cell(r, c, self.cell_scale)
                grid[r][c].set_middle_coordinate(cell_attributes[index])
                #grid[r][c].set_corner_coordinate(cell_attributes[index][1])

                index += 1
        return grid

    def set_cell_neighbors(self) -> None:
        """Loop through matrix and sett each cells neighbors."""
        for c in range(self.columns):
            for r in range(self.rows):
                self.matrix[r][c].set_neighbors(self.get_neighbors_list(r, c))

    def get_neighbors_list(self, row: int, col: int) -> list:
        """
        Loop through a cell neighbors and assign them to a list.

        :param row: type{int}, the row number of cell (x-coordinate)
        :param col: type{int}, the column number of cell (y-coordinate)
        :return: neighbors type{list}, neighbors of a specified cell coordinate
        """
        neighbors = []

        """
        We need to construct a loop so we find the neighbors of a cell
        # = cell we are looking at
        x = neighbor

            X X X <- y-coordinate + 1 (+ 1 for range limit)
            X # X
            X X X <- y coordinate - 1

        the same is done with the x-axis
        """
        for c in range(col - 1, col + 2):
            for r in range(row - 1, row + 2):

                # skip coordinates outside of grid (too large or too small)
                if r < 0 or r >= self.rows or c < 0 or c >= self.columns:
                    continue

                # we do not want to add the cell as its own neighbor
                if r == row and c == col:
                    continue

                cell = self.get_cell((r, c))

                # failsafe check, do not add cells that are not found
                if cell is None:
                    continue

                # if none of the above checks are triggered, add cell to neighbors list
                neighbors.append(cell)

        return neighbors

    def get_cell(self, index: tuple[int, int]) -> Cell:
        """
        Return a cell from the given index, if index is not eligible return None.

        :param index: type{tuple(int, int)}, index in (x, y) for grid matrix
        :return: cell type{Cell}, Cell-object from grid
        """
        if (index[0] >= 0 and index[1] >= 0) and (index[0] < self.rows and index[1] < self.columns):
            cell = self.matrix[index[0]][index[1]]
            return cell
        else:
            return None

    def get_matrix(self):
        return self.matrix
