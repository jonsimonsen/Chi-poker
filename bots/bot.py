"""A parent class for Chinese poker bots.

The class defines variables shared by all bots.
arrangeBoard() is an abstract method for arranging the hands.
Methods to find poker hands can be used or overwritten by children.
"""

from abc import ABC, abstractmethod
from hands.dealhand import *

class Bot(ABC):
    """Class for a Chinese poker bot."""
    def __init__(self, hand):
        self.suits = hand
        self.board = [-1, -1, -1]
        self.locked_pairs = 0
        self.ranks = []

    
    @abstractmethod
    def arrangeBoard(self):
        # Build a board from the hand of the bot
        # Override the method for all child classes
        pass

    def resetHand(self, hand):
        """Reset all variables on an existing bot object.
        
        Call __init__ with the given hand.
        """
        self.__init__(hand)

    # Base methods for finding various poker hands

    def findStraightFlush(self):
        """Return a number for the rank of the straight flush.

        Lower numbers mean a stronger hand.
        Return None if no straight flush is found.
        """
        for suit in range(2):
            if self.suits[suit] < (0b11 << 13):
                return None
            else:
                #Check for ordinary straight
                bitmask = 0b11111
                for i in reversed(range(9)):
                    if (self.suits[suit] & (bitmask << i)) == (bitmask << i):
                        self.suits[suit] = self.suits[suit] ^ (bitmask << i)
                        fixLengthBits(self.suits, suit)
                        self.suits.sort(reverse=True)
                        return 8 - i
                # Check for wheel
                bitmask = 0b1111
                if (self.suits[suit] & bitmask) == bitmask:
                    if self.suits[suit] & (1 << 12):
                        self.suits[suit] = self.suits[suit] ^ 0b1000000001111
                        fixLengthBits(self.suits, suit)
                        self.suits.sort(reverse=True)
                        return 9

        return None
    
    def findQuads(self):
        """Return a number for the rank of the quads.

        Lower numbers mean a stronger hand.
        Return None if no quad hand is found.
        """
        if 4 in self.ranks:
            i = self.ranks.index(4)
            for suit in range(4):
                removeCard(self.suits, suit, 12 - i)
                fixLengthBits(self.suits, suit)
                self.ranks[i] = 0
            return i + START_QUADS
        else:
            return None
    
    def findFullHouse(self):
        """Return a number for the rank of the full house.

        Lower numbers mean a stronger hand.
        Return None if no full house is found.
        """
        target = 2
        if 3 in self.ranks: # Do we need to consider 4 as well? Should revisit this later
            i = self.ranks.index(3)
            if self.locked_pairs > 0:
                target = 3
            if self.ranks.count(3) + self.ranks.count(2) >= target:
                for suit in range(4):
                    removeCard(self.suits, suit, 12 - i)
                    fixLengthBits(self.suits, suit)
                    self.ranks[i] = 0
                self.suits.sort(reverse=True)
                printHand(self.suits)
                return i + START_FH
        return None

    def findFlush(self):
        """Return a number for the rank of the flush.

        Lower numbers mean a stronger hand.
        Return None if no flush is found or a straight flush is found.
        """

        if self.suits[0] < (0b11 << 13):
            return None
        
        suit = 0
        # Check if the second suit has a higher flush than the first
        if self.suits[1] > (0b11 << 13) and self.suits[0] > (0b1 < 15):
            if (self.suits[1] % 8192) > (self.suits[0] % 8192):
                suit = 1

        # Collect cards for the highest possible flush
        flush = []
        for i in reversed(range(13)):
            if self.suits[suit] & 1 << i:
                flush.append(i)
        print(flush)
        print(self.ranks)
        
        # Make sure that there is no straight flush
        if flush[0] - flush[4] == 4:
            return None
        
        # Make sure that the flush does not contain a locked pair
        if self.locked_pairs > 0:
            lock = True
            low_pair = -1
            for i in range(13):
                if (list(reversed(self.ranks))[i] > 1):
                    print(i)
                    if (i) not in (flush[4::-1]):
                        lock = False
                        break
                    elif low_pair == -1:
                        low_pair = i
            print(lock)
            print(low_pair)

            if lock:
                print("Fixing")
                flush.remove(low_pair)
                if len(flush) < 5:
                    return None

        # Find rank
        rank = START_FLUSHES[(12 - flush[0])] - 1
        print("Rank: " + str(rank))
        for i in range(flush[0] - 1, flush[1], -1):
            rank += F3[(11 - i)]
        print("Rank: " + str(rank))
        for i in range(flush[1] - 1, flush[2], -1):
            rank += F2[(10 - i)]
        print("Rank: " + str(rank))
        for i in range(flush[2] - 1, flush[3], -1):
            rank += i
        print("Rank: " + str(rank))
        rank += flush[3] - (flush[4] + 1)
        print("Rank: " + str(rank))

        # Remove flush cards
        if self.suits[suit] < (0b1 < 15):
            self.suits[suit] = 0
        else:
            for value in flush[:5]:
                removeCard(self.suits, suit, value)
            fixLengthBits(self.suits, suit)
        return rank

    def findStraight(self):
        """Return a number for the rank of the straight.

        Lower numbers mean a stronger hand.
        Return None if no straight is found.
        """

        # Update duplicates
        self.ranks = findDuplicates(self.suits)

        indices = [0, 3] # State if there are no Ts in the hand
        legal_straight = True
        high_pair = -1

        # Search for straights containing a T
        if self.ranks[4] > 0:
            indices = self.findSequence(4, 0)
            if indices[1] == indices[0] + 4:
                if self.locked_pairs > 0:
                    for i in range(12, -1, -1):
                        if self.ranks[i] > 1:
                            if i > indices[1]:
                                break
                            elif i < indices[0]:
                                legal_straight = True
                                break
                            else:
                                legal_straight = False
                                high_pair = i
                if legal_straight:
                    return indices[0]
                
            # Do a new search if the found straight was not legal
            if high_pair in range(0, 4):
                indices = self.findSequence(4, high_pair + 1)
                if indices[1] == indices[0] + 4:
                    return indices[0]
        
        # Search for straights containing a 5
        if self.ranks[9] > 0:
            min_index = 0
            if high_pair > 4:
                min_index = high_pair + 1
            else:
                min_index = indices[1] + 2
            indices = self.findSequence(9, min_index)
            if indices[1] == indices[0] + 4:
                if (indices[1] == 13) and (high_pair == 0):
                    for i in range(8, 0, -1):
                        if self.ranks[i] > 1:
                            return indices[0]
                else:
                    return indices[0]

        return None
    
    def findSequence(self, card_index, min_index):
        """Return the lowest and highest index in the sequence.
        
        card_index is the index of a card in the sequence.
        min_index is the minimum index in the sequence.
        the function is used to find straights.
        """
        low_index = min_index
        high_index = 0
        for i in range(card_index - 1, min_index - 1, -1):
            if self.ranks[i] == 0:
                low_index = i + 1
                break
        for j in range(card_index + 1, low_index + 5):
            # Check Ace as a one (for a wheel)
            if j == 14:
                if self.ranks[0] == 0:
                    high_index = j - 1
            elif self.ranks[j] == 0:
                high_index = j - 1
                break
        if high_index == 0:
            high_index = low_index + 4

        print("upper: " + str(low_index) + " , lower: " + str(high_index))
        return [low_index, high_index]
