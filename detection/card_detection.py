from darknet import performDetect as scan
from pprint import pprint
import image_processing as imgp
import numpy as np
from os import path
import os
import cv2

DEBUG = False


def detect_cards(str):
    picture = str
    cfg = 'cfg/yolo_card_detection.cfg'
    data = 'cfg/card_detection.data'
    weights = 'cfg/card_detection.weights'

    scan_data = scan(imagePath=picture, thresh=0.25,
                     configPath=cfg, weightPath=weights,
                     metaPath=data, showImage=False,
                     makeImageOnly=False, initOnly=False)

    if len(scan_data) < 1:
        return False

    # print(len(scan_data))

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
                          'width': w,
                          'height': h,
                          'middle': tuple(np.add((x_start, y_start), (w / 2, h / 2)))}

        if confidence > 0.5:
            image_data.append(formatted_data)

        if DEBUG:
            print(f"Card name: {card_name}, confidence: {confidence}")

    return image_data


def get_column_numbers(data, showRows=False):
    avg_width = 0
    avg_space = 0
    avg_space_count = 0
    cur_col = 0
    for c in data:
        avg_width += c['size'][0]
        if cur_col != 0:
            space = card_rows[cur_col]['start'][0] - card_rows[cur_col - 1]['end'][0]
            if space < avg_width / (cur_col + 1):
                avg_space += space
                avg_space_count += 1
        cur_col += 1

    avg_width /= len(data)
    avg_space /= avg_space_count
    print(avg_space)
    prev_col = 0
    cur_col = 0
    for i in range(0, len(card_rows)):
        cur_col += 1
        space = card_rows[i]['start'][0] if i == 0 \
            else card_rows[i]['start'][0] - card_rows[i - 1]['end'][0]
        if space > avg_width:
            print(f"Coloumn {cur_col} not found!")
            cur_col += 1

        print(f"Space between column {prev_col} and {cur_col} is {space}")
        prev_col = cur_col


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
            card_rows = imgp.get_rows(img, save=False)
            get_column_numbers(card_rows)
            # print(f"Column position {row['start']}, Column size: {row['size']}")

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
            # pprint(image_data)

        print("We will do some image processing here soon!")
