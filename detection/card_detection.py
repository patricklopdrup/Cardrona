from darknet import performDetect as scan
from pprint import pprint
import os
from os import path
import numpy as np
import glob
import cv2
import math


def resize_image(img):
    """
    Inspired by alkasm on stackoverflow: https://stackoverflow.com/a/44724368

    A method to resize an image to a square where x and y must be
    divisble by 32.
    If the image extends over 800x800 it will be resized down to be
    compatible with our Darknet model.
    The image will be returned as a cv2 image
    """
    h, w = img.shape[:2]
    size = max(h, w)
    size = int(math.ceil(size / 32) * 32) if size <= 800 else 800

    aspect = w/h

    pad_left, pad_right, pad_top, pad_bot = 0, 0, 0, 0
    new_h, new_w = size, size
    if aspect > 1:
        new_h = np.round(size / aspect).astype(int)
        pad_vert = (size - new_h) / 2
        pad_top = np.floor(pad_vert).astype(int)
        pad_bot = np.ceil(pad_vert).astype(int)
    elif aspect < 1:
        new_w = np.round(size * aspect).astype(int)
        pad_horz = (size - new_w) / 2
        pad_left = np.floor(pad_horz).astype(int)
        pad_right = np.ceil(pad_horz).astype(int)

    bg_color = [255] * 3

    # scale and pad
    scaled_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
    scaled_img = cv2.copyMakeBorder(scaled_img,
                                    pad_top, pad_bot, pad_left, pad_right,
                                    borderType=cv2.BORDER_CONSTANT,
                                    value=bg_color)

    return scaled_img


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

    print(len(scan_data))

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
                          'height': h}

        if confidence > 0.5:
            image_data.append(formatted_data)

        print(f"Card name: {card_name}, confidence: {confidence}")

    return image_data


def get_rows(img, save=True):
    # Get the grayscale of the image and reduce noise
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # Extract the edges
    edge = cv2.Canny(gray, 30, 200)

    # Find the contours from the edged image
    contours, _ = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the found contours by their x position
    sorted_contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])

    img_cnts = img.copy()

    # Define the minimum size of the detected card areas
    h, w, _ = img.shape
    minArea = w / 10 * w / 10
    idx = 0
    images = []

    if save:
        files = glob.glob('extract/*')
        for f in files:
            os.remove(f)

    # Loop through all the contours and append the found areas to the images list.
    for contour in sorted_contours:
        area = cv2.contourArea(contour)
        if area > minArea:
            print(area)
            idx += 1
            x, y, w, h = cv2.boundingRect(contour)
            roi = img_cnts[y:y + h, x:x + w]
            square_img = resize_image(roi)
            images.append(square_img)
            if save:
                cv2.imwrite("extract/" + "row_" + str(idx) + ".png", square_img)

    return images


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
            card_rows = get_rows(img)
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
