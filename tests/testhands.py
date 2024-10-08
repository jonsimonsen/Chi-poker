"""Constants for test hands."""

# Example suits
NO_HAND = 0
ONE_CARD = 0b10000001000000
TWO_CARDS = 0b10000010100000
TWO_CARDS_V2 = 0b10000000101000
TWO_CARDS_V3 = 0b10001000000100
THREE_CARDS = 0b11000001000001
THREE_CARDS_V2 = 0b11100000000010
THREE_CARDS_V3 = 0b10100000000011
FOUR_CARDS = 0b101000100010001
FIVE_CARDS = 0b111010001000101

# Straight flush hands
A_SFL = [0b1001111100000100, FOUR_CARDS, TWO_CARDS, ONE_CARD]
T_SFL = [0b1001000111110000, FOUR_CARDS, TWO_CARDS, ONE_CARD]
SIX_SFL = [0b1000000100011111, FOUR_CARDS, THREE_CARDS, NO_HAND]
WHEEL_FL = [0b1001000100001111, FOUR_CARDS, THREE_CARDS, NO_HAND]
A_SFL6 = [0b1001111110000000, FOUR_CARDS, TWO_CARDS, ONE_CARD]
WHEEL_FL6 = [0b1001000000011111, FOUR_CARDS, THREE_CARDS, NO_HAND]
SFL_H2 = [FIVE_CARDS, 0b110000111110000, TWO_CARDS, ONE_CARD]
WHEEL_FLH2 = [FIVE_CARDS, 0b111000000001111, THREE_CARDS, NO_HAND]

# Quad hands
QUAD_A = [FOUR_CARDS, THREE_CARDS_V2, THREE_CARDS_V2, THREE_CARDS]
QUAD_2 = [FOUR_CARDS, THREE_CARDS_V3, THREE_CARDS_V3, THREE_CARDS]

# Busts
BUST_553 = [FIVE_CARDS, FIVE_CARDS, THREE_CARDS, NO_HAND]
BUST_544 = [FIVE_CARDS, FOUR_CARDS, FOUR_CARDS, NO_HAND]

# Full houses

# Flushes
A_FLUSH = [FIVE_CARDS, FOUR_CARDS, TWO_CARDS, TWO_CARDS]

# Suit combos

# Flushing
SFL10_A_9 = 0b1111111111111000
SFL10_A_6 = 0b1111111100011111
SFL10_K_5 = 0b1111111110001111
SFL10_A_F = 0b1111111101100111
SFL10_5_F = 0b1111111011001111
FL10_A_8 =  0b1111111011110110
SFL7_K7 = 0b1010111111100000
SFL7_77 = 0b1011000000111111
SFL7_K5 = 0b1010111110101000
SFL7_55 = 0b1011010100001111
SFL6_A6 = 0b1001111110000000
SFL6_J6 = 0b1000001111110000
SFL6_66 = 0b1001000000011111
SFL6_A5 = 0b1001111101000000
SFL6_J5 = 0b1000001111101000
SFL6_55 = 0b1001010000001111
SFL5_A = 0b111111100000000
SFL5_6 = 0b110000000011111
SFL5_5 = 0b111000000001111