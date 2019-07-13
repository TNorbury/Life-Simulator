import argparse
import time
import tkinter

# Importing packages from other parts of the project
import world.world as p_world

def sim():
    # Firstly, get rid of the start button
    for child in root.children.values():
        if child.winfo_rootx() - root.winfo_rootx() == 0 \
            and child.winfo_rooty() - root.winfo_rooty() == 0:
            widget = child

    widget.destroy()

    root.update()

    p_world.World(width, height, creatureRate, root)
    world = p_world.World.getInstance()
    world.generateWorld()
    world.displayWorld()
    while True:
        # Nothing is left alive, display the world one more time and then exit
        if not world.performTurn():
            world.displayWorld()
            break
        world.displayWorld()
        time.sleep(.5)


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

# Start by creating the GUI
root = tkinter.Tk(screenName="simulation")

# This button will start the simulation
tkinter.Button(root, text="start", command=sim).grid(row=0, column=0)

root.mainloop()
