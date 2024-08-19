# Chi-Poker

## Intro
The goal of the project is to create an AI for arranging Chinese Poker hands. It should not be perfected to such a degree that it would stand a chance against solid human opposition. It is hoped that the most advanced version would lose less than 0.1 bets per hand played against the best possible opposition.  

## Rules
It is assumed that the reader knows general rules for Chinese Poker. Some program specific rules need to be clarified.  

#### General Scoring
- Scooping wins 4 bets
- Winning 2 and tying 1 wins 3 bets
- Winning (2 of 3 hands) wins 2 bets
- Winning 1 and tying 2 wins 1 bet
- Folding loses 2 bets

There is no restriction against folding your hand  

#### Bonus Points
- 4 points for any straight flush
- 3 points for any quad hand
- 2 point for trips in the front
- 1 point for a full house in the middle

There are no other bonus points to be had. Note that if both players have bonus points, they apply for both even if one of the players has a weaker bonus hand (f.ex. straight flush vs. quads in the back wins 1 point in total).  

## Weaknesses
The plan is for the AI to optimalize their hands against a table of static hand values. This means that it does not take card removal into consideration. An example of a spot where it would be weak would be with a suit combination of 9-3-1-0. The best strategy here is presumably to take into account that the opposition is more likely to have flushes and generally stronger hands than average. This dictates a few adaptations.  

- Straights and weak flushes (especially in the back) are worth less than normal since the opposition is more likely to have strong flushes there  
- Very strong flushes and relatively weak full houses in the back are a bit stronger than normal since competent opposition is more likely to sacrifice the strength of their back for a stronger middle  
- Fold more liberally than normal since the opposition is more likely to have strong/playable hands (especially if you have a somewhat normal amount of rank duplication)  

## Plans
- Create a function for searching a chinese hand for various poker hands (straight flush, quads etc.).
- Create a function for rating a poker hand.
- Create a dumb AI that focuses on optimizing the back first and then the middle.

#### Poker hand ratings
5 card hands will be given an int value in [0, 17923]. If my calculations are correct, this should cover all different ranks of hands. Ranks of kickers are not take into account for quads, trips and full houses. For an improved AI, we might want to consider that f.ex. KKKKA is stronger than KKKKQ since it makes it impossible for someone to have stronger quads (but presumably there are better places to use an ace in that example).  

- Straight flushes [0, 9]  
- Quads [10, 22]  
- Full houses [23, 35]  
- Flushes [36, 1312]  
- Straights [1313, 1322]  
- Trips [1323, 1335]  
- Two pair [1336, 2193]  
- Pair [2194, 5053]  
- High card [5054, 17923]  

## Features
- Create hands by treating each suit as an int where each bit represents one rank. We might want to create a class for the hands later
- Enable printing processed hands in a manner that is easily readable. Uses a dict for mapping from bit position to card symbol.  
- Create bots that are able to arrange their starting hand into a board. So far it is only able to detect SFLs and quads.

## Versions
There will be no official version until a working dumb AI has been created.  

## AI Theory

#### Hand representation
Because the AI needs to be able to determine if the hand contains flushes, the hand will initially be represented with each suit recording what ranks are present in the suit (suit representation).  

When trying to find duplicated ranks (f.ex. quads), it would be quite an advantage if the hand is represented in a way that counts the number of cards for each rank (rank representation). It also turns out that this representation is easier to use for finding straights than the suit representation.  

We should be able to build a bot that finds an optimal solution by first populating the back hand (trying to make it as strong as possible). This means that if the algorithm has found a hand of a specific strength, it should never need to consider the possibility that it contains a stronger hand.    

With this principle in mind, we can conclude that the suit representation is no longer relevant when we're ready to search for straights. Anything from straights and down can therefore focus entirely on the rank representation of hands.  

If we later create an AI that tries to populate the front hand first, we might need to revise this principle.  

In the previous discussion, we've ignored the fact that constructing the best possible board is an iterative process. The way to deal with that should be to store the state of the hand before committing something to the board so we can go back to that state later to search for even better configurations. If we go back to a state where the suit representation is still relevant, it should work out fine since at that stage we've not started ignoring it yet.  
