"""A test function for printing hands."""

import test_context
from hands.dealhand import *

def main():
    # Test dealing a hand and printing it out
    nuts = dealHand()
    print("Unprocessed hand:")
    printCards(nuts)
    nuts= processHand(nuts)
    print("Processed hand:")
    printHand(nuts)

if __name__ == '__main__':
    main()
