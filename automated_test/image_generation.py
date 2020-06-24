from PIL import Image, ImageDraw
import numpy as np
import cv2
from automated_test import general_funcs as gf
import yaml

# Global configuration for file
cfg_path = "config/cfg.yml"
config = yaml.safe_load(open(cfg_path))
config = config['auto_test']
card_path = config['card_positions']['path']
save_folder = config['save_folder']


class image_generation():
    def __init__(self):
        self.card_images = {
            'Clubs': [Image.open(f'{card_path}Clubs/{i}.png') for i in range(1, 14)],
            'Diamonds': [Image.open(f'{card_path}Diamonds/{i}.png') for i in range(1, 14)],
            'Hearts': [Image.open(f'{card_path}Hearts/{i}.png') for i in range(1, 14)],
            'Spades': [Image.open(f'{card_path}Spades/{i}.png') for i in range(1, 14)],
            'Back': Image.open(f'{card_path}0.png'),
            'Blank': Image.open(f'{card_path}blank.png')
        }

    def generate_card(self, card, card_img_size):
        # Check if the card is face-down or face-up
        if card == 'Blank':
            card_img = self.card_images['Blank']
        elif card is None or card.is_facedown:  # Card is face-down
            card_img = self.card_images['Back']
        else:  # Card is face-up
            suit = gf.get_full_suit_name(card.suit)
            number = card.number
            card_img = self.card_images[suit][number - 1]

        # Resize the image using the aspect ratio further up
        card_img = card_img.resize(card_img_size, Image.ANTIALIAS)
        return card_img

    def generate_image(self, game_data, talon, stage=0, background_color=20):
        card_img_aspect = 0.5
        card_img_size = (np.round(232 * card_img_aspect).astype(int),
                         np.round(360 * card_img_aspect).astype(int))
        x_margin = np.round(40 * card_img_aspect).astype(int)
        y_margin = np.round(84 * card_img_aspect).astype(int)
        border_margin = np.round(90 * card_img_aspect).astype(int)
        foundation_x_start = np.round(908 * card_img_aspect).astype(int)

        # Current stage - What stage number this is
        img_path = f'{save_folder}/{stage}.jpg'

        # Define a numpy array with all 0's
        width = border_margin * 2 + 7 * card_img_size[0] + 6 * x_margin
        background_img = np.zeros([1000, width, 3], dtype=np.uint8)

        # Fill the image with a defined color
        background_img.fill(background_color)

        # Save the image
        cv2.imwrite(img_path, background_img)

        # Open the image with PIL
        generated_img = Image.open(img_path)

        # Make pile
        card_img = self.generate_card(None, card_img_size)
        x_pos = border_margin
        y_pos = border_margin
        card_pos = (x_pos, y_pos)
        generated_img.paste(card_img, card_pos, mask=card_img)

        # Make talon
        cur_card = talon.waste
        card_img = self.generate_card(cur_card, card_img_size)
        x_pos = border_margin + card_img_size[0] + x_margin
        y_pos = border_margin
        card_pos = (x_pos, y_pos)
        generated_img.paste(card_img, card_pos, mask=card_img)

        # Make foundations
        for n, suit in enumerate(['C', 'D', 'H', 'S']):
            cur_card = game_data.m_suit_pile.get_card(suit)
            if cur_card is None:
                cur_card = 'Blank'
            card_img = self.generate_card(cur_card, card_img_size)

            x_pos = n * (card_img_size[0] + x_margin) + foundation_x_start
            y_pos = border_margin
            card_pos = (x_pos, y_pos)

            generated_img.paste(card_img, card_pos, mask=card_img)

        # Loop through all rows
        for row in range(19):
            value = None

            # Loop through all columns
            for col in range(7):
                cur_card = game_data.solitaire[col, row]
                if cur_card != 0:  # Check if 0, because it's a numpy zero-array
                    value = 1
                    # Resize the image using the aspect ratio further up
                    card_img = self.generate_card(cur_card, card_img_size)

                    # Get the position of the card using x and y coordinates
                    x_pos = col * (card_img_size[0] + x_margin) + border_margin
                    y_pos = row * y_margin + card_img_size[1] + border_margin * 2
                    card_pos = (x_pos, y_pos)

                    # Paste the card on the image
                    generated_img.paste(card_img, card_pos, mask=card_img)
                elif cur_card == 0 and row == 0:
                    # Resize the image using the aspect ratio further up
                    card_img = self.generate_card('Blank', card_img_size)

                    # Get the position of the card using x and y coordinates
                    x_pos = col * (card_img_size[0] + x_margin) + border_margin
                    y_pos = row * y_margin + card_img_size[1] + border_margin * 2
                    card_pos = (x_pos, y_pos)

                    # Paste the card on the image
                    generated_img.paste(card_img, card_pos, mask=card_img)

            # If no card was found, break the loop
            if not value:
                break

        # Save, load, and show image
        generated_img.save(img_path, quality=100)
        temp_img = cv2.imread(img_path)
        cv2.imshow("hej", temp_img)
        cv2.waitKey(1)

        # card = self.card_images['Back']
        # card = card.resize(card_img_size, Image.ANTIALIAS)
        # generated_img.paste(card, (100, 150), mask=card)
        # generated_img.save(img_path, quality=95)
        # imgg = cv2.imread(img_path)
        # cv2.imshow("hej", imgg)
        # cv2.waitKey()
