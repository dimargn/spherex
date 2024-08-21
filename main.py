import argparse

from wheel_of_fortune import WheelOfFortune

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Word guessing game")
    parser.add_argument('--word_file', type=str)
    parser.add_argument('--limit', type=int, default=None)
    parser.add_argument('--players', type=int,  default=2)
    parser.add_argument('--names', type=str, nargs='+', required=True)
    args = parser.parse_args()

    game = WheelOfFortune(args.word_file, args.limit, args.players, args.names)
    game.play_game()



