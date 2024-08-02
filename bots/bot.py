# Class for Chinese poker bot
from abc import ABC, abstractmethod

class Bot(ABC):
    def __init__(self, hand):
        self.hand = hand
        self.board = [-1, -1, -1]
        self.locked_pairs = 0

    # Use a bot-specific algorithm to build a board from the hand of the bot
    @abstractmethod
    def arrangeBoard(self):
        pass

    # Base methods for finding various poker hands

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

    # Find flush
    def findFlush(hand):
        if hand[0] < (0b11 << 13):
            return None
        
        suit = 0
        # Check if the second suit has a higher flush than the first
        if hand[1] > (0b11 << 13) and hand[0] > (0b1 < 15):
            if (hand[1] % 8192) > (hand[0] % 8192):
                suit = 1

        # Collect cards for the highest possible flush
        flush = []
        for i in reversed(range(13)):
            if hand[suit] & 1 << i:
                flush.append(i)
        print(flush)
        
        # Make sure that there is no straight flush
        if flush[0] - flush[4] == 4:
            return None

        #Find rank
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


    # Find straight.
    def findStraight(hand):
            #Needs implementation
            return None
