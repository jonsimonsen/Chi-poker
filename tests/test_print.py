import test_context
from bots.dealhand import *

def main():
    # Test dealing a hand and printing it out
    nuts = dealHand()
    printCards(nuts)
    nuts= processHand(nuts)
    printHand(nuts)

if __name__ == '__main__':
    main()
