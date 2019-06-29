from world import World
import argparse

def main():

    # Define the arguments for the program
    parser = argparse.ArgumentParser(description="Generates a world and simulates life on it")
    parser.add_argument("--width", dest="width", nargs="?", metavar="width", default=10, type=int, help="Set the width of the world")
    parser.add_argument("--height", dest="height", nargs="?", metavar="height", default=10, type=int, help="Set the height of the world")

    args = parser.parse_args()

    width = args.width
    height = args.height

    world = World(width, height)
    world.generateWorld()
    world.displayWorld()

if __name__ == '__main__':
    main()