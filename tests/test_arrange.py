import test_context
from hands.dealhand import *
from bots.bot_gen0 import *
from tests.testhands import *

def main():
    hand_1 = A_SFL
    dumb_bot = Ai_gen0(hand_1)
    print("Start hand: ")
    printHand(dumb_bot.hand)
    dumb_bot.arrangeBoard()
    print("Summary: " + str(dumb_bot.board))
    printHand(dumb_bot.hand)

    hand_2 = QUAD_A
    dumb_bot2 = Ai_gen0(hand_2)
    print("Start hand: ")
    printHand(dumb_bot2.hand)
    dumb_bot2.arrangeBoard()
    print("Summary: " + str(dumb_bot2.board))
    printHand(dumb_bot2.hand)

if __name__ == '__main__':
    main()
    