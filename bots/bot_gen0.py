if __name__ == '__main__':
    import bot_context

from bots.bot import *
from hands.dealhand import *
import random

class Ai_gen0(Bot):
    def __init__(self, hand):
        super().__init__(hand)

    def arrangeBoard(self):
            back = -1
            middle = -1
            front = -1
            state = -1

            # Straight flush
            while state < START_QUADS:
                sfl = findStraightFlush(self.hand)
                if sfl is None:
                    state = START_QUADS
                elif back == -1:
                    back = sfl
                else:
                    middle = sfl
                    state = START_THREE

            # Find duplicates for Quads/Full house
            duplicates = findDuplicates(self.hand)
            
            # Quads
            while state < START_FH:
                quad = findQuads(self.hand, duplicates)
                if quad is None:
                    state = START_FH
                elif back == -1:
                    back = quad
                else:
                    middle = quad
                    state = START_THREE

            # Full house
            lock = False
            while state < START_FL:
                fh = findFullHouse(self.hand, duplicates, lock)
                if fh is None:
                    state = START_FL
                elif back == -1:
                    back = fh
                    self.locked_pairs = 1
                    lock = True
                else:
                    middle = fh
                    self.locked_pairs += 1
                    state = START_THREE

            # Flush
            flush = findFlush(self.hand)

            # Update board
            self.board = [back, middle, front]

if __name__ == '__main__':
    hand = processHand(dealHand())
    dumb_bot = Ai_gen0(hand)
    print("Start hand: ")
    printHand(dumb_bot.hand)
    dumb_bot.arrangeBoard()
    print("Summary: " + str(dumb_bot.board))
    printHand(dumb_bot.hand)
