import random
import os
import copy

# This "world" uses an X, Y coordinate system, with the origin in the uper left hand corner 

def generateWorld(height, width):
    # Initialize the array
    world = [[0 for y in range(height)] for x in range(width)]
    # random.seed(69)

    # Pick n spots (equal to 10% of total size) to place water and land starts
    # 5% for water, 5% for land
    numSpots = int((width * height) * 0.01);
    # numSpots = 5
    for i in range(numSpots):
        emptySpot = False

        while not emptySpot:
            # add a water spot
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)

            if notOccupied(world[x][y]):
                world[x][y] = "w"
                emptySpot = True
            
        emptySpot = False
        while not emptySpot:
            # add a land spot
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)

            if notOccupied(world[x][y]):
                world[x][y] = "l"
                emptySpot = True
            

    xCoordinates = range(len(world))
    yCoordinates = range(len(world[0]))

    # Now, go through all the spots and expand the land and water, until all spots are filled
    numEmptySpots = 1

    # We generate the map by determining what the next stage will look like, so we need to make a second
    # map of the same size as our "master" map
    nextWorldStage = [[0 for y in range(height)] for x in range(width)]
    while numEmptySpots > 0:
        numEmptySpots = 0

        # shuffle the coordinates, giving a random priority for expansion 
        random.shuffle(xCoordinates)
        for x in xCoordinates:
            random.shuffle(yCoordinates)
            for y in yCoordinates:
                spotType = world[x][y]

                # Count the number of empty spots
                if notOccupied(spotType):
                    numEmptySpots += 1
                
                # Otherwise, expand the spot's type in the "cardinal" directions
                # No expanding pass the boundaries of the world
                else:
                    # If this is an occupied space, then we'll set that in the next iteration
                    nextWorldStage[x][y] = spotType
                    
                    # Along with setting the neighboring coordinates 
                    # North
                    if (y - 1) >= 0 and notOccupied(nextWorldStage[x][y - 1]):
                        nextWorldStage[x][y - 1] = spotType
                    
                    # East
                    if (x + 1) < width and notOccupied(nextWorldStage[x + 1][y]):
                        nextWorldStage[x + 1][y] = spotType
                    
                    # South
                    if (y + 1) < height and notOccupied(nextWorldStage[x][y + 1]):
                        nextWorldStage[x][y + 1] = spotType

                    # West
                    if (x - 1) >= 0 and notOccupied(nextWorldStage[x - 1][y]):
                        nextWorldStage[x - 1][y] = spotType

        # Copy the next stage and make it the current stage
        world = copy.copy(nextWorldStage)

        # DEBUG -- Show the steps of generation
        # displayWorld(world)
        # print ""

    return world

def notOccupied(occupant):
    return occupant != "w" and occupant != "l"

def displayWorld(world):
    # This is needed for colors to show up on windows command line, can be commented out
    # on Linux
    os.system('color')
    lineColor = '\033[0m'
    # Print the top line
    # print lineColor + "_______________________________"

    # Iterate over the world, display each tile
    for x in range(len(world)):
        for y in range(len(world[x])):
            sqaureColor = ""
            square = world[x][y]

            # Water will be blue, land will be green
            if square == "w":
                sqaureColor = '\033[94m'
            elif square == "l":
                sqaureColor = '\033[92m'
            else:
                sqaureColor = '\033[0m'

            # print lineColor + "|",
            print sqaureColor + "X",
            
        # Print the end bracket
        # print lineColor + "|"
        print lineColor

def main():
    world = generateWorld(50, 50)
    # world = generateWorld(100, 70)
    displayWorld(world)


if __name__ == '__main__':
    main()