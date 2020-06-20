from .Darknet.darknet import performDetect as scan
from pprint import pprint
from . import image_processing as imgp
import numpy as np
from os import path
import yaml
import os
import cv2

cur_path = path.dirname(path.abspath(__file__))
cfg_path = cur_path + "/cfg/cfg.yml"
config = yaml.safe_load(open(cfg_path))
DEBUG = config["Debug"]


def detect_cards(str):
    picture = str
    cfg = cur_path + config["ML_Data"]["cfg"]
    data = cur_path + config["ML_Data"]["data"]
    weights = cur_path + config["ML_Data"]["weights"]

    scan_data = scan(imagePath=picture, thresh=0.25,
                     configPath=cfg, weightPath=weights,
                     metaPath=data, showImage=False,
                     makeImageOnly=False, initOnly=False)

    if len(scan_data) < 1:
        return False

    image_data = []

    for corner in scan_data:
        card_name, confidence, corner_data = corner
        x, y, w, h = corner_data

        x_start = round(x - (w / 2))
        y_start = round(y - (h / 2))
        x_end = round(x_start + w)
        y_end = round(y_start + h)

        formatted_data = {'name': card_name,
                          'start': (x_start, y_start),
                          'end': (x_end, y_end),
                          'confidence': confidence,
                          'width': w,
                          'height': h,
                          'middle': tuple(np.add((x_start, y_start), (w / 2, h / 2)))}

        if confidence > config["ML_Data"]["min_confidence"]:
            image_data.append(formatted_data)

    if DEBUG:
        print("\n\ndetect_cards - Confidence levels")
        for card in image_data:
            print(f"Card name: {card['name']}, confidence: {card['confidence']}")

    return image_data


def get_cards_from_image(img_path):
    col_data = detect_cards(img_path)
    if not col_data:
        return
    col_data = sorted(col_data, key=lambda i: i['name'])

    cur_card = ""
    card_corners = []
    card_middles = []
    for c in col_data:
        if not cur_card:
            cur_card = c['name']
            card_corners = [c['middle']]
            continue
        elif cur_card == c['name']:
            card_corners.append(c['middle'])
            continue
        else:
            card_middle = tuple(np.average(card_corners, axis=0))
            card_middles.append((cur_card, card_middle))
            cur_card = c['name']
            card_corners = [c['middle']]

    card_middle = tuple(np.average(card_corners, axis=0))
    card_middles.append((cur_card, card_middle))

    card_middles = sorted(card_middles, key=lambda t: t[1][1], reverse=False)

    return card_middles


if __name__ == '__main__':
    while True:
        inp = input("Enter command : ")
        if inp == "exit":
            print("Bye!")
            break
        elif inp == "extract":
            inp = input("Enter image path : ")
            if not path.exists(inp):
                print("The specified image does not exist!")
                continue

            img = cv2.imread(inp)
            card_rows = imgp.get_game_state(inp)

        elif inp == "detect":
            inp = input("Enter row number : ")
            img = f"extract/row_{inp}.png"
            if not path.exists(img):
                print("The specified row does not exist!")
                continue

            image_data = detect_cards(img)
            image = cv2.imread(img)
            for rect in image_data:
                cv2.rectangle(image, rect['start'], rect['end'], (255, 0, 0), 2)
            cv2.imshow("Detected cards", image)
            cv2.waitKey()
            cv2.destroyAllWindows()
