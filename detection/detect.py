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

    def get_tableaus(self):
        tableaus = []
        for tableau in self.game_data['tableaus']:
            cards = detector.get_cards_from_image(tableau['path'])
            tableaus.append(cards)

        return tableaus

    def get_tableau(self, tableau_num):
        tableau = self.game_data['tableaus'][tableau_num-1]
        cards = detector.get_cards_from_image(tableau['path'])
        return cards

    def get_foundations(self):
        foundations = []
        for foundation in self.game_data['foundations']:
            cards = detector.get_cards_from_image(foundation['path'])
            foundations.append(cards)

        return foundations

    def get_foundation(self, foundation_num):
        foundation = self.game_data['foundations'][foundation_num-1]
        cards = detector.get_cards_from_image(foundation['path'])
        return cards

    def get_talon(self):
        print("Get talon")


if __name__ == '__main__':
    detection = detect()
    detection.load_state("img/test3.jpg")
    print(detection.get_tableau(2))
