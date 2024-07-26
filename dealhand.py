import random

CARDS = { # Key is position of the bit in the suit list
  0: "2",
  1: "3",
  2: "4",
  3: "5",
  4: "6",
  5: "7",
  6: "8",
  7: "9",
  8: "T",
  9: "J",
  10: "Q",
  11: "K",
  12: "A"
}

# Deal a 13 card hand for Chinese poker (cards represented as numbers from 0 to 51)
def dealHand():
    deck = list(range(52))
    hand = random.sample(deck, 13)
    hand.sort()
    return hand

# Encode a hand as 4 ints (one per suit) with the first three bits indicating the number of cards in the suit
def processHand(hand):
    i = 0
    suit = 1
    suits = [0, 0, 0, 0]

    while(suit < 5):
        count = 0
        while(i < 13 and hand[i] < suit * 13 ):
            suits[suit - 1] += 1 << (hand[i] % 13)
            count += 1
            i += 1
        print("count: " + str(count))
        suits[suit -1] += addLengthBits(count)
        suit += 1
    
    suits.sort(reverse=True)
    print(suits)
    return suits

# Create an int to encode the length of a suit as its most significant bits (for adding to the suit int)
def addLengthBits(count):
    # Python switch/case
    match count:
        case 0:
            return 0
        case 1 | 2 | 3:
            return 0b1 << 13
        case 4:
            return 0b1 << 14
        case 5:
            return 0b11 << 13
        case 6:
            return 0b1 << 15
        case 7:
            return 0b101 << 13
        case 8:
            return 0b11 << 14
        case _:
            return 0b111 << 13
    
# Print a hand showing cards in brackets for each suit. The input should be a newly generated (not processed) hand
def printCards(hand):
    i = 0
    suit = 1
    cards = ""

    while(suit < 5):
        cards += "[ "
        while(i < 13 and hand[i] < suit * 13 ):
            cards += str(hand[i]) + " "
            i += 1
        suit += 1
        cards += "]"

    print(cards)
    return

# Print a processed hand showing cards in brackets for each suit.
def printHand(hand):
    cards = ""
    for suit in hand:
        cards += "["
        for card in reversed(range(13)):
            bitmask = 0b1
            if (suit & (bitmask << card)) == (bitmask << card):
                cards += CARDS[card]
        cards += "]"
    print(cards)
    return

# Arrange a chinese pokerhand
def arrangeHand(hand):
    back = 0
    middle = 0
    front = 0

    sfl = findStraightFlush(hand)
    return

# Check a hand for a straight flush. Return None if not found. Otherwise, return a number corresponding to the strength
def findStraightFlush(hand):
    if hand[0] < (0b11 << 13):
        return -1
    else:
        rank = findStraight(hand[0])
        if rank is None:
            if hand[1] <( 0b11 << 13):
                return -2
            else:
                rank = findStraight(hand[1])

    return rank

# Check a hand for a straight
def findStraight(hand):
    # Check for ordinary straight
    bitmask = 0b11111
    for i in reversed(range(9)):
        if (hand & (bitmask << i)) == (bitmask << i):
            return 8 - i
    # Check for wheel
    bitmask = 0b1111
    if(hand & bitmask) == bitmask:
        if(hand & 1 << 12):
            return 9
    return -3

# Test dealing a hand and printing it out
""" nuts = dealHand()
printCards(nuts)
nuts= processHand(nuts)
printHand(nuts)
arrangeHand(nuts) """

# Test specific hands
A_SFL = [0b1001111100000100, 0b101000100010001, 0b10000010100000, 0b10000001000000]
T_SFL = [0b1001000111110000, 0b101000100010001, 0b10000010100000, 0b10000001000000]
SIX_SFL = [0b1000000100011111, 0b101000100010001, 0b10000010100000, 0b10000001000000]
WHEEL_FL = [0b1001000100001111, 0b101000100010001, 0b10000010100000, 0b10000001000000]
print("Ace: " + str(findStraightFlush(A_SFL)))
print("Ten: " + str(findStraightFlush(T_SFL)))
print("Six: " + str(findStraightFlush(SIX_SFL)))
print("Five: " + str(findStraightFlush(WHEEL_FL)))
