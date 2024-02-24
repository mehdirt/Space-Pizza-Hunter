import curses
import random
from typing import Tuple

# TODO: Remove hardcodes
# initializing curses
stdscr = curses.initscr()

# Configuration
curses.noecho() # Run noecho() to turn off automatic echoing of keys to the screen
curses.cbreak() # Enable cbreak mode
stdscr.keypad(True) # Enable keypad mode
stdscr.nodelay(True) # Program won't wait for user to press any key

# Get maximum values of the screen columns and rows
maxl = curses.LINES - 1
maxc = curses.COLS - 1

# Initializing game variables
world = []
food = []
player_l = player_c = 0
score = 0

def random_place() -> Tuple[int, int]:
    """Returns a random place on screen which is already empty."""
    a = random.randint(0, maxl)
    b = random.randint(0, maxc)
    while world[a][b] != ' ':
        a = random.randint(0, maxl)
        b = random.randint(0, maxc)

    return a, b

def init() -> None:
    """"""
    global player_l, player_c
    # Initializing the world with obstacles and empty spaces
    for i in range(-1, maxl+1):
        world.append([])
        for j in range(-1, maxc+1):
            world[i].append(' ' if random.random() > 0.03 else '.')
    
    # Initializing foods coordinates
    for i in range(10):
        fl, fc = random_place() # Food cordinates
        fa = random.randint(1000, 10000) # Food age
        food.append((fl, fc, fa))
    # Initializing player coordinate        
    player_l, player_c = random_place()



def draw() -> None:
    """"""
    # Drawing the world wiht its obstacles and empty spaces
    for i in range(maxl):
        for j in range(maxc):
            stdscr.addch(i, j, world[i][j])
    stdscr.addstr(1, 1, f"Score: {score}")
    # Drawing the foods
    for f in food:
        fl, fc, fa = f
        stdscr.addch(fl, fc, '*')

    # Drawing the player
    stdscr.addch(player_l, player_c, 'X')
    stdscr.refresh()

def in_range(a: int, min: int, max: int) -> int:
    """Prevent user from crossing the borders."""
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

def cheack_food() -> None:
    """Check if player reached any food. Generate new food on screen if it was true."""
    global score
    for i in range(len(food)):
        fl, fc, fa = food[i]
        if fl == player_l and fc == player_c:
            score += 10
            # Making new food on the world
            nfl, nfc = random_place()
            nfa = random.randint(1000, 10000)
            food[i] = (nfl, nfc, nfa)

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
    cheack_food()
    draw()

# Clear the screen
stdscr.clear()
stdscr.refresh()
