from os import path
import numpy as np
from pprint import pprint
import cv2


def get_rows(img):
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

    idx = 0
    h, w, _ = img.shape
    minArea = w / 10 * w / 10
    for contour in sorted_contours:
        area = cv2.contourArea(contour)
        if area > minArea:
            print(area)
            idx += 1
            x, y, w, h = cv2.boundingRect(contour)
            roi = img_cnts[y:y + h, x:x + w]
            cv2.imwrite(str(idx) + '.png', roi)
            cv2.drawContours(img_cnts, [contour], -1, (0, 255, 0), 3)
            cv2.imshow('Contours', roi)
            cv2.waitKey()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    while True:
        inp = input("Enter image name or exit : ")
        if inp == "exit":
            print("Bye!")
            break
        if not path.exists(inp):
            print("The specified image does not exist!")
            continue
        img = cv2.imread(inp)
        get_rows(img)
        print("We will do some image processing here soon!")
