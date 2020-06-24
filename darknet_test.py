from detection.Darknet.darknet import performDetect as scan
from detection.Darknet.darknet_video import YOLO
import detection.image_processing as imgp
import detection.camera as cam
import detection.card_detection as detector
from pprint import pprint


def picture(img=None):
    cfg = "detection/cfg/card_detection_416.cfg"
    data = "detection/cfg/card_detection.data"
    weights = "detection/cfg/card_detection.weights"
    if not img:
        picture = "detection/extract/talon.png"
    else:
        picture = img

    scan_data = scan(imagePath=picture, thresh=0.4,
                     configPath=cfg, weightPath=weights,
                     metaPath=data, showImage=True,
                     makeImageOnly=False, initOnly=False)


def video():
    while True:
        cam.take_picture(1)
        imgp.get_game_state('detection/captures/picture_1.jpg')
        cards = detector.get_cards_from_image(
            'detection/extract/tableau_1.png')
        pprint(cards)


if __name__ == "__main__":
    video()
