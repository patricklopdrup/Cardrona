import numpy as np
import glob
import yaml
import math
import cv2
import os


cur_path = os.path.dirname(os.path.abspath(__file__))
cfg_path = cur_path + "/cfg/cfg.yml"
config = yaml.safe_load(open(cfg_path))
DEBUG = config["Debug"]
DEBUG_IMG = config["Debug_Images"]


def resize_image(img):
    """
    Inspired by alkasm on stackoverflow: https://stackoverflow.com/a/44724368

    A method to resize an image to a square where x and y must be
    divisble by 32.
    If the image extends over 800x800 it will be resized down to be
    compatible with our Darknet model.
    The image will be returned as a cv2 image
    """
    max_size = config["ML_Data"]["max_size"]
    h, w = img.shape[:2]
    size = max(h, w)
    size = int(math.ceil(size / 32) * 32) if size <= max_size else max_size

    aspect = w / h

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

    bg_color = config["ML_Data"]["bgcolor"]

    # scale and pad
    scaled_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
    scaled_img = cv2.copyMakeBorder(scaled_img,
                                    pad_top, pad_bot, pad_left, pad_right,
                                    borderType=cv2.BORDER_CONSTANT,
                                    value=bg_color)

    return scaled_img


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
        files = glob.glob(cur_path + '/extract/*')
        for f in files:
            os.remove(f)

    if DEBUG_IMG:
        img_cnts_dbg = img.copy()
        cv2.drawContours(img_cnts_dbg, contours, -1, (0, 255, 0), 3)
        cv2.imshow("Debug", gray)
        cv2.waitKey()
        cv2.imshow("Debug", edge)
        cv2.waitKey()
        cv2.imshow("Debug", img_cnts_dbg)
        cv2.waitKey()
    # Loop through all the contours and append the found areas to the images list.
    for contour in sorted_contours:
        area = cv2.contourArea(contour)
        print(area)
        if area > minArea:
            # print(area)
            idx += 1
            x, y, w, h = cv2.boundingRect(contour)
            roi = img_cnts[y:y + h, x:x + w]
            square_img = resize_image(roi)
            images.append({'img': square_img, 'start': (x, y),
                           'end': (x + w, y + h), 'size': (w, h)})
            if save:
                cv2.imwrite(cur_path + "/extract/" + "row_" + str(idx) + ".png", square_img)

            if DEBUG_IMG:
                cv2.drawContours(img_cnts, [contour], 0, (0, 255, 0), 3)
                cv2.imshow("Debug", img_cnts)
                cv2.waitKey()
    if DEBUG_IMG:
        cv2.destroyAllWindows()

    return images


def get_game_state(img):
    img = cv2.imread(img)
    # Get the grayscale of the image and reduce noise
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # Extract the edges
    edge = cv2.Canny(gray, 30, 200)

    # Find the contours from the edged image
    contours, _ = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the found contours by their x position
    sorted_contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])
    sorted_contours_copy = sorted_contours.copy()

    img_cnts = img.copy()

    # Define the minimum size of the detected card areas
    h, w, _ = img.shape
    minArea = w / 10 * w / 10
    idx = 0
    top = []
    tableaus = []

    files = glob.glob(cur_path + '/extract/*')
    for f in files:
        os.remove(f)

    if DEBUG_IMG:
        img_cnts_dbg = img.copy()
        cv2.drawContours(img_cnts_dbg, contours, -1, (0, 255, 0), 3)
        cv2.imshow("Debug", gray)
        cv2.waitKey()
        cv2.imshow("Debug", edge)
        cv2.waitKey()
        cv2.imshow("Debug", img_cnts_dbg)
        cv2.waitKey()
    # Loop through all the contours and append the found areas to the images list.
    for contour in sorted_contours_copy:
        sorted_contours.pop(0)
        area = cv2.contourArea(contour)
        if area > minArea:
            # print(area)
            idx += 1
            x, y, w, h = cv2.boundingRect(contour)
            roi = img_cnts[y:y + h, x:x + w]
            square_img = resize_image(roi)
            if idx <= 6:
                top.append({'img': square_img, 'start': (x, y),
                            'end': (x + w, y + h), 'size': (w, h),
                            'contour': contour})
            else:
                tableaus.append({'img': square_img, 'start': (x, y),
                                 'end': (x + w, y + h), 'size': (w, h),
                                 'contour': contour})

    sorted_top = sorted(top, key=lambda img: img['start'][0])
    sorted_tableaus = sorted(tableaus, key=lambda img: img['start'][0])

    idx = 0
    talon = []
    foundations = []
    tableaus = []

    for c in sorted_top:
        idx += 1
        if idx == 2:
            image_path = cur_path + "/extract/" + "talon.png"
            cv2.imwrite(image_path, c['img'])
            c.update(path=image_path)
            talon.append(c)
        elif idx > 2:
            image_path = cur_path + "/extract/" + "foundation_" + str(idx-2) + ".png"
            c.update(path=image_path)
            cv2.imwrite(image_path, c['img'])
            foundations.append(c)

        if DEBUG_IMG:
            cv2.drawContours(img_cnts, [c['contour']], 0, (0, 255, 0), 3)
            cv2.imshow("Debug", img_cnts)
            cv2.waitKey()

    idx = 0
    for c in sorted_tableaus:
        idx += 1
        image_path = cur_path + "/extract/" + "tableau_" + str(idx) + ".png"
        c.update(path=image_path)
        cv2.imwrite(image_path, c['img'])
        tableaus.append(c)

        if DEBUG_IMG:
            cv2.drawContours(img_cnts, [c['contour']], 0, (0, 255, 0), 3)
            cv2.imshow("Debug", img_cnts)
            cv2.waitKey()
    cv2.destroyAllWindows()

    if len(talon) != 1:
        print("Talon error in image")
        return False

    if len(foundations) != 4:
        print(f"Found {len(foundations)} foundations but expected 4")
        return False

    if len(tableaus) != 7:
        print(f"Found {len(tableaus)} foundations but expected 7")
        return False

    return {'talon': talon, 'foundations': foundations, 'tableaus': tableaus}
