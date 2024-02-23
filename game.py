#######################################################################
# "In Pursuit of Happiness"                                           #
# Never be disappointed in your life. Keep going. No matter what.     #
# Always avoid negative people (evils in this case).                  #
# Always have a smile on your beautiful face.                         #
# Take care.                                                          #
# :)                                                                  #
#######################################################################


# Import modules
from playsound import playsound
import curses
import random
import time
import os



# Initialize the curses
stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()
curses.noecho()
curses.cbreak()
curses.curs_set(False)
stdscr.keypad(True)
stdscr.nodelay(True)

# Determine the size of the screen
max_lines = curses.LINES - 1
max_columns = curses.COLS - 1

# Defining variables, addressing sound files and also other similar stuff is gonna be here
world = []
happinesses = []
evils = []
ponds = []
player_character = "X"
happiness_character = "H"
evil_character = "E"
pond_character = "W"
beep_sound = os.path.join('sound', 'soft_beep.wav')
gameover_sound = os.path.join('sound', 'gameover.wav')
happiness_meter = 0
player_x = 0
player_y = 0

# Functions
def set_coordinates():
    """
    Specify random coordinates that is not taken by an obstacle.
    """
    x = random.randint(0, max_lines)
    y = random.randint(0, max_columns)

    while world[x][y] != ' ':
        x = random.randint(0, max_lines)
        y = random.randint(0, max_columns)
    
    return x, y

def init():
    """
    Initialize the world.
    Add dots to the world based on each place's coordinates.
    """
    global player_x, player_y

    # Initialize the world
    for i in range(max_lines + 1):
        world.append([])
        for j in range(max_columns + 1):
            world[i].append(' ' if random.random() > 0.05 else '.')
    
    # Initialize a happiness
    for i in range(15):
        happiness_x, happiness_y = set_coordinates()
        happinesses.append((happiness_x, happiness_y))
    
    # Initialize evils
    for i in range(8):
        evil_x, evil_y = set_coordinates()
        evils.append((evil_x, evil_y))
    
    # Initialize ponds
    for i in range(22):
        pond_x, pond_y = set_coordinates()
        ponds.append((pond_x, pond_y))
   
    # Set random coordinates to the player in the world
    player_x, player_y = set_coordinates()

def draw():
    """
    Draw the world.
    """
    # Draw the initialized world
    for i in range(max_lines):
        for j in range(max_columns):
            stdscr.addch(i, j, world[i][j])
    
    # Show happiness meter
    stdscr.addstr(1, 1, f"Happiness Meter: {happiness_meter}", curses.A_BOLD)

    # Draw the initialized happinesses
    for h in happinesses:
        happiness_x, happiness_y = h
        stdscr.addch(happiness_x, happiness_y, happiness_character, curses.color_pair(3))
    
    # Draw the initialized evils
    for e in evils:
        evil_x, evil_y = e
        stdscr.addch(evil_x, evil_y, evil_character, curses.color_pair(2))
    
    # Draw the initialized ponds
    for p in ponds:
        pond_x, pond_y = p
        stdscr.addch(pond_x, pond_y, pond_character, curses.color_pair(5))
        # A pond should not be on an obstacle or a happiness
        while world[pond_x][pond_y] == '.' and happinesses[(pond_x, pond_y)] == (pond_x, pond_y):
            stdscr.addch(pond_x, pond_y, pond_character, curses.color_pair(5))

    # Create a player in the world with given coordinates
    stdscr.addch(player_x, player_y, player_character, curses.color_pair(4))
    stdscr.refresh()

def border(n, minimum, maximum):
    """
    When player is moving around, it shouldn't cross the sides of the screen.
    Otherwise the game will crash.
    """
    if n > maximum:
        return maximum
    if n < minimum:
        return minimum
    return n

def drowning(x, y):
    """
    If the player steps into a pond, then the player drowns to death!
    """
    global playing
    
    for p in ponds:
        pond_x, pond_y = p
        if x == pond_x and y == pond_y:
            stdscr.addstr(max_lines//2, max_columns//2 - 4, "YOU DROWNED!", curses.color_pair(5))
            stdscr.refresh()
            playsound(gameover_sound)
            time.sleep(2)
            playing = False
        else:
            pass

def move_player(character):
    """
    You know ADWS keys right? They make the player move in games :)
    When player is moving around, it shouldn't move over the obstacles.
    """
    global player_x, player_y
    
    # The player should not be able to get pass the obstacles and ponds
    if character == 'w' and world[player_x - 1][player_y] != '.':
        player_x -= 1
        drowning(player_x, player_y)
    elif character == 's' and world[player_x + 1][player_y] != '.':
        player_x += 1
        drowning(player_x, player_y)
    elif character == 'a' and world[player_x][player_y - 1] != '.':
        player_y -= 1
        drowning(player_x, player_y)
    elif character == 'd' and world[player_x][player_y + 1] != '.':
        player_y += 1
        drowning(player_x, player_y)

    player_x = border(player_x, 0, max_lines - 1)
    player_y = border(player_y, 0, max_columns - 1)

def move_evils():
    """
    Evils are all around the world and they can be ANYWHERE.
    You ask why?.... Because they MOVE.
    """
    global playing
    
    # Evils can move around. They smell people like you that want happiness in their life.
    # The question is: Will you be able to avoid them?
    # Remember that evils should not be able to get pass the obstacles.
    for i in range(len(evils)):
        evil_x, evil_y = evils[i]
        if random.random() > 0.95:
            if evil_x > player_x and world[evil_x - 1][evil_y] != '.':
                evil_x -= 1
        if random.random() > 0.95:
            if evil_x < player_x and world[evil_x + 1][evil_y] != '.':
                evil_x += 1
        if random.random() > 0.95:
            if evil_y > player_y and world[evil_x][evil_y - 1] != '.':
                evil_y -= 1
        if random.random() > 0.95:
            if evil_y < player_y and world[evil_x][evil_y + 1] != '.':
                evil_y += 1
            evil_x = border(evil_x, 0, max_lines - 1)
            evil_y = border(evil_y, 0, max_columns - 1)
            evils[i] = (evil_x, evil_y)
        # If you contact with an evil, you will DIE
        if evil_x == player_x and evil_y == player_y:
            stdscr.addstr(max_lines//2, max_columns//2 - 4, "YOU DIED!", curses.color_pair(2))
            stdscr.refresh()
            playsound(gameover_sound)
            time.sleep(3)
            playing = False


def how_is_life():
    """
    So the player achieved a happiness. What now?...
    Of course the player will be happy :)
    Each time the player achieves a happiness, these changes will happen in the player's life:
        - Happiness meter will increase.
        - A new happiness will be created.
    And the player will be in pursuit of happiness forever...
    """
    global happiness_meter

    # If the player achieves a happiness, increase the happiness meter.
    # Then create a new happiness.
    for i in range(len(happinesses)):
        happiness_x, happiness_y = happinesses[i]
        if happiness_x == player_x and happiness_y == player_y:
            happiness_meter += 5
            if happiness_meter % 100 == 0:
                playsound(beep_sound)
            new_happiness_x, new_happiness_y = set_coordinates()
            happinesses[i] = (new_happiness_x, new_happiness_y)

def main():
    for i in range(0, curses.COLORS):
        curses.init_pair(i+1, i, curses.COLOR_BLACK)
    
    init()
    
    global playing, player_x, player_y
    
    playing = True
    while playing:
        try:
            c = stdscr.getkey()
        except:
            c = ''
        if c in 'adws':
            move_player(c)
        elif c == 'q':
            playing = False
        how_is_life()
        move_evils()
        time.sleep(0.01)
        draw()

main()

stdscr.addstr(max_lines//2, max_columns//2 - 9, "THANKS FOR PLAYING!", curses.color_pair(3))
stdscr.refresh()
stdscr.addstr(max_lines//2 + 1, max_columns//2 - 7, "ALWAYS BE HAPPY", curses.color_pair(3))
stdscr.refresh()
time.sleep(3)
stdscr.clear()
stdscr.refresh()
