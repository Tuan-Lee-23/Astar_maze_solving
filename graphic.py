import pygame
import sys
import threading
import time
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
MARGIN = 5

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(10):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(10):
        grid[row].append(0)  # Append a cell

# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
grid[1][5] = 1

# Initialize pygame

# Loop until the user clicks the close button.
done = False


def read_input_file(dir: str):
    try:
        with open(dir, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if i == 1:
                    # line = line.split(' ')
                    line = line.replace("(", "").replace(")", "").replace(", ", ",").replace("\n","")
                    line = line.split("  ")
                    print(line)
                    pathList = []
                    for item in line:
                        if item is not '':
                            pathList.append([item.split(",")[0], item.split(",")[1]])

                    print(pathList)
                    return line


            return []
    except FileNotFoundError:
        print("File not found:", dir, "\nplease fix your directory")
        sys.exit(1)



# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# output_file = '/Users/macintoshhd/HOCDIIIII/AIProject1/res.txt'  # arguments[2]
#
# input_data = read_input_file(output_file)
#
# # Get maze and start, goal position
# maze = input_data[0]
# start = input_data[1]
# -------- Main Program Loop -----------
array = []
map = []
index = 0
drawArray = []
optimalPath = []
isOptimal = False
optimalPathForDraw = []
openPath = []
start = []
goal = []
speed = 0.15
def addStart(point):
    global start
    start = point
def addGoal(point):
    global goal
    goal = point
def addMap(arr):
    global map
    map = arr
    print("did add map")
    print(map)

def drawPath(array1):
    array = array1
    index = 0
    def drawL():
        global index
        global isOptimal
        global drawArray
        global optimalPathForDraw
        global speed
        for i in range(len(array)):
            if index <= len(array):
                if isOptimal == True:
                    optimalPathForDraw.append(array[index])
                else:
                    drawArray.append(array[index])
                index = index + 1
                time.sleep(speed)
        if index == len(array) and isOptimal != True:
            index = 0
            isOptimal = True
            drawPath(optimalPath)
            return

    # for i in range(10):
    t = threading.Thread(target=drawL)
    # threads.append(t)
    t.start()

def addOptimalPath(path):
    global optimalPath
    optimalPath = path
def addOpenPath(path):
    global openPath
    openPath = path
dd = 1
def main():
    global dd
    global isOptimal
    global openPath
    global speed
    done = False
    pygame.init()

    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [len(map[0]) * 20 + (len(map[0]) + 1 ) * 5, len(map) * 20 + (len(map) + 1 ) * 5]
    speed = 1.0/len(map)
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Set title of screen
    pygame.display.set_caption("Array Backed Grid")

    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Set that location to one
                grid[row][column] = 1
                print("Click ", pos, "Grid coordinates: ", row, column)

        # Set the screen background
        screen.fill(BLACK)
        if dd == 1:
            print("didDraw")
            drawPath(openPath)
            dd = 0
        # Draw the grid
        for row in range(len(map)):
            for column in range(len(map[row])):
                if map[row][column] == 0:
                    color = WHITE
                else:
                    color = BLACK
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
        for item in drawArray:
            color = GREEN
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * item[1] + MARGIN,
                              (MARGIN + HEIGHT) * item[0] + MARGIN,
                              WIDTH,
                              HEIGHT])
        if isOptimal:
            for item in optimalPathForDraw:
                color = RED
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * item[1] + MARGIN,
                                  (MARGIN + HEIGHT) * item[0] + MARGIN,
                                  WIDTH,
                                  HEIGHT])
        pygame.draw.rect(screen,
                         BLUE,
                         [(MARGIN + WIDTH) * start[1] + MARGIN,
                          (MARGIN + HEIGHT) * start[0] + MARGIN,
                          WIDTH,
                          HEIGHT])
        pygame.draw.rect(screen,
                         YELLOW,
                         [(MARGIN + WIDTH) * goal[1] + MARGIN,
                          (MARGIN + HEIGHT) * goal[0] + MARGIN,
                          WIDTH,
                          HEIGHT])
        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

