
from xmlrpc.client import Boolean


class Cell:
    def __init__(self, x: int, y: int, cell_scale: tuple) -> None:
        # Cell position and scale
        self.x, self.y = x, y
        self.cell_scale = cell_scale

        # Cell attributes
        self.mines_around = -1
        self.flagged = False
        self.clicked = False

    def set_neighbors(self, neighbors: list) -> None:
        """
        Set cell's neighbors

        :param neighbors: type{list}, neighbor list created from grid
        """
        self.neighbors = neighbors

    def set_middle_coordinate(self, coordinate):
        self.middle_coordinate = coordinate

    #def set_corner_coordinate(self, coordinate):
    #    self.corner_coordinate = coordinate

    def get_flagged_in_neighbors(self) -> int:
        """
        Find the amount of mines in neighbors, return zero by default.

        :return: amount type{int}, the amount of mines in neighbors
        """
        amount = 0
        for cells in self.neighbors:
            if cells.flagged is True:
                amount += 1

        return amount

    def get_unclicked_in_neighbors(self) -> int:
        amount = 0
        for cells in self.neighbors:
            if cells.clicked is False:
                amount += 1

        return amount

    def get_cell_coordinates(self) -> tuple:
        pixel_pos = [self.cell_scale[0] * self.x, self.cell_scale[1] * self.y]

        # return position in the middle of the box
        x, y = round(pixel_pos[0] + self.cell_scale[0] / 2), round(pixel_pos[1] + self.cell_scale[1] / 2 + 2)
        return (x, y)

    def untouched(self) -> bool:
        return self.flagged is False and self.clicked is False
