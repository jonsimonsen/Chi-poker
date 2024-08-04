"""Test straight flush hands.

Test board arrangement for straight flush hands.
Currently uses the gen 0 bot in the tests.
"""

import test_context
from hands.dealhand import *
from bots.bot_gen0 import *
from tests.testhands import *

def main():
    """Test various categories of straight flush hands."""

    dumb_bot = Ai_gen0([0, 0, 0, 0])

    # 10 card suits
    SUITS_10 = [SFL10_A_9, SFL10_A_6, SFL10_K_5, SFL10_A_F, SFL10_5_F, FL10_A_8]
    STRING_10 = ["A to 5: ", "A and 6: ", "K and 5: ", "A and 8f: ", "5 and Kf: ", "Af and 8f: "]

    for i in range(len(SUITS_10)):
        dumb_bot.resetHand([SUITS_10[i], THREE_CARDS, NO_HAND, NO_HAND])
        dumb_bot.arrangeBoard()
        print(STRING_10[i])
        print(dumb_bot.board)
        print(dumb_bot.hand)

if __name__ == '__main__':
    main()