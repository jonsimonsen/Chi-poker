"""Test straight hands.

Test board arrangement for straight hands.
Currently uses the gen 0 bot in the tests.
"""

import test_context
from hands.dealhand import *
from bots.bot_gen0 import *
from tests.testhands import *

def main():
    """Test various categories of straight hands."""

    # Tested
    # 4 4 3-3 2-2 -T
    # 4 4 3-3 2 -T9
    # 4 4 3 2 -T6
    # 4 4 3-3 2-3 -JT
    dumb_bot = Ai_gen0([FOUR_CARDS, FOUR_CARDS, THREE_CARDS_V3, TWO_CARDS_V2])
    dumb_bot.arrangeBoard()

if __name__ == '__main__':
    main()
