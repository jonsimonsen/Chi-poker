import random
import bot_context
from bots.bot import *
from bots.dealhand import *

class Ai_gen0(Bot):
    def __init__(self, hand):
        super().__init__(hand)

    def arrangeBoard(self):
            back = -1
            middle = -1
            front = -1
            state = -1

            while state < START_QUADS:
                sfl = findStraightFlush(hand)
                if sfl is None:
                    state = START_QUADS
                elif back == -1:
                    back = sfl
                else:
                    middle = sfl
                    state = START_THREE
            duplicates = findDuplicates(hand)
            while state < START_FH:
                quad = findQuads(duplicates)
                if quad is None:
                    state = START_FH
                elif back == -1:
                    back = quad
                    print(hand[0])
                    hand[0] = hand[0] ^ (0b1 << (22 - quad))
                    print(hand[0])
                    print(duplicates)
                    duplicates[quad - 10] = 0
                    print(duplicates)
                else:
                    middle = quad
                    print(hand[0])
                    hand[0] = hand[0] ^ (0b1 << (22 - quad))
                    print(hand[0])
                    print(duplicates)
                    duplicates[quad - 10] = 0
                    print(duplicates)
                    state = START_THREE

if __name__ == '__main__':
    hand = processHand(dealHand())
    dumb_bot = Ai_gen0(hand)
    printHand(dumb_bot.hand)
    dumb_bot.arrangeBoard()
