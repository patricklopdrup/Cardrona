from os import path
import cv2


def get_rows(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edge = cv2.Canny(gray, 30, 200)

    contours, _ = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

    cv2.imshow('GrayScale', gray)
    cv2.imshow('Edges', edge)
    cv2.imshow('Contours', img)
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
