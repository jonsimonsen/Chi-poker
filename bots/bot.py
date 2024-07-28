# Class for Chinese poker bot
from abc import ABC, abstractmethod

class Bot(ABC):
    def __init__(self, hand):
        self.hand = hand
        self.board = [-1, -1, -1]

    # Use a bot-specific algorithm to build a board from the hand of the bot
    @abstractmethod
    def arrangeBoard(self):
        pass
