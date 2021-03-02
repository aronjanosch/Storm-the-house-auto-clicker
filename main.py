import numpy as np
import cv2
from mss.darwin import MSS as mss
import pyautogui, time, math, PIL.Image
from pynput.mouse import Button, Controller
from pynput.keyboard import Controller as keycon
from pynput.keyboard import Key

GAME_REGION = (541,304,1139,750)
timeout = time.time() + 320
last_time = time.time()
mouse = Controller()
keyboard = keycon()
level = 0
last_kills = []
#cv2.imwrite('test.png', image)


def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


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
    cv2.imwrite('empty.png', img)

def mouse_move_click(x,y):
    mouse.position = (x, y)
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(0.02)
    mouse.press(Button.left)
    mouse.release(Button.left)


def kill(sh):
    global GAME_REGION, last_kills
    kill_bubble = 30
    for y in range(250, len(sh), 4):
        for x in range(5, len(sh[y]) - 110, 4):
            if sh[y][x] < 10:
                screen_x = (GAME_REGION[0] + x + 8)
                screen_y = (GAME_REGION[1] + y + 5)

                skip = False
                for pos in last_kills:
                    if dist(screen_x, screen_y, pos[0], pos[1]) < kill_bubble:
                        skip = True
                        break

                if skip:
                    continue

                mouse_move_click(screen_x, screen_y)
                last_kills.append([screen_x, screen_y])

                if len(last_kills) > 4:
                    del last_kills[0]

                if level < 2:
                    return

def reload(sh):
    if sh[27][60] > 195:
        keyboard.press(Key.space)
        time.sleep(0.05)
        keyboard.release(Key.space)


def upgrade():
    mouse_move_click(GAME_REGION[0] + 320, GAME_REGION[1] + 108)
    for i in range(20):
        time.sleep(0.2)
        mouse_move_click(GAME_REGION[0] + 65, GAME_REGION[1] + 110)

    time.sleep(2)
    mouse_move_click(GAME_REGION[0] + 300, GAME_REGION[1] + 410)


while True:
    if time.time() > timeout:
        pass
    mouse_x = pyautogui.position().x
    mouse_y = pyautogui.position().y

    if level == 0:
        image = screenshot()
        template = cv2.imread("play.png")
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.resize(template, (0, 0), fx=0.5, fy=0.5)
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = max_loc
        mouse_move_click(GAME_REGION[0] + top_left[0], GAME_REGION[1] + top_left[1])
        level = 1

    if GAME_REGION[0] < mouse_x < GAME_REGION[2] and GAME_REGION[1] < mouse_y < GAME_REGION[3]:
        image = screenshot()
        #cv2.imwrite('test.png', image)
        reload(image)
        kill(image)
        #print('loop took {} seconds'.format(time.time() - last_time))
        last_time = time.time()

        if image[10][2] > 250:
            print("Sleep 10 sec")
            time.sleep(10)
            print("upgrade")
            upgrade()
            print("sleep 5 sec")
            time.sleep(5)
            print("ready to kill")

