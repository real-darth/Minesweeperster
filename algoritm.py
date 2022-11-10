from cell import Cell
from grid import Grid

import random

import pyautogui

def first_move(grid: Grid):
    # TODO: Change to right corner for better win rate!
    x, y = grid.rows // 2, grid.columns // 2
    cell = grid.get_cell((x, y))
    click(cell)

def move(grid: Grid):
    performed_move = False
    random_tiles = []

    for row in grid.get_matrix():
        for cell in row:
            # BASE LOGIC 1: The easiest options
            if cell.clicked is False and cell.mines_around == -1 and cell.flagged is False:
                random_tiles.append(cell)
                continue

            mine_count = cell.mines_around
            unclicked = cell.get_unclicked_in_neighbors()
            flagged = cell.get_flagged_in_neighbors()

            # check if we have flagged all mines around us
            # if we have, we can safley open the rest!
            if mine_count == flagged:
                if reveal_neighbors(cell):
                    performed_move = True

            # if the unclicked count equals the mine count
            # all unclicked tiles are mines! Flag them all
            if mine_count == unclicked:
                if flag_neighbors(cell):
                    performed_move = True

    print(len(random_tiles))

    # LAST RESORT LOGIC: random tile 
    if performed_move == False and len(random_tiles) > 0:

        rand_cell = random.choice(random_tiles)
        if rand_cell:
            if random_click(rand_cell):
                performed_move = True

    return performed_move

def flag_neighbors(cell: Cell):
    action = False
    for neighbor in cell.neighbors:
        if neighbor.untouched():
            neighbor.flagged = True
            click(neighbor, True)
            action = True
    return action

def reveal_neighbors(cell: Cell):
    action = False
    for neighbor in cell.neighbors:
        if neighbor.untouched():
            neighbor.clicked = True
            click(neighbor)
            action = True
    return action

def random_click(cell: Cell):
    cell.clicked = True
    click(cell)
    return True

    
def click(cell: Cell, flag = False):
    #x, y = cell.get_cell_coordinates()
    #y, x = x + SCREEN_X, y + SCREEN_Y

    x, y = cell.middle_coordinate
    pyautogui.click(x, y, button='right' if flag else 'left')

def reset_game(reset_position):
    x, y = reset_position
    pyautogui.click(x, y, button='left')