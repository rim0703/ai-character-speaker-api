# For Raspberry Pi

import cv2

window_title = "AI Character Speaker"


def showCharacter(image_path):
    character_img = cv2.imread(image_path)

    cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window_title, character_img)
    cv2.waitKey(1)


def closeWindow():
    cv2.destroyWindow(window_title)
