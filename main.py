# uses MSS and keyboard
from grid import Grid
from algoritm import move, first_move, reset_game
from time import sleep

import mss.tools
from PIL import Image
import keyboard
import colorama
import pyautogui
import cv2

def screen(top, left, w, h):
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"top": top, "left": left, "width": w, "height": h}
        output = "result.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        return img

# beginner 10x10
# intermediet 16x16

def locate_blocks():
    # find all tiles
    cells = list(pyautogui.locateAllOnScreen('blocks/nblock.png', confidence=0.99))
    coordinates = []

    if len(cells) == 0:
        print("No board found!")
        return None
    
    column_count = 0
    top_comparetor = cells[0].top

    # for each tile
    for c in cells:
        # calculate and store center of tile and corner
        x, y = c.left + c.width // 2, c.top + c.height // 2
        middle = (x, y)
        #corner = (c.left, c.top)

        #coordinates.append((middle, corner))
        coordinates.append(middle)

        # meanwhile check for columns, will be used to automatically
        # calculate dimension of board
        if (top_comparetor == c.top):
            column_count += 1

    row_count = len(cells) // column_count
    print("Tiles detected:", len(cells))
    print("Dimension of board:", row_count, "x", column_count)

    # get final corners of screen
    # top-left corner the easiest
    top = cells[0].top
    left = cells[0].left
    # the width and height needs some calculations
    # take the last tile, the right-bottom corner, calculate outmost edge point
    # then calculate whole width and height, they represent "area"
    last = cells[len(cells) - 1]
    h = (last.top + last.height) - top
    w = (last.left + last.width) - left
    
    field = (int(top), int(left), int(w), int(h))

    return coordinates, (row_count, column_count), field


def main() -> None:
    colorama.init()

    coordinates, dimension, field_size = locate_blocks()
    row_count, column_count = dimension
    top, left, w, h = field_size

    s = pyautogui.locateOnScreen('blocks/smiley.png', confidence=0.99)
    s_pos = (s.left + s.width // 2, s.top + s.height // 2)

    # top corner of game
    #keyboard.wait('c')
    #left, top = pyautogui.position()
    #print(type(top), type(left))

    # bottom corner of game
    #keyboard.wait('c')
    #bot_pos = pyautogui.position()

    # w, h = bot_pos[0] - left, bot_pos[1] - top
    #test(top, left)

    # TODO: make more dynamic?
    cell_w, cell_h  = 30, 30 #w // row_count, h // column_count
    print(cell_w, cell_h)

    stopAI = False

    # define board
    while stopAI is False:
        grid = Grid(row_count, column_count, (cell_w, cell_h), coordinates)

        # first round:
        # TODO: check if we still need + 1 offset?
        img = screen(top, left + 1, w - 1, h)
        grid.update(img)

        sleep(1)
        first_move(grid)

        game = True

        # begin game
        while game is True:
            # take screenshot
            img = screen(top, left, w, h)

            # update 
            grid.update(img)

            # check if player wants to quit
            if pyautogui.position() <= (800, 600):
                game = False
                stopAI = True

            # check for game over
            if grid.clicked_on_mine is True:
                print("clicked on mine, game over")
                sleep(1)
                reset_game(s_pos)
                break

            if move(grid) is False:
                print("won, continue")
                sleep(0.5)
                reset_game(s_pos)
                break

            sleep(0.1)

main()
#pyautogui.click(800, 600, button='left')