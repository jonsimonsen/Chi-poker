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
        self.hand = hand
        self.board = [-1, -1, -1]
        self.locked_pairs = 0
        self.duplicates = []

    
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
            if self.hand[suit] < (0b11 << 13):
                return None
            else:
                #Check for ordinary straight
                bitmask = 0b11111
                for i in reversed(range(9)):
                    if (self.hand[suit] & (bitmask << i)) == (bitmask << i):
                        self.hand[suit] = self.hand[suit] ^ (bitmask << i)
                        fixLengthBits(self.hand, suit)
                        self.hand.sort(reverse=True)
                        return 8 - i
                # Check for wheel
                bitmask = 0b1111
                if (self.hand[suit] & bitmask) == bitmask:
                    if self.hand[suit] & (1 << 12):
                        self.hand[suit] = self.hand[suit] ^ 0b1000000001111
                        fixLengthBits(self.hand, suit)
                        self.hand.sort(reverse=True)
                        return 9

        return None
    
    def findQuads(self):
        """Return a number for the rank of the quads.

        Lower numbers mean a stronger hand.
        Return None if no quad hand is found.
        """
        if 4 in self.duplicates:
            i = self.duplicates.index(4)
            for suit in range(4):
                removeCard(self.hand, suit, 12 - i)
                fixLengthBits(self.hand, suit)
                self.duplicates[i] = 0
            return i + START_QUADS
        else:
            return None
    
    def findFullHouse(self):
        """Return a number for the rank of the full house.

        Lower numbers mean a stronger hand.
        Return None if no full house is found.
        """
        target = 2
        if 3 in self.duplicates: # Do we need to consider 4 as well? Should revisit this later
            i = self.duplicates.index(3)
            if self.locked_pairs > 0:
                target = 3
            if self.duplicates.count(3) + self.duplicates.count(2) >= target:
                for suit in range(4):
                    removeCard(self.hand, suit, 12 - i)
                    fixLengthBits(self.hand, suit)
                    self.duplicates[i] = 0
                self.hand.sort(reverse=True)
                printHand(self.hand)
                return i + START_FH
        return None

    def findFlush(self):
        """Return a number for the rank of the flush.

        Lower numbers mean a stronger hand.
        Return None if no flush is found or a straight flush is found.
        """

        if self.hand[0] < (0b11 << 13):
            return None
        
        suit = 0
        # Check if the second suit has a higher flush than the first
        if self.hand[1] > (0b11 << 13) and self.hand[0] > (0b1 < 15):
            if (self.hand[1] % 8192) > (self.hand[0] % 8192):
                suit = 1

        # Collect cards for the highest possible flush
        flush = []
        for i in reversed(range(13)):
            if self.hand[suit] & 1 << i:
                flush.append(i)
        print(flush)
        print(self.duplicates)
        
        # Make sure that there is no straight flush
        if flush[0] - flush[4] == 4:
            return None
        
        # Make sure that the flush does not contain a locked pair
        if self.locked_pairs > 0:
            lock = True
            low_pair = -1
            for i in range(13):
                if (list(reversed(self.duplicates))[i] > 1):
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
        if self.hand[suit] < (0b1 < 15):
            self.hand[suit] = 0
        else:
            for value in flush[:5]:
                removeCard(self.hand, suit, value)
            fixLengthBits(self.hand, suit)
        return rank

    def findStraight(self):
        """Return a number for the rank of the straight.

        Lower numbers mean a stronger hand.
        Return None if no straight is found.
        """

        #Update duplicates
        self.duplicates = findDuplicates(self.hand)

        upper_bound = 0
        lower_bound = 0

        #Search for straights containing a T
        if self.duplicates[4] > 0:
            for i in range(4, 0, -1):
                if self.duplicates[i] == 0:
                    upper_bound = i + 1
                    break
            for j in range(5, upper_bound + 5):
                if self.duplicates[j] == 0:
                    lower_bound = j - 1
                    break
            if lower_bound == 0:
                lower_bound = upper_bound + 4

        print("upper: " + str(upper_bound) + " , lower: " + str(lower_bound))

        return None
