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

        for i in range(len(FUNCS_5)):
            category = self.findHandCategory(FUNCS_5[i][0], FUNCS_5[i][1])
            if category == START_3:
                break
        for j in range (len(FUNCS_3)):
            category = self.findHandCategory(FUNCS_3[j][0], FUNCS_3[j][1])
            if category == END_3_HI:
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
            elif functionName.startswith("findThree"):
                self.board[2] = hand
                thisCategory = END_3_HI
            elif self.board[0] == -1:
                self.board[0] = hand
            else:
                self.board[1] = hand
                thisCategory = START_3
        
        return thisCategory


if __name__ == '__main__':
    #Simulate multiple hands
    numHands = 200
    print("Simulating " + str(numHands) + " Chinese poker hands:\n")
    dumb_bot = Ai_gen0([0, 0, 0, 0])
    dumb_bot.simulateHands(numHands)

    """hand = None
    # Arrange 50 random hands
    for i in range(50):
        hand = processHand(dealHand())
        dumb_bot.resetHand(hand)
        print("Hand " + str(i) + ":\n")
        printHand(dumb_bot.suits)
        dumb_bot.arrangeBoard()
        print("Summary: " + str(dumb_bot.board))
        print("Bonus: " + str(dumb_bot.bonus))
        print("")"""

    # Test specific hands
    print("Test specific hands:\n")


    """print("Old issue - Should probably be removed")
    dumb_bot.resetHand([0b1001100001101010, 0b11000000000001, 0b10100100000000, 0b10100010001000])
    print("Start hand: ")
    printHand(dumb_bot.suits)
    dumb_bot.arrangeBoard()
    print("Summary: " + str(dumb_bot.board))"""

    """print("Straight issue")
    dumb_bot.resetHand([0b100101000100010, 0b11000100000001, 0b10100001010000, 0b10010100010000])
    print("Start hand: ")
    printHand(dumb_bot.suits)
    dumb_bot.arrangeBoard()
    print("Summary: " + str(dumb_bot.board))"""

    """print("Two pair issue")
    dumb_bot.resetHand([0b100011000000011, 0b100001010100100, 0b10010100100000, 0b10000100010000])
    print("Start hand: ")
    printHand(dumb_bot.suits)
    dumb_bot.arrangeBoard()
    print("Summary: " + str(dumb_bot.board))"""

    """print("Hi card issue")
    dumb_bot.resetHand([0b100011000011000, 0b100010000100110, 0b100000100010000, 0b100000010010001])
    print("Start hand: ")
    printHand(dumb_bot.suits)
    dumb_bot.arrangeBoard()
    print("Summary: " + str(dumb_bot.board))"""

    """print("Test nut low flush")
    dumb_bot.resetHand([0b110000000101111, 0b11100100000000, 0b11100100000000, 0b10001010000000])
    print("Start hand: ")
    printHand(dumb_bot.suits)
    dumb_bot.arrangeBoard()
    print("Summary: " + str(dumb_bot.board))"""

    """print("Rank issue (locked pair used)")
    dumb_bot.resetHand([0b110001110011001, 0b10101000000000, 0b10100010000010, 0b10010010000000])
    print("Start hand: ")
    printHand(dumb_bot.suits)
    dumb_bot.arrangeBoard()
    print("Summary: " + str(dumb_bot.board))"""

    """print("Double flush issue")
    dumb_bot.resetHand([0b111010000100110, 0b110100110000101, 0b10001000010000, 0b10000001000000])
    print("Start hand: ")
    printHand(dumb_bot.suits)
    dumb_bot.arrangeBoard()
    print("Summary: " + str(dumb_bot.board))"""

