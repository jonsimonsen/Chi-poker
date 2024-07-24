import random

def dealHand():
    deck = list(range(52))
    hand = random.sample(deck, 13)
    hand.sort()
    return hand

def printHand(hand):
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


# Use
printHand(dealHand())
