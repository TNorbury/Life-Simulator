import argparse
import time

# Importing packages from other parts of the project
import world.world as p_world

def main():

    # Define the arguments for the program
    parser = argparse.ArgumentParser(description="Generates a world and simulates life on it")
    parser.add_argument("--width", dest="width", nargs="?", metavar="width", default=10, type=int, help="Set the width of the world")
    parser.add_argument("--height", dest="height", nargs="?", metavar="height", default=10, type=int, help="Set the height of the world")
    parser.add_argument("--creatureRate", dest="creatureRate", nargs="?", metavar="creatureRate", 
        default=10, type=int, help="Set the percentage of land tiles that will have a creature spawn on it")

    args = parser.parse_args()

    width = args.width
    height = args.height
    creatureRate = args.creatureRate

    p_world.World(width, height, creatureRate)
    world = p_world.World.getInstance()
    world.generateWorld()
    world.displayWorld()
    while True:
        world.performTurn()
        world.displayWorld()
        time.sleep(.5)
        # input()

if __name__ == '__main__':
    main()