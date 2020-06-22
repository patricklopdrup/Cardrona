from pprint import pprint
from game import game_columns as game_logic
from make_game_test import show_test
from game import card
import numpy as np
import yaml
import cv2
from PIL import Image, ImageDraw

# Global configuration for file
cfg_path = "config/cfg.yml"
config = yaml.safe_load(open(cfg_path))
config = config['auto_test']
card_path = config['card_positions']['path']
save_folder = config['save_folder']


class game:
    def __init__(self):
        self.game_data = game_logic.GameColumns()
        self.card_images = {
            'Clubs': [f'{card_path}Clubs/{i}.png' for i in range(1, 14)],
            'Diamonds': [f'{card_path}Diamonds/{i}.png' for i in range(1, 14)],
            'Hearts': [f'{card_path}Hearts/{i}.png' for i in range(1, 14)],
            'Spades': [f'{card_path}Spades/{i}.png' for i in range(1, 14)]
        }
        self.current_stage = 0

        self.deck = card.Deck()

        m_deck = self.deck.make_deck()
        m_deck = self.deck.shuffle(m_deck)

        for m_card in m_deck:
            print(m_card, end=", ")
        print()

        # Creating the game in the 2D array
        for col in range(7):
            for row in range(7):
                if row == col:
                    self.game_data.solitaire[col, row] = m_deck.pop(0)
                elif row < col:
                    m_card = None
                    self.game_data.solitaire[col, row] = m_card

    def generate_image(self, background_color=20):
        self.current_stage += 1
        img_path = f'{save_folder}/{self.current_stage}.jpg'
        img = np.zeros([1000, 2000, 3], dtype=np.uint8)
        img.fill(background_color)
        cv2.imwrite(img_path, img)
        imgg = Image.open(img_path)
        card = Image.open(self.card_images['Clubs'][0])
        imgg.paste(card, (100, 150), mask=card)
        imgg.save(img_path, quality=95)
        imgg = cv2.imread(img_path)
        cv2.imshow("hej", imgg)
        cv2.waitKey()

    def test(self):
        self.game_data.col_facedown
