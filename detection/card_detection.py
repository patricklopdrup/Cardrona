from darknet import performDetect as scan
from pprint import pprint
import os
from os import path
import numpy as np
import glob
import cv2


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
            images.append(roi)
            if save:
                cv2.imwrite("extract/" + "row_" + str(idx) + ".png", roi)

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
            cv2.imshow("Hello", image)
            cv2.waitKey()
            cv2.destroyAllWindows()
            pprint(image_data)

        # sharpen_image(img)

        print("We will do some image processing here soon!")
