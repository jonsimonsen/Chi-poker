import random

# Deal a 13 card hand for Chinese poker (cards represented as numbers from 0 to 51)
def dealHand():
    deck = list(range(52))
    hand = random.sample(deck, 13)
    hand.sort()
    return hand

# Encode a hand as 4 ints (one per suit) with the first three bits indicating the number of cards in the suit
def processHand(hand):
    spades = 0
    hearts = 1
    diamonds = 2
    clubs = 3

    i = 0
    suit = 1
    suits = [spades, hearts, diamonds, clubs]
    print(suits)

    while(suit < 5):
        count = 0
        while(i < 13 and hand[i] < suit * 13 ):
            print(hand[i] % 13)
            count += 1
            i += 1
        print("count: " + str(count))
        suit += 1

    return

# Print a hand showing cards in brackets for each suit
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
    return

# Test dealing a hand and printing it out
nuts = dealHand()
printHand(nuts)
processHand(nuts)
