import random
import os
import copy

DEBUG = False

# Nodes are what make up the world, they have a terrain and an occupant
class Node:
    # Node Attributes
    # m_terrain -- the terrain of the node
    # m_occupant -- the occupant of the node

    def __init__(self):
        self.m_terrain = ""
        self.m_occupant = ""

    def terrain(self):
        return self.m_terrain

    def setTerrain(self, terrain):
        self.m_terrain = terrain

    def hasTerrain(self):
        return self.m_terrain != ""

    def setOccupant(self, occupant):
        self.m_occupant = occupant

    def isOccupied(self):
        return self.m_occupant != ""

    def toString(self):
        # The colors work as follows:
        # u'\u001b[38;5;Xm' -- Foreground (i.e. text) color
        # u'\u001b[48;5;Xm' -- background color
        # Where X is a value between 0 and 255 inclusive 
        # Color List: https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit

        # This resets the terminal colors
        lineColor = '\033[0m'

        # Water will be blue, land will be green
        if self.m_terrain == "w":
            return u'\u001b[48;5;26m' + " "
        elif self.m_terrain == "l":
            return u'\u001b[48;5;28m' + " "

        else:
            # This really only gets used in debug mode in order
            # to display blank spaces
            return lineColor + " "
    

# This "world" uses an X, Y coordinate system, with the origin in the uper left hand corner 
class World:
    # World Attributes:
    # m_width -- width of the world
    # m_height -- height of the world
    # m_world -- Array that holds the data of the world

    # Constructor
    def __init__(self, width, height):
        self.m_width = width
        self.m_height = height
        
        # initialize the array that houses the world
        self.m_world = [[Node() for x in range(self.m_width)] for y in range(self.m_height)]

        # random.seed(69)

    # Procedurally generate the world map
    def generateWorld(self):

        # Water and land spots will start with a random number of nodes between 1
        # and 10% of the total area of the map
        for _ in range(random.randint(1, int((self.m_width * self.m_height) * 0.1))):
            self.spawnNode("w")

        for _ in range(random.randint(1, int((self.m_width * self.m_height) * 0.1))):
            self.spawnNode("l")

        # Spawn a single desert tile
        # world = spawnNode(world, "s")

        # DEBUG -- Show the initial generation
        if DEBUG:
            self.displayWorld()
            print("")
            input()

        xCoordinates = list(range(len(self.m_world[0])))
        yCoordinates = list(range(len(self.m_world)))

        # Now, go through all the spots and expand the land and water, until all spots are filled
        numEmptySpots = 1

        # We generate the map by determining what the next stage will look like, so we need to make a second
        # map of the same size as our "master" map
        nextWorldStage = [[Node() for x in range(self.m_width)] for y in range(self.m_height)]
        while numEmptySpots > 0:
            numEmptySpots = 0

            # shuffle the coordinates, giving a random priority for expansion 
            random.shuffle(xCoordinates)
            for x in xCoordinates:
                random.shuffle(yCoordinates)
                for y in yCoordinates:

                    # Count the number of empty spots
                    if not self.m_world[y][x].hasTerrain():
                        numEmptySpots += 1
                    
                    # Otherwise, expand the spot's type in the "cardinal" directions
                    # No expanding pass the boundaries of the world
                    else:
                        # If this is an occupied space, then we'll set that in the next iteration
                        nextWorldStage[y][x].setTerrain(self.m_world[y][x].terrain())
                        
                        # Along with setting the neighboring coordinates 
                        # North
                        if (y - 1) >= 0 and not nextWorldStage[y - 1][x].hasTerrain():
                            nextWorldStage[y - 1][x].setTerrain(self.m_world[y][x].terrain())
                        
                        # East
                        if (x + 1) < self.m_width and not nextWorldStage[y][x + 1].hasTerrain():
                            nextWorldStage[y][x + 1].setTerrain(self.m_world[y][x].terrain())
                        
                        # South
                        if (y + 1) < self.m_height and not nextWorldStage[y + 1][x].hasTerrain():
                            nextWorldStage[y + 1][x].setTerrain(self.m_world[y][x].terrain())

                        # West
                        if (x - 1) >= 0 and not nextWorldStage[y][x - 1].hasTerrain():
                            nextWorldStage[y][x - 1].setTerrain(self.m_world[y][x].terrain())

            # Copy the next stage and make it the current stage
            self.m_world = copy.deepcopy(nextWorldStage)

            # DEBUG -- Show the steps of generation
            if DEBUG and numEmptySpots > 0:
                self.displayWorld()
                print("")
                input()

    def spawnNode(self, nodeType):
        emptySpot = False

        while not emptySpot:
            x = random.randint(0, self.m_width - 1)
            y = random.randint(0, self.m_height - 1)

            # if self.notOccupied(x, y):
            # Find a spot that doesn't have terrain yet
            if not self.m_world[y][x].hasTerrain():
                self.m_world[y][x].setTerrain(nodeType)
                emptySpot = True

    def displayWorld(self):
        # This is needed for colors to show up on windows command line, can be commented out
        # on Linux
        if (os.name=="nt"):
            os.system('color')
        lineColor = '\033[0m'

        # Iterate over the world, display each tile
        for x in range(len(self.m_world)):
            for y in range(len(self.m_world[x])):
                print(self.m_world[x][y].toString(), end="")
            
            # Reset the coloring
            print(lineColor)

def main():
    world = World(75, 25)
    world.generateWorld()
    world.displayWorld()


if __name__ == '__main__':
    main()
