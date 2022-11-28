# uses MSS and keyboard
from grid import Grid
from algoritm import move, first_move, reset_game
from time import sleep
from ai_statistics import Stats

import mss.tools
from PIL import Image
import colorama
import pyautogui
import cv2

# for mac use size: 22

def screen(top, left, w, h):
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"top": top, "left": left, "width": w, "height": h}
        #monitor = {"top": 530, "left": 430, "width": 44, "height": 44}
        #monitor = {"top": 530//2, "left": 430//2, "width": 44//2, "height": 42 // 2}
        output = "result.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        return img

# beginner 10x10
# intermediet 16x16
MAC = True

def locate_blocks():
    if (MAC):
        divisor = 2
    else : 
        divisor = 1

    # find all tiles
    cells = list(pyautogui.locateAllOnScreen('blocks/block_mac.png', confidence=0.99))
    coordinates = []

    if len(cells) == 0:
        print("No board found!")
        return None
    
    column_count = 0
    top_comparetor = cells[0].top // divisor

    # for each tile
    for c in cells:
        #print(c)
        # calculate and store center of tile and corner
        x, y = c.left // divisor + (c.width // 2) // divisor, c.top // divisor + (c.height // 2) // divisor
        middle = (x, y)
        #corner = (c.left, c.top)

        #coordinates.append((middle, corner))
        coordinates.append(middle)

        # meanwhile check for columns, will be used to automatically
        # calculate dimension of board
        if (top_comparetor == c.top // divisor):
            column_count += 1

    print("Tiles detected:", len(cells))
    row_count = len(cells) // column_count
    print("Dimension of board:", row_count, "x", column_count)

    # get final corners of screen
    # top-left corner the easiest
    top = cells[0].top // divisor
    left = cells[0].left // divisor
    # the width and height needs some calculations
    # take the last tile, the right-bottom corner, calculate outmost edge point
    # then calculate whole width and height, they represent "area"
    last = cells[len(cells) - 1]
    h = (last.top // divisor + last.height // divisor) - top
    w = (last.left // divisor + last.width // divisor) - left
    
    field = (int(top), int(left), int(w), int(h))

    return coordinates, (row_count, column_count), field


def main() -> None:
    colorama.init()

    if (MAC):
        divisor = 2
    else : divisor =1

    # field and cells positions
    coordinates, dimension, field_size = locate_blocks()
    row_count, column_count = dimension
    top, left, w, h = field_size

    # smiley position
    s = pyautogui.locateOnScreen('blocks/smiley_mac.png', confidence=0.99)
    s_pos = s.left // divisor + ((s.width // 2) // divisor), s.top // divisor + ((s.height // 2) // divisor)

    # TODO: make more dynamic?
    #cell_w, cell_h  = 30, 30 #w // row_count, h // column_count
    cell_w, cell_h  = 44, 44 #w // row_count, h // column_count

    # track statistics
    stats = Stats()

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
            if pyautogui.position() <= (100 // (divisor * 1.5), 100 // (divisor * 1.5)):
                print("moved mouse to stop game")
                print(stats)
                game = False
                stopAI = True

            # check for game over
            if grid.clicked_on_mine is True:
                print("clicked on mine, game over")
                stats.increment_loss()
                sleep(1)
                reset_game(s_pos)
                print(stats)
                break

            if move(grid) is False:
                print("won, continue")
                stats.increment_win()
                sleep(0.5)
                reset_game(s_pos)
                print(stats)
                break

            sleep(0.1)

    # when program finnished, print winrate
    print(stats)
    

main()