# Minesweeperster
 A simple Minesweeper AI I made cause I want to be lazy

<!-- Index Table -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About</a>
      <ul>
        <li><a href="libraries">Libraries</a></li>
      </ul>
    <li><a href="#how-to-use">How to use</a></li>
    <li><a href="#statistics">Statistics</a></li>
    <li><a href="#todo">TODO</a></li>
    
    <!-- <li><a href="#acknowledgements">Acknowledgements</a></li> -->
  </ol>
</details>

## About
> I got lazy playing minesweeper. This project is planned to be expanded..

This is a python-built AI that plays Minesweeper currently only on this [website](http://play-minesweeper.com/). It automatically finds the playing field __when size: 30__ and uses a simple algorithm to try and solve the board. It will start a new board everytime the game is over. 

### Libraries
- [numpy](https://numpy.readthedocs.io/en/latest/)
- [mss](https://python-mss.readthedocs.io/)
- [pyautogui](https://pyautogui.readthedocs.io/en/latest/)
- [pillow](https://pillow.readthedocs.io/en/stable/)
> optional:
* [colorama](https://super-devops.readthedocs.io/en/latest/misc.html)

## How to use
To use the AI, download the project and the required libraries. Open this [website](http://play-minesweeper.com/) and set size to 30. Afterwards, display the board on your screen and run the application in the background. The AI will find the board and start playing the game.

To stop the program, drag your mouse to the top-left corner of your screen. This will kill the instance, you may have to try some times since your mouse will likley be flicking across the screen.

## Statistics
> TODO: Display a general win-rate of the AI

## TODO
- [x] Usable on multiple board sizes.
- [ ] Try to fix for multiple screen sizes (can scale the board in pixels).
- [ ] mine count 6 and 7.
- [ ] Better error handling.
- [ ] Expanded algorithm to check for other conditions, such as tile-patterns.
- [ ] Better random-click algorithm, can calculate the different chances for a mine and select the best option.
- [ ] Statistics, win-loose-rate
