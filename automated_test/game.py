from pprint import pprint
from game import game_columns as game_logic
from make_game_test import show_test
from game import card
import numpy as np
import yaml
import cv2
from automated_test import image_generation as ig


# Global configuration for file
cfg_path = "config/cfg.yml"
config = yaml.safe_load(open(cfg_path))
config = config['auto_test']
card_path = config['card_positions']['path']
save_folder = config['save_folder']


class game:
    def __init__(self):
        self.game_data = game_logic.GameColumns()
        self.card_image_paths = {
            'Clubs': [f'{card_path}Clubs/{i}.png' for i in range(1, 14)],
            'Diamonds': [f'{card_path}Diamonds/{i}.png' for i in range(1, 14)],
            'Hearts': [f'{card_path}Hearts/{i}.png' for i in range(1, 14)],
            'Spades': [f'{card_path}Spades/{i}.png' for i in range(1, 14)],
            'Back': f'{card_path}0.png'
        }
        self.current_stage = 0

        self.deck_class = card.Deck()

        self.deck = self.deck_class.make_deck()
        self.deck = self.deck_class.shuffle(self.deck)

        self.face_down = []

        # Creating the game in the 2D array
        for col in range(7):
            for row in range(7):
                if row == col:
                    self.game_data.solitaire[col, row] = self.deck.pop(0)
                elif row < col:
                    m_card = None
                    self.game_data.solitaire[col, row] = m_card
                    self.face_down.append(self.deck.pop(0))

    def test(self):
        generator = ig.image_generation()
        temp_card = self.deck.pop(0)
        self.game_data.solitaire[0, self.game_data.get_pile_size_in_col(
            0)] = temp_card
        talon = self.deck.pop(0)
        generator.generate_image(game_data=self.game_data, stage=self.current_stage, talon=talon)
        self.current_stage += 1
