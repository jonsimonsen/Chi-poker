import random
from hands.constants import *

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
        while(i < 13 and hand[i] < suit * 13 ):
            suits[suit - 1] += 1 << (hand[i] % 13)
            i += 1
        fixLengthBits(suits, suit - 1)
        suit += 1
    
    suits.sort(reverse=True)
    return suits

# Create an int to encode the length of a suit as its most significant bits (for adding to the suit int)
# Returns nothing, but alters the hand accordingly
def fixLengthBits(hand, suit):
    if hand[suit] > MAX_CARDBITS:
        #Strip lenght bits
        bits = bin(hand[suit])[-13:]
    else:
        #Strip 0b
        bits = bin(hand[suit])[2:]
    cards = int(bits, 2)

    # Python switch/case
    match cards.bit_count():
        case 0:
            hand[suit] = cards
        case 1 | 2 | 3:
            hand[suit] = cards + (0b1 << 13)
        case 4:
            hand[suit] = cards + (0b1 << 14)
        case 5:
            hand[suit] = cards + (0b11 << 13)
        case 6:
            hand[suit] = cards + (0b1 << 15)
        case 7:
            hand[suit] = cards + (0b101 << 13)
        case 8:
            hand[suit] = cards + (0b11 << 14)
        case _:
            hand[suit] = cards + (0b111 << 13)
    return

# Track duplicate values
def findDuplicates(hand):
    duplicates = []
    for i in reversed(range(13)):
        count = 0
        for suit in hand:
            if suit & (1 << i):
                count += 1
        duplicates.append(count)
    return duplicates
    
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

# Find straight flush.
# Returns None if not found. Otherwise, returns a number corresponding to the strength
def findStraightFlush(hand):
    for suit in range(2):
        if hand[suit] < (0b11 << 13):
            return None
        else:
            #Check for ordinary straight
            bitmask = 0b11111
            for i in reversed(range(9)):
                if (hand[suit] & (bitmask << i)) == (bitmask << i):
                    print("spre: " + str(hand[suit]))
                    hand[suit] = hand[suit] ^ (bitmask << i)
                    fixLengthBits(hand, suit)
                    print("spost: " + str(hand[suit]))
                    hand.sort(reverse=True)
                    return 8 - i
            # Check for wheel
            bitmask = 0b1111
            if (hand[suit] & bitmask) == bitmask:
                if hand[suit] & (1 << 12):
                    print("wpre: " + str(hand[suit]))
                    hand[suit] = hand[suit] ^ 0b1000000001111
                    fixLengthBits(hand, suit)
                    print("wpost: " +str(hand[suit]))
                    hand.sort(reverse=True)
                    return 9

    return None

# Find quads
def findQuads(hand, duplicates):
    if 4 in duplicates:
        i = duplicates.index(4)
        print("index: " + str(i))
        for suit in range(4):
            print(hand[suit])
            removeCard(hand, suit, 12 - i)
            print(hand[suit])
            fixLengthBits(hand, suit)
            duplicates[i] = 0
        return i + START_QUADS
    else:
        return None
    
# Find full house
def findFullHouse(hand, duplicates, lock=False):
    target = 2
    if 3 in duplicates: # Do we need to consider 4 as well? Should revisit this later
        i = duplicates.index(3)
        print("index: " + str(i))
        if lock:
            target = 3
        if duplicates.count(3) + duplicates.count(2) >= target:
            for suit in range(4):
                print(hand[suit])
                removeCard(hand, suit, 12 - i)
                print(hand[suit])
                fixLengthBits(hand, suit)
                duplicates[i] = 0
            hand.sort(reverse=True)
            return i + START_FH
    return None

# Find straight.
def findStraight(hand):
        #Needs implementation
        return None

# Remove a card from a suit
def removeCard(hand, suit, value):
    # https://stackoverflow.com/questions/12173774/how-to-modify-bits-in-an-integer/12174125#12174125
    hand[suit] &= ~ (1 << value)