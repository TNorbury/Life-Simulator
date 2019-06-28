from world import World

def main():
    world = World(75, 25)
    world.generateWorld()
    world.displayWorld()

if __name__ == '__main__':
    main()