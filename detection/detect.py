import card_detection as detector
import image_processing as imgp
from pprint import pprint
from os import path


class detect:
    game_data = {}

    def load_state(self, img):
        if not path.exists(img):
            print("The specified image does not exist!")
            return

        self.game_data = imgp.get_game_state(img)

    def get_tableaus():
        print("All tableaus")

    def get_tableau():
        print("Single tableau")

    def get_foundations():
        print("Get foundations")

    def get_talon():
        print("Get talon")


if __name__ == '__main__':
    detection = detect()
    detection.load_state("img/test3.jpg")
