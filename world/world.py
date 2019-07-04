import random
import os
import copy
import math
import sys

# Importing packages from other parts of the project
import creature.creature as p_creature

DEBUG = False

# Nodes are what make up the world, they have a terrain and an occupant
class Node:
    # Node Attributes
    # m_terrain -- the terrain of the node
    # m_occupant -- the occupant of the node

    # Land "l" is the only valid type of land right now
    VALID_LAND = {"l"}

    def __init__(self):
        self.m_terrain = ""
        self.m_occupant = 0

    def terrain(self):
        return self.m_terrain

    def setTerrain(self, terrain):
        self.m_terrain = terrain

    def hasTerrain(self):
        return self.m_terrain != ""

    def isLand(self):
        # No terrain? Probably not land then
        if (not self.hasTerrain()):
            return False
        
        # Make sure the current terrain type is land
        return self.m_terrain in self.VALID_LAND  

    def isWater(self):
        # If it's not land then it's water
        return not self.isLand()      

    def setOccupant(self, occupant):
        self.m_occupant = occupant

    def isOccupied(self):
        return self.m_occupant != 0

    def toString(self):
        # The colors work as follows:
        # u'\u001b[38;5;Xm' -- Foreground (i.e. text) color
        # u'\u001b[48;5;Xm' -- background color
        # Where X is a value between 0 and 255 inclusive 
        # Color List: https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit

        # This resets the terminal colors
        lineColor = '\033[0m'

        terrainDisplay = ""
        occupantDisplay = ""

        # Water will be blue, land will be green
        if self.m_terrain == "w":
            terrainDisplay = u'\u001b[48;5;26m'
        elif self.m_terrain == "l":
            terrainDisplay = u'\u001b[48;5;28m'

        else:
            # This really only gets used in debug mode in order
            # to display blank spaces
            terrainDisplay = lineColor

        # The occupying creature will know how to display itself
        if (self.isOccupied()):
            occupantDisplay = self.m_occupant.toString()
        
        # If there is no occupant, then we'll just have an empty space
        else:
            occupantDisplay = " "

        return terrainDisplay + occupantDisplay
    

# This "world" uses an X, Y coordinate system, with the origin in the uper left hand corner 
class World:
    # World Attributes:
    # m_width -- width of the world
    # m_height -- height of the world
    # m_world -- Array that holds the data of the world
    # m_creatureRate -- Percentage (0%-100%) of land tiles that will have a creature spawn
    #                   on it
    # m_numLandTiles -- The number of land tiles in the world

    # The world will be a singleton, so it'll keep track of its instance
    m_instance = None

    @staticmethod
    def getInstance():
        if World.m_instance != None:
            return World.m_instance

    # Constructor. 
    # This will only be called by the simulation upon start up.
    # Any other attempts to create a new world will cause an error
    def __init__(self, width, height, creatureRate):
        if World.m_instance != None:
            raise Exception("The world already exists!")
        else:
            self.m_width = width
            self.m_height = height
            self.m_creatureRate = creatureRate

            # initialize the array that houses the world
            self.m_world = [[Node() for x in range(self.m_width)] for y in range(self.m_height)]

            World.m_instance = self
            # random.seed(10)


    # Procedurally generate the world map
    def generateWorld(self):
        # Water and land spots will start with a random number of nodes between 1
        # and 10% of the total area of the map
        for _ in range(random.randint(1, int(math.ceil((self.m_width * self.m_height) * 0.1)))):
            self.spawnNode("w")

        self.m_numLandTiles = random.randint(1, int(math.ceil((self.m_width * self.m_height) * 0.1)))
        for _ in range(self.m_numLandTiles):
            self.spawnNode("l")

        # DEBUG -- Show the initial generation
        if DEBUG:
            self.displayWorld()
            print("")
            input()

        # Now that we have the initial terrain nodes laid out, start to propagate them until
        # the world is filled
        self.propagateTerrain()

        # Now, spawn creatures in the world
        self.spawnCreatures()


    def propagateTerrain(self):
        xCoordinates = list(range(self.m_width))
        yCoordinates = list(range(self.m_height))

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


    def spawnCreatures(self):
        # Firstly, we need to determine the number of creatures that will be on this map
        numCreatures = math.ceil((self.m_creatureRate / 100) * self.m_numLandTiles)

        # Now, spawn the number of creatures in the appropriate locations
        for _ in range(numCreatures):
            emptySpot = False

            while not emptySpot:
                x = random.randint(0, self.m_width - 1)
                y = random.randint(0, self.m_height - 1)

                # Find a spot that doesn't have an occupant yet and is land
                if not self.m_world[y][x].isOccupied() and self.m_world[y][x].isLand():
                    self.m_world[y][x].setOccupant(p_creature.Creature())
                    # self.m_world[y][x].m_occupant.performTurn()
                    emptySpot = True


    def spawnNode(self, nodeType):
        emptySpot = False

        while not emptySpot:
            x = random.randint(0, self.m_width - 1)
            y = random.randint(0, self.m_height - 1)

            # Find a spot that doesn't have terrain yet
            if not self.m_world[y][x].hasTerrain():
                self.m_world[y][x].setTerrain(nodeType)
                emptySpot = True


    def findCreature(self, creature):
        # Search the map for a given creature
        for x in range(self.m_width):
            for y in range(self.m_height):
                if self.m_world[y][x].m_occupant == creature:
                    return x, y
        
        return -1, -1

    # Simulate a single turn on this world
    def performTurn(self):
        xCoordinates = list(range(self.m_width))
        yCoordinates = list(range(self.m_height))
            
        # Go through all the nodes in a random order and have them perform a turn
        random.shuffle(xCoordinates)
        for x in xCoordinates:
            random.shuffle(yCoordinates)
            for y in yCoordinates:
                if self.m_world[y][x].isOccupied():
                    self.m_world[y][x].m_occupant.performTurn()

        # Now that all the turns have be performed, tell
        # all the creatures that they can perform a turn again
        livingCreautres = False
        for x in range(self.m_width):
            for y in range(self.m_height):
                if self.m_world[y][x].isOccupied():
                    self.m_world[y][x].m_occupant.dayOver()

                    # There is still something living out there
                    livingCreautres = True
        
        return livingCreautres

    def inBounds(self, x, y):
        if x < 0 or x >= self.m_width or y < 0 or y >= self.m_height:
            return False
        return True
        
    def validMove(self, x, y):
        # boundary check
        if not self.inBounds(x, y):
            return False
        
        return self.m_world[y][x].isLand() and not self.m_world[y][x].isOccupied()

    def isWater(self, x, y):
        # boundary check
        if not self.inBounds(x, y):
            return False

        return self.m_world[y][x].isWater()

    def moveOccupant(self, oldX, oldY, newX, newY):
        # Do a boundary check first 
        if not self.inBounds(oldX, oldY) or not self.inBounds(newX, newY):

            # TEST CODE REMOVE LATER, if the boundary is reached, kill the occupant
            self.m_world[oldY][oldX].setOccupant(0)

            return

        # Firstly, set the occupant at its new location
        self.m_world[newY][newX].setOccupant(self.m_world[oldY][oldX].m_occupant)

        # Then remove it from its old location
        self.removeOccupant(oldX, oldY)


    def removeOccupant(self, x, y):
        if (self.inBounds(x, y)):
            self.m_world[y][x].m_occupant = 0

    def displayWorld(self):
        # This is needed for colors to show up on windows command line
        if (os.name=="nt"):
            os.system('color')
        lineColor = '\033[0m'

        # Print the horizontal coordinates
        print(" ", end="")
        for x in range(len(self.m_world[0])):
            print(x % 10, end="")
        print("")

        # Iterate over the world, display each tile
        for x in range(len(self.m_world)):
            print(x % 10, end="")
            for y in range(len(self.m_world[x])):
                print(self.m_world[x][y].toString(), end="")
            
            # Reset the coloring
            print(lineColor)
        print("")
            


# This main mostly exists for testing purposes, so that we can see if the world is
# generate properly
def main():
    world = World(5, 5, 50)
    world.generateWorld()
    world.displayWorld()


if __name__ == '__main__':
    main()
