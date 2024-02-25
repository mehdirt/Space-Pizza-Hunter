import curses
import random
import time
from typing import Tuple

# TODO: Remove hardcodes

testing = True
food_age = 500
food_number = 10

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

# Game variables
world = []
foods = []
enemies = []
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

def init() -> None: # TODO: Convert the snippet codes here to functions + Handle their Hardcodings
    """Initialize game's variables."""

    global player_l, player_c
    # Initializing the world with obstacles and empty spaces
    for i in range(-1, maxl+1):
        world.append([])
        for j in range(-1, maxc+1):
            world[i].append(' ' if random.random() > 0.03 else '.')
    
    # Initializing foods coordinates
    for i in range(food_number):
        fl, fc = random_place() # Food cordinates
        fa = random.randint(food_age, food_age * 5) # Food age
        foods.append((fl, fc, fa))
    
    # Initializing enemies coordinates
    for i in range(3):
        el, ec = random_place()
        enemies.append((el, ec))

    # Initializing player coordinate        
    player_l, player_c = random_place()



def draw() -> None:
    """Draw game's features."""

    # Drawing the world with its obstacles and empty spaces
    for i in range(maxl):
        for j in range(maxc):
            stdscr.addch(i, j, world[i][j])
    stdscr.addstr(1, 1, f"Score: {score}")
    # Drawing the foods
    for food in foods:
        fl, fc, fa = food
        stdscr.addch(fl, fc, '*')

    # Drawing enemies
    for enemy in enemies:
        el, ec = enemy
        stdscr.addch(el, ec, 'E')

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

def get_close(enemy_x, enemy_y, player_x, player_y):
    """"""
    if enemy_x > player_l:
        enemy_x -= 1
    elif enemy_x < player_l:
        enemy_x += 1

    if enemy_y > player_c:
        enemy_y -= 1
    elif enemy_y < player_c:
        enemy_y += 1  

    return enemy_x, enemy_y

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

def check_food() -> None:
    """Check if player reached any food. Generate new food on screen if it was true."""
    global score
    for i in range(len(foods)):
        fl, fc, fa = foods[i]
        # Food spoiling (Age reduction)
        fa -= 10
        # Check if player catched a food
        if fl == player_l and fc == player_c:
            score += 10
            # Making new food on the world
            fl, fc = random_place()
            fa = random.randint(food_age, food_age * 5)
        if fa <= 0:
            fl, fc = random_place()
            fa = random.randint(food_age, food_age * 5)
        
        foods[i] = (fl, fc, fa)
    

def move_enemy():
    """Move enemies on the screen."""
    global playing
    for i in range(len(enemies)):
        el, ec = enemies[i]
        if random.random() > 0.9:
            el, ec = get_close(el, ec, player_l, player_c)
            # el += random.choice([0, 1, -1])
            # ec += random.choice([0, 1, -1])
            el = in_range(el, 0, maxl - 1)
            ec = in_range(ec, 0, maxc - 1)
            enemies[i] = (el, ec)
        time.sleep(0.02)

        if el == player_l and ec == player_c and not testing:
            stdscr.addstr(maxl//2, maxc//2, "YOU DIED!")
            stdscr.refresh()
            time.sleep(3)
            playing = False
    

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
    check_food()
    move_enemy()
    draw()

# Quiting the game
stdscr.addstr(maxl//2, maxc//2, "Thanks for Playing!")
stdscr.refresh()
time.sleep(2)

stdscr.clear()
stdscr.refresh()
