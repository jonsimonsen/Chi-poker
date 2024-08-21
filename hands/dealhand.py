"""Library of utility function for dealing with 13 card hands.

dealhand() deals a new random hand.
processhand() converts a dealt hand into the standard format.
fixLengthBits() adds bits for humber of cards in a suit.
findDuplicates() counts cards of each rank and returns them in a list.
printCards() prints the cards of an unprocessed hand.
printHand() prints the cards of a processed hand.
removeCard() removes a card of a specific rank from a suit.
"""

import random
from hands.constants import *

def dealHand():
    """Return a random unprocessed 13 card hand.
    
    Cards are represented as ints in [0, 51].
    """

    deck = list(range(52))
    hand = random.sample(deck, 13)
    hand.sort()
    return hand

def processHand(hand):
    """Return cards by suit.
    
    Convert an unprocessed hand into a standard format.
    Encode each suit as ints with the last bits for each card rank.
    Prepend length bits to the suits (see fiXLengthBits function).
    """

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

def fixLengthBits(hand, suit):
    """Return nothing. The function just alters the hand.
    
    Keep card bits unchanged.
    Set length bits of each suit to show number of set card bits.
    See match case clause for the categorization.
    """

    #Strip lenght bits
    if hand[suit] > MAX_CARDBITS:
        bits = bin(hand[suit])[-13:]
    else:
        bits = bin(hand[suit])[2:] #Strip 0b
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

def findDuplicates(hand):
    """Return a list of card duplications in the hand.
    
    The list is sorted by card rank descending.
    """

    duplicates = []
    for i in reversed(range(13)):
        count = 0
        for suit in hand:
            if suit & (1 << i):
                count += 1
        duplicates.append(count)
    return duplicates
    
def printCards(unprocessed_hand):
    """Print cards by suit for an unprocessed hand."""

    i = 0
    suit = 1
    cards = ""

    while(suit < 5):
        cards += "[ "
        while(i < 13 and unprocessed_hand[i] < suit * 13 ):
            cards += str(unprocessed_hand[i]) + " "
            i += 1
        suit += 1
        cards += "]"

    print(cards)
    return

def printHand(hand):
    """Print cards by suit for a processed hand."""
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

def removeCard(hand, suit, value):
    """Return none. The function just alters the hand.
    
    Remove a card from a suit.
    suit is the index of the suit we want to remove the card from.
    value is the rank of the card (A = 12, ... , 2 = 0)
    """

    # https://stackoverflow.com/questions/12173774/how-to-modify-bits-in-an-integer/12174125#12174125
    hand[suit] &= ~ (1 << value)

def rankHiCard(hand):
    """Return the rank of a high card hand.
    
    0 for the best (AKQJ9) down to
    1276 for the worst (75432)
    """