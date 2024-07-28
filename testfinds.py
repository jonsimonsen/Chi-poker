from dealhand import *

# Test specific SFL hands
print("Ace: " + str(findStraightFlush(A_SFL)))
print("Ten: " + str(findStraightFlush(T_SFL)))
print("Six: " + str(findStraightFlush(SIX_SFL)))
print("Five: " + str(findStraightFlush(WHEEL_FL)))
print("Others:")
print("Ace: " + str(findStraightFlush(A_SFL6)))
print("Six: " + str(findStraightFlush(WHEEL_FL6)))
print("Ten (2nd): " + str(findStraightFlush(SFL_H2)))
print("Wheel (2nd): " + str(findStraightFlush(WHEEL_FLH2)))

# Test busted SFL hands
print("Balanced: " + str(findStraightFlush(QUAD_A)))
print("No SFL: " + str(findStraightFlush(BUST_544)))
print("Distribution: " + str(findStraightFlush(BUST_553)))

# Test specific Quad hands
counts = findDuplicates(QUAD_A)
rank = findQuads(counts)
print("Quad A: " + str(rank))
counts = findDuplicates(QUAD_2)
rank = findQuads(counts)
print("Quad 2: " + str(rank))
