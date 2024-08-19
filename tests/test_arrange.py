"""Test board arrangement for the gen 0 bot.

Tests some selected hand types.
"""

import test_context
from hands.dealhand import *
from bots.bot_gen0 import *
from tests.testhands import *

def main():
    hand_1 = A_SFL
    dumb_bot = Ai_gen0(hand_1)
    print("Start hand: ")
    printHand(dumb_bot.suits)
    dumb_bot.arrangeBoard()
    print("Summary: " + str(dumb_bot.board))
    printHand(dumb_bot.suits)

    hand_2 = QUAD_A
    dumb_bot2 = Ai_gen0(hand_2)
    print("Start hand: ")
    printHand(dumb_bot2.suits)
    dumb_bot2.arrangeBoard()
    print("Summary: " + str(dumb_bot2.board))
    printHand(dumb_bot2.suits)

    hand_4 = A_FLUSH
    dumb_bot4 = Ai_gen0(hand_4)
    print("Start hand: ")
    printHand(dumb_bot4.suits)
    dumb_bot4.arrangeBoard()
    print("Summary: " + str(dumb_bot4.board))
    printHand(dumb_bot4.suits)

if __name__ == '__main__':
    main()
    