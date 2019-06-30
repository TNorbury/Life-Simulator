import random

# Creates are a base class for things that inhabit the world6
class Creature:

    def __init__(self):
        self.name=""
        self.turnPerformed = False

    def performTurn(self):
        # In order to prevent a circular import issue, we'll wait 
        # from world.world import World
        import world.world as p_world
        
        if not self.turnPerformed:
            # First, pay attention to the world around us
            world = p_world.World.getInstance()

            # Now, let's explore the world, start be finding our position
            x, y = world.findCreature(self)

            if x != -1 and y != -1:
                # The creature can move to any adjacent land position that isn't occupied
                horizontalMoves = list(range(-1, 2))
                verticalMoves = list(range(-1, 2))
                random.shuffle(horizontalMoves)
                random.shuffle(verticalMoves)

                moveMade = False

                # Go over the random assortment of possible moves, looking for one that is valid
                for i in horizontalMoves:
                    for j in verticalMoves:
                        if world.validMove(x + i, y + j):
                            world.moveOccupant(x, y, x + i, y + j)
                            moveMade = True
                            break
                    if moveMade:
                        break

                # world.moveOccupant(x, y, x + 1, y)
                self.turnPerformed = True

    def dayOver(self):
        self.turnPerformed = False

    # Returns a string that can be pretented to represent this creature
    def toString(self):
        return u'\u001b[38;5;178m' + "X"
