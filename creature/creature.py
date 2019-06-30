import random

# Creates are a base class for things that inhabit the world6
class Creature:
    # Creature Attributes
    # m_turnPerformed -- This is just a flag to indicate if this creature has performed all its actions during a turn
    # m_lifeSpan -- This is a counter to determine how many turn a creature has left before it dies


    def __init__(self):
        self.name=""
        self.m_turnPerformed = False

        # The lifespan for each creature will be random, but 
        self.m_lifeSpan = random.randint(1, 21)

    def performTurn(self):
        # In order to prevent a circular import issue, we'll wait 
        # from world.world import World
        import world.world as p_world
        
        if not self.m_turnPerformed:
            # First, pay attention to the world around us
            world = p_world.World.getInstance()

            # Now, let's explore the world, start be finding our position
            x, y = world.findCreature(self)

            # Sometimes the only action left to do is die, so if this creature's life span is empty
            # then remove it from the map
            if (self.m_lifeSpan == 0):
                world.removeOccupant(x, y)

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

                self.m_turnPerformed = True
                self.m_lifeSpan -= 1

    def dayOver(self):
        self.m_turnPerformed = False

    # Returns a string that can be pretented to represent this creature
    def toString(self):
        return u'\u001b[38;5;178m' + "X"
