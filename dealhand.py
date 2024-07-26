import random

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
            #print(hand[i] % 13)
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

# Test dealing a hand and printing it out
nuts = dealHand()
printCards(nuts)
nuts= processHand(nuts)
