import random

from game import Game


class WheelOfFortune(Game):

    def __init__(self, word_file, limit, num_of_players, names):
        self.words = self.load_words(word_file, limit)
        self.scores = [0] * num_of_players
        self.players = names

    def load_words(self, file_path: str, limit: int = None) -> list[str]:
        with open(file_path, 'r') as f:
            words = [line.strip() for line in f.readlines()]
        if limit:
            words = words[:limit]
        random.shuffle(words)
        return words

    @staticmethod
    def display_word(word: str, guessed_letters: str) -> str:
        return ''.join([letter if letter in guessed_letters else '-' for letter in word])

    def get_player_guess(self, guessed_letters: list[str]):
        guess = input("Enter a letter or the full word: ").lower()
        if len(guess) == 1 and guess in guessed_letters:
            print(f"Letter '{guess}' already guessed. Try again.")
            return None
        return guess

    def handle_correct_guess(self, word: str, guess: str, guessed_letters: set, correct_letters: set, current_player: int):
        occurrences = word.count(guess)
        correct_letters.add(guess)
        self.scores[current_player] += occurrences
        guessed_letters.add(guess)
        print(f"Correct! {guess} occurs {occurrences} times.")

    def handle_full_word_guess(self, word: str, guess: str, correct_letters: set, current_player: int) -> bool:
        if guess == word:
            missing_letters = set(word) - correct_letters
            self.scores[current_player] += len(missing_letters)
            correct_letters.update(missing_letters)
            print(f"Correct! You guessed the whole word: {word}")
            return True
        else:
            print(f"Incorrect guess for the whole word.")
            return False

    def play_turn(self, word: str, guessed_letters: set, correct_letters: set, current_player: int) -> bool:
        print(f"***************************************************")
        print(f"Word: {self.display_word(word, guessed_letters)}")
        print(f"Guessed letters: {', '.join(sorted(guessed_letters))}")
        print(f"{self.players[current_player]}'s turn:")
        guess = self.get_player_guess(guessed_letters)

        if not guess:
            return True
        if len(guess) == 1:
            if guess in set(word):
                self.handle_correct_guess(word, guess, guessed_letters, correct_letters, current_player)
                return True
            else:
                guessed_letters.add(guess)
                print(f"Wrong guess.")
                return False
        else:
            if self.handle_full_word_guess(word, guess, correct_letters, current_player):
                return False
            return False

    def play_round(self, word: str):
        guessed_letters = set()
        correct_letters = set()
        current_player = 0

        while set(word) != correct_letters:
            if not self.play_turn(word, guessed_letters, correct_letters, current_player):
                current_player = (current_player + 1) % len(self.players)
            print(f"Scores: {', '.join([f'{self.players[i]}: {self.scores[i]}' for i in range(len(self.players))])}")

        print(f"Word guessed! The word was: {word}")

    def play_game(self):
        for word in self.words:
            self.play_round(word.lower())
        print("Game over!")
        print(f"Final Scores: {', '.join([f'{self.players[i]}: {self.scores[i]}' for i in range(len(self.players))])}")
        winner = max(self.scores)
        winners = [self.players[i] for i in range(len(self.players)) if self.scores[i] == winner]
        if len(winners) > 1:
            print(f"It's a tie between: {', '.join(winners)}!")
        else:
            print(f"{winners[0]} wins!")
