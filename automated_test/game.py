from pprint import pprint
import numpy as np
import yaml
import cv2

# Global configuration for file
cfg_path = "config/cfg.yml"
config = yaml.safe_load(open(cfg_path))
card_path = config['card_positions']['path']


class game:
    card_images = {
        'Clubs': [f'{card_path}Clubs/{i}.png' for i in range(1, 14)],
        'Diamonds': [f'{card_path}Diamonds/{i}.png' for i in range(1, 14)],
        'Hearts': [f'{card_path}Hearts/{i}.png' for i in range(1, 14)],
        'Spades': [f'{card_path}Spades/{i}.png' for i in range(1, 14)]
    }

    def generate_image(self, background_color=20):
        image = np.zeros([1000, 2000, 3], dtype=np.uint8)
        image.fill(background_color)
        cv2.imshow("hej", image)
        cv2.waitKey()
