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
        self.startHand = hand
        self.board = [-1, -1, -1]
        self.bonus = 0
        self.locked_pairs = 0
        self.pair_count = -1
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

    def makeChart(self):
        """Prepare arrays for a hand ranking chart.

        Populate all spots in back, middle and front.
        """
        self.back = []
        for i in range(START_PAIR):
            self.back.append(0)
        self.middle = []
        for j in range(END_HI):
            self.middle.append(0)
        self.front = []
        for k in range(START_3, END_3_HI):
            self.front.append(0)

    def simulateHands(self, numHands):
        """Arrange numHands Chinese hands.
        
        
        """
        self.makeChart()
        hand = None

        # Arrange random hands
        for i in range(numHands):
            hand = processHand(dealHand())
            self.resetHand(hand)
            self.arrangeBoard()
            self.back[self.board[0]] += 1
            self.middle[self.board[1]] += 1
            self.front[self.board[2] - START_3] += 1

        with open('x_gen0_back.txt', 'w') as r_back, open('c_gen0_back.txt', 'w') as c_back:

            count = 0
            print("Back:\n", file=r_back)
            print("Back:\n", file=c_back)
            print(BREAKPOINTS_5_CARDS[0][1] + ":", file=r_back)
            print(BREAKPOINTS_5_CARDS[0][1] + ":", file=c_back)
            rank_index = 1
            back_next = BREAKPOINTS_5_CARDS[rank_index][0]
            for backHand in range(len(self.back)):
                if backHand == back_next:
                    print(BREAKPOINTS_5_CARDS[rank_index][1] + ":", file=r_back)
                    print(BREAKPOINTS_5_CARDS[rank_index][1] + ":", file=c_back)
                    rank_index += 1
                    if back_next < BREAKPOINTS_5_CARDS[-1][0]:
                        back_next = BREAKPOINTS_5_CARDS[rank_index][0]
                    else:
                        back_next = -1
                print(self.back[backHand], file=r_back)
                count += self.back[backHand]
                print(count, file=c_back)

        print("\nMiddle:\n")
        print(BREAKPOINTS_5_CARDS[0][1] + ":")
        rank_index = 1
        middle_next = BREAKPOINTS_5_CARDS[rank_index][0]
        for middleHand in range(len(self.middle)):
            if middleHand == middle_next:
                print(BREAKPOINTS_5_CARDS[rank_index][1] + ":")
                rank_index += 1
                if middle_next < BREAKPOINTS_5_CARDS[-1][0]:
                    middle_next = BREAKPOINTS_5_CARDS[rank_index][0]
                else:
                    middle_next = -1
            print(self.middle[middleHand])

        print("\nFront:\n")
        print(BREAKPOINTS_3_CARDS[0][1] + ":")
        rank_index = 1
        front_next = BREAKPOINTS_3_CARDS[rank_index][0]
        for frontHand in range(len(self.front)):
            if frontHand == front_next:
                print(BREAKPOINTS_3_CARDS[rank_index][1] + ":")
                rank_index += 1
                if front_next < BREAKPOINTS_3_CARDS[-1][0]:
                    front_next = BREAKPOINTS_3_CARDS[rank_index][0]
                else:
                    front_next = -1
            print(self.front[frontHand])
        print("\n")

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
                        self.bonus += 4
                        return 8 - i
                # Check for wheel
                bitmask = 0b1111
                if (self.suits[suit] & bitmask) == bitmask:
                    if self.suits[suit] & (1 << 12):
                        self.suits[suit] = self.suits[suit] ^ 0b1000000001111
                        fixLengthBits(self.suits, suit)
                        self.suits.sort(reverse=True)
                        self.bonus += 4
                        return 9
        return None
    
    def findQuads(self):
        """Return a number for the rank of the quads.

        Lower numbers mean a stronger hand.
        Return None if no quad hand is found.
        """
        self.ranks = findDuplicates(self.suits)
        if 4 in self.ranks:
            i = self.ranks.index(4)
            for suit in range(4):
                removeCard(self.suits, suit, 12 - i)
                fixLengthBits(self.suits, suit)
                self.ranks[i] = 0
            self.bonus += 3
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
                self.locked_pairs += 1
                if self.board[0] > -1:
                    self.bonus += 1
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
                flush.append(12 - i)
        
        # Make sure that there is no straight flush
        if flush[4] - flush[0] == 4:
            return None
        
        # Make sure that the flush does not contain a locked pair
        if self.locked_pairs > 0:
            lock = True
            low_pair = -1
            for i in reversed(range(13)):
                if self.ranks[i] > 1:
                    if (i) not in (flush[4::-1]):
                        lock = False
                        break
                    elif low_pair == -1:
                        low_pair = i

            if lock:
                flush.remove(low_pair)
                if len(flush) < 5:
                    return None

        # Find rank
        rank = rankHiCard(flush)

        # Remove flush cards
        if self.suits[suit] < (0b1 < 15):
            self.suits[suit] = 0
        else:
            for value in flush[:5]:
                removeCard(self.suits, suit, 12 - value)
            fixLengthBits(self.suits, suit)
        self.suits.sort(reverse=True)
        return START_FL + rank

    def findStraight(self):
        """Return a number for the rank of the straight.

        Lower numbers mean a stronger hand.
        Return None if no straight is found.
        """

        # Update duplicates
        if self.suits is not None:
            self.ranks = findDuplicates(self.suits)
            self.suits = None # Suits are no longer needed

        indices = [0, 3] # State if there are no Ts in the hand
        straight_found = False
        high_pair = -1

        # Search for straights containing a T
        if self.ranks[4] > 0:
            indices = self.findSequence(4, 0)
            if indices[1] == indices[0] + 4:
                if self.locked_pairs > 0:
                    for i in range(12, -1, -1):
                        if self.ranks[i] > 1:
                            if (i > indices[1]) or (i < indices[0]) or (self.ranks[i] > 2):
                                straight_found = True
                                break
                            else:
                                high_pair = i
                else:
                    straight_found = True

            # Do a new search if the found straight was not legal
            if (high_pair in range(0, 4)) and (not straight_found):
                indices = self.findSequence(4, high_pair + 1)
                if indices[1] == indices[0] + 4:
                    straight_found = True
        
        # Search for straights containing a 5
        if (self.ranks[9] > 0) and (not straight_found):
            min_index = 0
            if high_pair > 3:
                min_index = high_pair + 1
            else:
                min_index = indices[1] + 2
            indices = self.findSequence(9, min_index)
            if indices[1] == indices[0] + 4:
                if (indices[1] == 13) and (high_pair == 0):
                    for i in range(8, 0, -1):
                        if self.ranks[i] > 1:
                            straight_found = True
                elif (self.locked_pairs > 0 and high_pair == -1):
                    for i in range(12):
                        if self.ranks[i] > 1:
                            if (i < indices[0]) or (i > indices[1]) or (self.ranks[i] > 2):
                                if not (i == 0 and indices[1] == 13 and self.ranks[i] < 3):
                                    straight_found = True
                                    break
                            else:
                                high_pair = i
                else:
                    straight_found = True

            # Do a new search if the found straight was not legal
            if (high_pair in range(5, 9)) and (not straight_found):
                indices = self.findSequence(9, high_pair + 1)
                if indices[1] == indices[0] + 4:
                    straight_found = True

        if straight_found:
            for rank in range (indices[0], indices[1] + 1):
                if rank == 13:
                    self.ranks[0] -= 1
                else:
                    self.ranks[rank] -= 1
            return indices[0] + START_STR
        else:
            return None
        
    def findTrips(self):
        """Return a number for the rank of the trips.

        Lower numbers mean a stronger hand.
        Return None if no trip hand is found.
        """

        self.pair_count = getPairCount(self.ranks) - self.locked_pairs

        if self.pair_count == 0:
            return None

        if 3 in self.ranks:
            i = self.ranks.index(3)
            self.ranks[i] = 0
            self.pair_count -= 1
            return i + START_TRIPS
        else:
            return None

    def findTwoPair(self):
        """Return a number for the rank of the two pair.

        Lower numbers mean a stronger hand.
        Return None if no two pair hand is found.
        """
        if self.pair_count < 2:
            return None
        
        first_pair = -1
        second_pair = -1
        rank = 0
        kicker = 14 #Ensure that a pair is used when all cards are paired

        first_pair = self.ranks.index(2)
        self.ranks[first_pair] = 0
        second_pair = self.ranks.index(2)
        self.ranks[second_pair] = 0
        self.pair_count -= 2

        if(1 in self.ranks):
            kicker = self.ranks.index(1)
        if (kicker > second_pair + 1) and (self.pair_count > 0):
            candidate = self.ranks.index(2)
            if candidate < kicker:
                kicker = candidate
                self.pair_count -= 1
        self.ranks[kicker] -= 1

        # Calculate hand rank
        for i in range(first_pair):
            rank += 12 - i
        rank += second_pair - first_pair - 1

        #Justify for kickers
        rank = rank * 11 + kicker
        if kicker > second_pair:
            rank -= 2
        elif kicker > first_pair:
            rank -= 1

        return START_TWO_PAIR + rank
    
    def findPair(self):
        """Return a number for the rank of the pair.

        Lower numbers mean a stronger hand.
        Return None if no pair hand is found.
        """
        if self.pair_count < 1:
            return None
        
        pair = self.ranks.index(2)
        self.ranks[pair] = 0
        self.pair_count -= 1
        kickers = []
        rank = 0

        while len(kickers) < 3:
            index = self.ranks.index(1)
            self.ranks[index] = 0
            if index > pair:
                index -= 1
            kickers.append(index)

        rank += pair * PAIR_KICKERS
        for i in range(10 - kickers[0], 10):
            if i < 1:
                print("Error. Unexpected kicker index.")
                break
            rank += N_CHOOSE_2[i]
        for j in range(kickers[0] + 1, kickers[1]):
            rank += 11 - j
        rank += kickers[2] - kickers[1] - 1

        return START_PAIR + rank
    
    def findHiCard(self):
        """Return a number for the rank of the high card hand.
        
        Lower numbers mean a stronger hand.
        """
        
        if self.locked_pairs > 0: # Locked pairs are now irrelevant
            if 3 in self.ranks:
                self.ranks[self.ranks.index(3)] = 1
            if 2 in self.ranks:
                self.ranks[self.ranks.index(2)] = 0
            self.locked_pairs = 0

        hi_cards = []
        for i in range(5):
            card = self.ranks.index(1)
            hi_cards.append(card)
            self.ranks[card] = 0

        rank = rankHiCard(hi_cards)
        return START_HI + rank
    
    def findThreeCardTrips(self):
        """Return the rank of the trips.
        
        Return None if there are no trips or trips are illegal
        """
        # Update duplicates
        if self.suits is not None:
            self.ranks = findDuplicates(self.suits)
            self.suits = None # Suits are no longer needed
            
        self.pair_count = getPairCount(self.ranks) - self.locked_pairs
        if self.board[1] >= START_TWO_PAIR or self.pair_count == 0:
            return None
        
        if 3 in self.ranks:
            self.bonus += 2
            return START_3 + self.ranks.index(3)
        else:
            return None
        
    def findThreeCardPair(self):
        """Return the rank of the pair.
        
        Return None if there is no pair or a pair is illegal"""
        if self.pair_count == 0:
            return None
        
        pair = self.ranks.index(2)
        self.ranks[pair] = 0
        self.pair_count -= 1
        kicker = 99
        pair_kicker = 99
        trip_kicker = 99

        if 1 in self.ranks:
            kicker = self.ranks.index(1)

        if self.pair_count > 1 and (2 in self.ranks):
            pair_kicker = self.ranks.index(2)
        if 3 in self.ranks:
            trip_kicker = self.ranks.index(3)
        kicker = min(kicker, pair_kicker, trip_kicker)

        if pair < kicker:
            kicker -= 1

        return START_3_PAIR + (pair * 12) + kicker
    
    def findThreeCardHi(self):
        """Return the rank of the hi card hand."""

        #Remove all locked pairs from ranks
        for i in range(len(self.ranks)):
            if self.ranks[i] > 1:
                self.ranks[i] -= 2
        

        hi = self.ranks.index(1)
        self.ranks[hi] = 0
        middle = self.ranks.index(1)
        self.ranks[middle] = 0
        try:
            low = self.ranks.index(1)
        except Exception:
            print(self.ranks)
            printHand(self.startHand)

        rank = 0

        for i in range(11 - hi, 11):
            rank += N_CHOOSE_2[i]
        for j in range(hi + 1, middle):
            rank += 12 - j
        rank += low - middle - 1

        return START_3_HI + rank

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
            if j == 13:
                if self.ranks[0] == 0:
                    high_index = j - 1
            elif self.ranks[j] == 0:
                high_index = j - 1
                break
        if high_index == 0:
            high_index = low_index + 4

        return [low_index, high_index]
