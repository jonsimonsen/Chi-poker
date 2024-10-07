"""Constants for use in arranging and manipulating hands.

We might want to move some of these into other files later.
"""

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

MAX_CARDBITS = 8191

# Hand ranking constants

# Generic
PAIR_KICKERS = 220

# 2-flushes and other hands where you choose 2 cards
N_CHOOSE_2 = [1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66]

# 3-flushes
F3_12 = 165
F3_11 = 120
F3_10 = 84
F3_9 = 56
F3_8 = 35
F3_7 = 20
F3_6 = 10
F3_5 = 4
F3_4 = 1 # Ignoring this when counting since straight flushes are its own category
F3 = [F3_12, F3_11, F3_10, F3_9, F3_8, F3_7, F3_6, F3_5]

# Starting point of various hands in the rankings
START_SFL = 0
START_QUADS = 10
START_FH = 23
START_FL = 36
START_F_K = sum(F3) - 1 # 1 less since there are two straight flushes containing an ace
START_F_Q = START_F_K + sum(F3[1:])
START_F_J = START_F_Q + sum(F3[2:])
START_F_T = START_F_J + sum(F3[3:])
START_F_9 = START_F_T + sum(F3[4:])
START_F_8 = START_F_9 + sum(F3[5:])
START_F_7 = START_F_8 + sum(F3[6:])
START_FLUSHES = [0, START_F_K, START_F_Q, START_F_J, START_F_T, START_F_9, START_F_8, START_F_7]
START_STR = 1313
START_TRIPS = 1323
START_TWO_PAIR = 1336
START_PAIR = 2194
START_HI = 5054
END_HI = 6331
BREAKPOINTS_5_CARDS = [[0, "Straight flush"], [START_QUADS, "Quads"], [START_FH, "Full house"], [START_FL, "Flush"], [START_STR, "Straight"],
                       [START_TRIPS, "Trips"], [START_TWO_PAIR, "Two pairs"], [START_PAIR, "Pair"], [START_HI, "Hi card"]]

# Starting point of three card hands
START_3 = 6400
START_3_PAIR = 6413
START_3_HI = 6569
END_3_HI = 6855
BREAKPOINTS_3_CARDS = [[0, "Trips"], [(START_3_PAIR - START_3), "Pair"], [(START_3_HI - START_3), "Hi card"]]

# Mapping between function name and hand strength of the next hand category
FUNC_SFL = ["findStraightFlush", START_QUADS]
FUNC_QUADS = ["findQuads", START_FH]
FUNC_FH = ["findFullHouse", START_FL]
FUNC_FL = ["findFlush", START_STR]
FUNC_STR = ["findStraight", START_TRIPS]
FUNC_TRIPS = ["findTrips", START_TWO_PAIR]
FUNC_TWO_PAIR = ["findTwoPair", START_PAIR]
FUNC_PAIR = ["findPair", START_HI]
FUNC_HI = ["findHiCard", START_3]
FUNC_3TRIPS = ["findThreeCardTrips", START_3_PAIR]
FUNC_3PAIR = ["findThreeCardPair", START_3_HI]
FUNC_3HI = ["findThreeCardHi", END_3_HI]
FUNCS_5 = [FUNC_SFL, FUNC_QUADS, FUNC_FH, FUNC_FL, FUNC_STR, FUNC_TRIPS, FUNC_TWO_PAIR, FUNC_PAIR, FUNC_HI]
FUNCS_3 = [FUNC_3TRIPS, FUNC_3PAIR, FUNC_3HI]
