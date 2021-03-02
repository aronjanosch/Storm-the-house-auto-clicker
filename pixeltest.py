import numpy as np
import cv2
from PIL import Image
from mss.darwin import MSS as mss


GAME_REGION = (541,304,1139,750)


def capture_screenshot():
    # Capture entire screen
    with mss() as sct:
        sct_img = sct.grab(GAME_REGION)
        # Convert to PIL/Pillow Image
        return sct_img


def screenshot():
    screen = np.array(capture_screenshot())
    image = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    return cv2.resize(image, (0, 0), fx=0.5, fy=0.5)

def save_screenshot():
    img = screenshot()
    cv2.imwrite(input("Name of the file: "), img)


image = Image.fromarray(screenshot())
px = image.load()
print(px[2, 2])
save_screenshot()
