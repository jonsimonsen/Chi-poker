"""A child class for the dumbest Chinese poker bot.

The bot always arranges the strongest hand in the back.
Then it arranges the strongest remaining hand in the middle.
It never folds.

arrangeBoard() handles the arrangement of board and hand.
"""

if __name__ == '__main__':
    import bot_context

from bots.bot import *
from hands.dealhand import *
import random

class Ai_gen0(Bot):
    """Class for a generation 0 poker bot."""
    def __init__(self, hand):
        super().__init__(hand)

    def arrangeBoard(self):
        """Update the board for the poker bot.

        Put the strongest hand in the back.
        Then put the strongest remaining hand in the middle. 
        """
        back = -1
        middle = -1
        front = -1
        board_rank = -1

        # Straight flush
        while board_rank < START_QUADS:
            sfl = self.findStraightFlush()
            if sfl is None:
                board_rank = START_QUADS
            elif back == -1:
                back = sfl
            else:
                middle = sfl
                board_rank = START_THREE

        # Find duplicates for Quads/Full house
        self.ranks = findDuplicates(self.suits)
        
        # Quads
        while board_rank < START_FH:
            quad = self.findQuads()
            if quad is None:
                board_rank = START_FH
            elif back == -1:
                back = quad
            else:
                middle = quad
                board_rank = START_THREE

        # Full house
        while board_rank < START_FL:
            fh = self.findFullHouse()
            if fh is None:
                board_rank = START_FL
            elif back == -1:
                back = fh
                self.locked_pairs = 1
            else:
                middle = fh
                self.locked_pairs += 1
                board_rank = START_THREE

        # Flush
        while board_rank < START_STR:
            flush = self.findFlush()
            if flush is None:
                board_rank = START_STR
            elif back == -1:
                back = flush
            else:
                middle = flush
                board_rank = START_THREE

        # Straight
        straight = self.findStraight()

        # Update board
        self.board = [back, middle, front]

if __name__ == '__main__':
    hand = processHand(dealHand())
    dumb_bot = Ai_gen0(hand)
    print("Start hand: ")
    printHand(dumb_bot.suits)
    dumb_bot.arrangeBoard()
    print("Summary: " + str(dumb_bot.board))
    printHand(dumb_bot.suits)

    dumb_bot.resetHand([0b1001100001101010, 0b11000000000001, 0b10100100000000, 0b10100010001000])
    print("Start hand: ")
    printHand(dumb_bot.suits)
    dumb_bot.arrangeBoard()
    print("Summary: " + str(dumb_bot.board))
    printHand(dumb_bot.suits)
