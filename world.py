import random
import os
import copy

# This "world" uses an X, Y coordinate system, with the origin in the uper left hand corner 

DEBUG = False

def generateWorld(w, h):
    # Initialize the array
    world = [[0 for x in range(w)] for y in range(h)]
    # random.seed(69)

    # Pick n spots (equal to 10% of total size) to place water and land starts
    # 5% for water, 5% for land
    numSpots = int((w * h) * 0.01);
    # numSpots = 1
    for i in range(numSpots):

        world = spawnNode(world, "w")
        world = spawnNode(world, "l")

    # Spawn a single desert tile
    # world = spawnNode(world, "s")

    # DEBUG -- Show the initial generation
    if DEBUG:
        displayWorld(world)
        print ""
        raw_input()

    xCoordinates = range(len(world[0]))
    yCoordinates = range(len(world))

    # Now, go through all the spots and expand the land and water, until all spots are filled
    numEmptySpots = 1

    # We generate the map by determining what the next stage will look like, so we need to make a second
    # map of the same size as our "master" map
    nextWorldStage = [[0 for y in range(w)] for x in range(h)]
    while numEmptySpots > 0:
        numEmptySpots = 0

        # shuffle the coordinates, giving a random priority for expansion 
        random.shuffle(xCoordinates)
        for x in xCoordinates:
            random.shuffle(yCoordinates)
            for y in yCoordinates:
                spotType = world[y][x]

                # Count the number of empty spots
                if notOccupied(spotType):
                    numEmptySpots += 1
                
                # Otherwise, expand the spot's type in the "cardinal" directions
                # No expanding pass the boundaries of the world
                else:
                    # If this is an occupied space, then we'll set that in the next iteration
                    nextWorldStage[y][x] = spotType
                    
                    # Along with setting the neighboring coordinates 
                    # North
                    if (y - 1) >= 0 and notOccupied(nextWorldStage[y - 1][x]):
                        nextWorldStage[y - 1][x] = spotType
                    
                    # East
                    if (x + 1) < w and notOccupied(nextWorldStage[y][x + 1]):
                        nextWorldStage[y][x + 1] = spotType
                    
                    # South
                    if (y + 1) < h and notOccupied(nextWorldStage[y + 1][x]):
                        nextWorldStage[y + 1][x] = spotType

                    # West
                    if (x - 1) >= 0 and notOccupied(nextWorldStage[y][x - 1]):
                        nextWorldStage[y][x - 1] = spotType

        # Copy the next stage and make it the current stage
        world = copy.deepcopy(nextWorldStage)

        # DEBUG -- Show the steps of generation
        if DEBUG and numEmptySpots > 0:
            displayWorld(world)
            print ""
            raw_input()

    return world

def spawnNode(world, nodeType):
    emptySpot = False

    while not emptySpot:
        x = random.randint(0, len(world[0]) - 1)
        y = random.randint(0, len(world) - 1)

        if notOccupied(world[y][x]):
            world[y][x] = nodeType
            emptySpot = True

    return world


def notOccupied(occupant):
    return occupant == 0

def displayWorld(world):
    # This is needed for colors to show up on windows command line, can be commented out
    # on Linux
    os.system('color')
    lineColor = '\033[0m'

    # Iterate over the world, display each tile
    for x in range(len(world)):
        for y in range(len(world[x])):
            sqaureColor = ""
            square = world[x][y]

            # The colors work as follows:
            # u'\u001b[38;5;Xm' -- Foreground (i.e. text) color
            # u'\u001b[48;5;Xm' -- background color
            # Where X is a value between 0 and 255 inclusive 
            # Color List: https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit

            # Water will be blue, land will be green
            if square == "w":
                print u'\u001b[48;5;26m' + " ",
            elif square == "l":
                print u'\u001b[48;5;28m' + " ",
            # elif square == "s":

            else:
                print lineColor + " ",
        
        # Reset the coloring
        print lineColor

def main():
    world = generateWorld(100, 60)
    displayWorld(world)

if __name__ == '__main__':
    main()