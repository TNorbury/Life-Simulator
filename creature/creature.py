import random

MAX_THIRST = 10
MAX_HEALTH = 5

# Creates are a base class for things that inhabit the world6
class Creature:
    # Creature Attributes
    # m_turnPerformed -- This is just a flag to indicate if this creature has performed all its actions during a turn
    # m_lifeSpan -- This is a counter to determine how many turn a creature has left before it dies
    # m_thirst -- how much the create has a desire to drink water, if it runs out they start to die
    # m_thirstThreshold -- how low the creature's thirst can get before having to search for a drink
    # m_vision -- How far away the creature can see
    # m_health -- How many turns can the creature survive negative actions (i.e. dehydration) before it dies

    def __init__(self):
        self.name=""
        self.m_turnPerformed = False

        # The lifespan for each creature will be random
        self.m_lifeSpan = random.randint(25, 50)

        # All creatures have the same amount of thirst, however some are able to
        # wait longer before searching for a drink
        self.m_thirst = MAX_THIRST
        self.m_thirstThreshold = random.randint(1, int(MAX_THIRST / 2))

        # We'll change this later, for now all creatures can see the same distance
        self.m_vision = 1

        self.m_health = MAX_HEALTH

    def performTurn(self):
        # In order to prevent a circular import issue, we'll wait until we need
        # the world in order to import it
        import world.world as p_world
        
        if not self.m_turnPerformed:
            # First, pay attention to the world around us
            world = p_world.World.getInstance()

            # Now, let's explore the world, start be finding our position
            x, y = world.findCreature(self)

            # Sometimes the only action left to do is die, so if this creature's life span is empty
            # then remove it from the map
            if self.m_lifeSpan == 0:
                world.removeOccupant(x, y)
                return

            if x != -1 and y != -1:

                # If the creature is thirsty look for something to drink
                if (self.m_thirst < self.m_thirstThreshold):
                    # The creature looks around, in search of something to drink
                    for i in range(0 - self.m_vision, self.m_vision + 1):
                        for j in range(0 - self.m_vision, self.m_vision + 1):
                            # If this space is water, drink from it
                            if world.isWater(x + i, y + j):
                                self.m_thirst = MAX_THIRST
                                self.m_health = MAX_HEALTH
                                self.m_turnPerformed = True
                                break
                        if self.m_turnPerformed:
                            break

                # If no action has been performed yet, then the creature will explore
                # elif not self.m_turnPerformed:
                if not self.m_turnPerformed:
                    # Random movement, when the creature doesn't have any needs to fulfill
                    # The creature can move to any adjacent land position that isn't occupied
                    horizontalMoves = list(range(-1, 2))
                    verticalMoves = list(range(-1, 2))
                    random.shuffle(horizontalMoves)
                    random.shuffle(verticalMoves)

                    # Go over the random assortment of possible moves, looking for one that is valid
                    for i in horizontalMoves:
                        for j in verticalMoves:
                            if world.validMove(x + i, y + j):
                                world.moveOccupant(x, y, x + i, y + j)
                                self.m_turnPerformed = True
                                break
                        if self.m_turnPerformed:
                            break

                self.m_turnPerformed = True


    def dayOver(self):
        import world.world as p_world
        world = p_world.World.getInstance()
        x, y = world.findCreature(self)

        self.m_turnPerformed = False

        self.m_lifeSpan -= 1
        self.m_thirst -= 1

        # If the creature has run out of thrist, then start damaging its health
        if self.m_thirst <= 0:
            self.m_health -= 1

        # When the creature's health reaches 0, then it dies
        if self.m_health <= 0:
            world.removeOccupant(x, y)

    # Returns a string that can be pretented to represent this creature
    def toString(self):
        creatureColor = u'\u001b[38;5;178m'

        # If the creature is thristy, display it as a red X
        if (self.m_thirst < self.m_thirstThreshold):
            creatureColor = u'\u001b[38;5;196m'
        return creatureColor + "X"
