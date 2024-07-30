import test_context
from hands.dealhand import *
from bots.bot_gen0 import *
from tests.testhands import *

def main():
    hand_1 = A_SFL
    dumb_bot = Ai_gen0(hand_1)
    dumb_bot.arrangeBoard()
    print(dumb_bot.hand)
    print(dumb_bot.board)
    """ hand_1 = arrangeHand(A_SFL)
    print(hand_1)
    hand_2 = arrangeHand(QUAD_A)
    print(hand_2) """
    # Needs rewriting

if __name__ == '__main__':
    main()
    