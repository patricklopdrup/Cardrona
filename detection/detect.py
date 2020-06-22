from . import card_detection as detector
from . import image_processing as imgp
from pprint import pprint
from os import path
from . import camera


class detect:
    game_data = {}
    cur_image_num = 0

    def take_picture(self):
        self.cur_image_num += 1
        camera.take_picture(self.cur_image_num)
        img_path = path.dirname(path.abspath(__file__)) + \
            f'/captures/picture_{self.cur_image_num}.jpg'
        self.load_state(img_path)
        return True

    def load_state(self, img):
        if not path.exists(img):
            print("The specified image does not exist!")
            return

        self.game_data = imgp.get_game_state(img)
        return True

    def get_tableaus(self):
        tableaus = []
        for tableau in self.game_data['tableaus']:
            cards = detector.get_cards_from_image(tableau['path'])
            if cards:
                tableaus.append(cards)
            else:
                tableaus.append([None])

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
        talon = self.game_data['talon'][0]
        cards = detector.get_cards_from_image(talon['path'])
        return cards


def print_stuff(detection):
    print("Talon")
    pprint(detection.get_talon())
    print("\nFoundations")
    pprint(detection.get_foundations())
    print("\nTableaus")
    pprint(detection.get_tableaus())


if __name__ == '__main__':
    detection = detect()
    # detection.load_state('img/test3.jpg')
    detection.take_picture()
    print_stuff(detection)
    # detection.load_state(f'captures/picture_1.jpg')
    # for n in range(0, 100):
    #    detection.take_picture()

    # for n in range(1, 15):
    #    file = f"img/{n}.jpg"
    #    print(f"\n\nData from {file}")
    #    detection.load_state(file)
    #    if not detection.game_data:
    #        continue
    #    print("Talon")
    #    pprint(detection.get_talon())
    #    print("\nFoundations")
    #    pprint(detection.get_foundations())
    #    print("\nTableaus")
    #    pprint(detection.get_tableaus())
