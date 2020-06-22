import yaml
from automated_test import game as game_test


if __name__ == '__main__':
    game = game_test.game()
    # game.generate_image()
    game.test()
