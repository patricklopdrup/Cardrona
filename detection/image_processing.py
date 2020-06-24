import numpy as np
import glob
import yaml
import math
import cv2
import os


# Global configuration for file
cur_path = os.path.dirname(os.path.abspath(__file__))
cfg_path = cur_path + "/cfg/cfg.yml"
config = yaml.safe_load(open(cfg_path))
DEBUG = config["Debug"]
DEBUG_IMG = config["Debug_Images"]


def resize_image(img):
    """
    Inspired by alkasm on stackoverflow: https://stackoverflow.com/a/44724368

    A function to resize an image to a square where x and y must be
    divisble by 32.
    If the image extends over 800x800 it will be resized down to be
    compatible with our Darknet model.
    The image will be returned as a cv2 image
    """

    # Get the size of the image and define what the new size will be (max 800x800)
    h, w = img.shape[:2]
    size = 960
    aspect = w / h
    if h > size:
        h = size
        w = np.round(size * aspect).astype(int)
        img = cv2.resize(img, (w, h), interpolation=cv2.INTER_CUBIC)

    padding_hor = size - w

    padding_vert = size - h

    bg_color = config["ML_Data"]["bgcolor"]

    # scale the image and add padding
    scaled_img = cv2.copyMakeBorder(img,
                                    0, padding_vert, 0, padding_hor,
                                    borderType=cv2.BORDER_CONSTANT,
                                    value=bg_color)

    return scaled_img


def get_game_state(img):
    """
    Contour finding expired by geaxgx on GitHub:
    https://github.com/geaxgx/playing-card-detection/blob/master/creating_playing_cards_dataset.ipynb

    A function to get all elements of a solitare game from a single picture.
    The function will find the Talon, foundations and tableaus of the game and
    sort the sub-images by where they were found in the image.
    i.e. sorting the Foundations by their x-position in the image.
    """
    img = cv2.imread(img)

    # Apply morphological transformation to the images, this removes a lot
    # of detail from the image, making the edge detection less prone to error.
    morph = img.copy()
    for n in range(1, 4):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*n+1, 2*n+1))
        morph = cv2.dilate(morph, kernel, iterations=1)
        morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
        morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)

    # Get the grayscale of the image
    blur = cv2.blur(morph, (10, 10))
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # Apply adaptive treshold to the image
    tres = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 255, 0)

    # Extract the edges
    edge = cv2.Canny(tres, 30, 200)

    # Find the contours from the edged image
    contours, _ = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the found contours by their y position
    sorted_contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])
    sorted_contours_copy = sorted_contours.copy()

    img_cnts = img.copy()

    # Remove all files in the extract folder to prepare it for new images
    files = glob.glob(cur_path + '/extract/*')
    for f in files:
        os.remove(f)

    # Check if we have image debugging on and show the contour finding process if it is
    if DEBUG_IMG:
        img_cnts_dbg = img.copy()
        cv2.drawContours(img_cnts_dbg, contours, -1, (0, 255, 0), 3)
        cv2.imshow("Debug", gray)
        cv2.waitKey()
        cv2.imshow("Debug", edge)
        cv2.waitKey()
        cv2.imshow("Debug", img_cnts_dbg)
        cv2.waitKey()

    # Define the minimum size of the detected card areas
    h, w, _ = img.shape
    minArea = w / 30 * w / 30

    # Variables needed in the loop
    top, tableaus = [], []
    idx = 0

    # Loop through all the contours and append the found areas to the images list.
    for contour in sorted_contours_copy:
        sorted_contours.pop(0)
        area = cv2.contourArea(contour)

        # Check if the area of the contour is big enough to be considered a playing card
        if area > minArea:
            idx += 1
            # Find the contour boundaries and save it as a region of interest (ROI)
            x, y, w, h = cv2.boundingRect(contour)
            roi = img_cnts[y:y + h, x:x + w]
            square_img = resize_image(roi)

            # Check if the found area is one of the first 6 areas this means it
            # must be in the top (Talon or foundations) and save it in the top array
            if idx <= 6:
                top.append({'img': square_img, 'start': (x, y),
                            'end': (x + w, y + h), 'size': (w, h),
                            'contour': contour})

            else:  # Save it as a tableau if it is not part of first 6 detections
                tableaus.append({'img': square_img, 'start': (x, y),
                                 'end': (x + w, y + h), 'size': (w, h),
                                 'contour': contour})

    # Sort the arrays by their x-position, we do this so we
    # know what tableau/foundation etc. we are working with
    sorted_top = sorted(top, key=lambda img: img['start'][0])
    sorted_tableaus = sorted(tableaus, key=lambda img: img['start'][0])

    # Reset the index variable and the arrays while also defining a few new ones.
    idx = 0
    talon, foundations, tableaus = [], [], []

    # Loop through the sorted top array and save the images in it in the Extract
    # folder with corresponding names to their placement
    for c in sorted_top:
        idx += 1
        if idx == 2:  # The card is a talon
            image_path = cur_path + "/extract/" + "talon.png"
            cv2.imwrite(image_path, c['img'])
            c.update(path=image_path)
            talon.append(c)

        elif idx > 2:  # The card is a foundation
            image_path = cur_path + "/extract/" + "foundation_" + str(idx-2) + ".png"
            c.update(path=image_path)
            cv2.imwrite(image_path, c['img'])
            foundations.append(c)

        # Check if we have image debugging on and show the
        # individual extracted image contour area if it is
        if DEBUG_IMG:
            cv2.drawContours(img_cnts, [c['contour']], 0, (0, 255, 0), 3)
            cv2.imshow("Debug", img_cnts)
            cv2.waitKey()

    idx = 0
    # Loop through the tableaus and save the images in the extract folder
    for c in sorted_tableaus:
        idx += 1
        image_path = cur_path + "/extract/" + "tableau_" + str(idx) + ".png"
        c.update(path=image_path)
        cv2.imwrite(image_path, c['img'])
        tableaus.append(c)

        # Check if we have image debugging on and show the
        # individual extracted image contour area if it is
        if DEBUG_IMG:
            cv2.drawContours(img_cnts, [c['contour']], 0, (0, 255, 0), 3)
            cv2.imshow("Debug", img_cnts)
            cv2.waitKey()

    # Destroy all OpenCV windows
    if DEBUG_IMG:
        cv2.destroyAllWindows()

    # Check if we have exactly one talon
    if len(talon) != 1:
        print(f"Found {len(talon)} talons but expected 1")
        return False

    # Check if we have exactly 4 foundations
    if len(foundations) != 4:
        print(f"Found {len(foundations)} foundations but expected 4")
        return False

    # Check if we have exactly 7 tableaus
    if len(tableaus) != 7:
        print(f"Found {len(tableaus)} foundations but expected 7")
        return False

    # Return all the found areas in a dictionary
    return {'talon': talon, 'foundations': foundations, 'tableaus': tableaus}
