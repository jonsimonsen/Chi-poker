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

        for num in range(len(FUNCS)):
            cat = self.findHandCategory(FUNCS[num][0], FUNCS[num][1])
            if cat == START_THREE:
                break
    
    def findHandCategory(self, functionName, nextCategory):
        """Return the rank of the next hand to search for.

        Call the function with functionName until it returns None or
        the first two slots of the board is taken.
        This should correspond to having found all remaining hands that are 
        higher ranking than nextCategory.
        This assumes that all higher ranking hands than those being searched for
        by the function is already found.
        """
        method = getattr(self, functionName)
        thisCategory = nextCategory - 1
        while(thisCategory < nextCategory):
            hand = method()
            if hand is None:
                thisCategory = nextCategory
            elif self.board[0] == -1:
                self.board[0] = hand
            else:
                self.board[1] = hand
                thisCategory = START_THREE
        
        return thisCategory


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
