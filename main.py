import curses
import random

# initializing curses
stdscr = curses.initscr()

# Configuration
curses.noecho() # Run noecho() to turn off automatic echoing of keys to the screen
curses.cbreak() # Enable cbreak mode
stdscr.keypad(True) # Enable keypad mode
stdscr.nodelay(True
               )
# Get maximum values of the screen columns and rows
maxl = curses.LINES - 1
maxc = curses.COLS - 1

# Initializing a matrix representing screen space
world = []
player_l = player_c = 0

def init() -> None:
    """"""
    global player_l, player_c
    for i in range(-1, maxl+1):
        world.append([])
        for j in range(-1, maxc+1):
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

def in_range(a: int, min: int, max: int) -> int:
    """"""
    if a > max:
        return max
    elif a < min:
        return min
    return a

def obstacle(x: int, y: int) -> bool:
    """Check if there is an obstacle in the given coordinates."""
    global world
    return world[x][y] == '.'

def move(char: str) -> None:
    """Get one of the 'asdw' keys and move toward the corresponding direction."""
    global player_l, player_c
    match char:
        case 'w':
            if not obstacle(player_l-1, player_c):
                player_l -= 1
        case 's':
            if not obstacle(player_l+1, player_c):
                player_l += 1
        case 'a':
            if not obstacle(player_l, player_c-1):
                player_c -= 1
        case 'd':
            if not obstacle(player_l, player_c+1):
                player_c += 1

    # Prevent from escaping the area
    player_l = in_range(player_l, 0, maxl - 1)
    player_c = in_range(player_c, 0, maxc - 1)

# Starting the game
init()

playing = True
while playing:
    try:
        c = stdscr.getkey()
    except:
        c = ''
    if c in 'asdw':
        move(c)
    elif c == 'q':
        playing = False
    draw()

# Clear the screen
stdscr.clear()
stdscr.refresh()
