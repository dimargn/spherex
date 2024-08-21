from abc import ABC, abstractmethod


class Game(ABC):

    @abstractmethod
    def play_game(self):
        pass