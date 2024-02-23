import curses
import random

# initializing curses
stdscr = curses.initscr()

# Configuration
curses.noecho() # Run noecho() to turn off automatic echoing of keys to the screen
curses.cbreak() # Enable cbreak mode
stdscr.keypad(True) # Enable keypad mode

# Get maximum values of the screen columns and rows
maxl = curses.LINES - 1
maxc = curses.COLS - 1

# Initializing a matrix representing screen space
world = []
player_l = player_c = 0

def init() -> None:
    """"""
    global player_l, player_c
    for i in range(maxl):
        world.append([])
        for j in range(maxc):
            world[i].append(' ' if random.random() > 0.03 else '.')
    player_l = random.randint(0, maxl)
    player_c = random.randint(0, maxc)


def draw() -> None:
    """"""
    for i in range(maxl):
        for j in range(maxc):
            stdscr.addch(i, j, world[i][j])
    
    stdscr.addch(player_l, player_c, 'X')
    stdscr.refresh()

# Create a world
init()
draw()

stdscr.refresh()
stdscr.getkey()