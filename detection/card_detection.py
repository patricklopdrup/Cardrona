from .Darknet.darknet import performDetect as scan
from pprint import pprint
from . import image_processing as imgp
import numpy as np
from os import path
from bisect import bisect_left
import yaml
import os
import cv2

# Global configuration for file
cur_path = path.dirname(path.abspath(__file__))
cfg_path = cur_path + "/cfg/cfg.yml"
config = yaml.safe_load(open(cfg_path))
DEBUG = config["Debug"]


def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    return after


def detect_cards(str):
    """
    A function to gather all cards from an image and return them as a list
    """

    # Configuration
    img = cv2.imread(str)
    size = max(img.shape[:2])
    sizes = list(config['ML_Data']['size_cfg'])

    closest = take_closest(sizes, size)

    picture = str
    cfg = f'{cur_path}{config["ML_Data"]["cfg"]}_{closest}.cfg'
    data = cur_path + config["ML_Data"]["data"]
    weights = cur_path + config["ML_Data"]["weights"]

    # Use the scan method from the darknet wrapper to detect all card corners
    scan_data = scan(imagePath=picture, thresh=0.5,
                     configPath=cfg, weightPath=weights,
                     metaPath=data, showImage=False,
                     makeImageOnly=False, initOnly=False)

    # Check if we have at least 1 card corner in the image
    if len(scan_data) < 1:
        return False

    image_data = []

    # Loop through all the card corners in the image and save
    # information about the corners
    for corner in scan_data:
        # Gather data about the detected card corner and calculate
        # the poistion of it
        card_name, confidence, corner_data = corner
        x, y, w, h = corner_data
        x_start = round(x - (w / 2))
        y_start = round(y - (h / 2))
        x_end = round(x_start + w)
        y_end = round(y_start + h)

        # Save all the data about the corner in a dictionary
        formatted_data = {'name': card_name,
                          'start': (x_start, y_start),
                          'end': (x_end, y_end),
                          'confidence': confidence,
                          'width': w,
                          'height': h,
                          'middle': tuple(np.add((x_start, y_start), (w / 2, h / 2)))}

        # Check if the confidence of the detected corner is higher
        # than the defined confidence level in the configuration file
        if confidence > config["ML_Data"]["min_confidence"]:
            # Add it to the list if it is
            image_data.append(formatted_data)

    # If debugging is on, print all the detected card corners
    # and their confidence level
    if DEBUG:
        print("\n\ndetect_cards - Confidence levels")
        for card in image_data:
            print(
                f"Card name: {card['name']}, confidence: {card['confidence']}")

    # Return all card corners as a list of dictionaries
    return image_data


def get_cards_from_image(img_path):
    """
    A function to get all the cards in an image, it will return
    a list of cards ordered by their Y position
    """

    # Retrieve all the card corners in the image
    col_data = detect_cards(img_path)
    if not col_data:
        return

    # Sort the corners by their name (card suit + number)
    col_data = sorted(col_data, key=lambda i: i['name'])

    # Define variables needed for the loop
    cur_card = ""
    card_corners = []
    card_middles = []

    # Loop through all the card corners and group the corners into
    # a single card where we save the card middle
    for c in col_data:
        # Check if the corner is the same suit and value as the corner
        # from the previous iteration
        if not cur_card:  # If no card has been assigned
            cur_card = c['name']
            card_corners = [c['middle']]
            continue

        elif cur_card == c['name']:  # If the corner is the same as the card
            card_corners.append(c['middle'])
            continue

        else:  # If the corner is not the same as the card
            # Calculate the middle of the card and add it to the card_middles
            # array
            card_middle = tuple(np.average(card_corners, axis=0))
            card_middles.append((cur_card, card_middle))

            # Assign the current corner as the new current card
            cur_card = c['name']
            card_corners = [c['middle']]

    # Calculat the middle of the last card in the dataset
    card_middle = tuple(np.average(card_corners, axis=0))
    card_middles.append((cur_card, card_middle))

    # Sort the cards by their Y position in the image
    card_middles = sorted(card_middles, key=lambda t: t[1][1], reverse=False)

    # Return the sorted list of cards
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
                cv2.rectangle(image, rect['start'],
                              rect['end'], (255, 0, 0), 2)
            cv2.imshow("Detected cards", image)
            cv2.waitKey()
            cv2.destroyAllWindows()
