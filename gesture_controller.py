import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np


last_action_time = 0
cooldown = 1 

# -------------------------
# Mediapipe setup
# -------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# -------------------------
# Screen and pyautogui setup
# -------------------------
screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

# -------------------------
# Variables
# -------------------------
cap = cv2.VideoCapture(0)
last_action_time = time.time()
cooldown = 0.8
enable_control = False   # start locked
index_hold_start = None
index_hold_duration = 1.0

# -------------------------
# Helper function
# -------------------------
def fingers_up(hand):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    fingers.append(hand.landmark[tips[0]].x < hand.landmark[tips[0]-1].x)

    # Other fingers
    for i in range(1,5):
        fingers.append(hand.landmark[tips[i]].y < hand.landmark[tips[i]-2].y)

    return fingers

# -------------------------
# Main loop
# -------------------------
while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            fingers = fingers_up(hand)

            # -------------------------
            # Gesture definitions
            # -------------------------
            open_palm = fingers == [True, True, True, True, True]
            fist = fingers == [False, False, False, False, False]

            index_only = fingers == [False, True, False, False, False]

            two_fingers = fingers == [False, True, True, False, False]

            four_fingers = fingers == [False, True, True, True, True]

            # -------------------------
            # Get index position
            # -------------------------
            index_tip = hand.landmark[8]
            h, w, _ = frame.shape
            x = int(index_tip.x * w)
            y = int(index_tip.y * h)

            cv2.circle(frame, (x, y), 8, (0,0,255), -1)

            # -------------------------
            # LOCK / UNLOCK
            # -------------------------
            if open_palm:
                enable_control = True

            if fist:
                enable_control = False

            if not enable_control:
                cv2.putText(frame,"GESTURE CONTROL LOCKED",(10,50),
                            cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)
                continue

            # -------------------------
            # NEXT SLIDE (2 fingers)
            # -------------------------
            if two_fingers:
                if time.time() - last_action_time > cooldown:
                    pyautogui.press("right")
                    last_action_time = time.time()

            # -------------------------
            # PREVIOUS SLIDE (4 fingers)
            # -------------------------
            if four_fingers:
                if time.time() - last_action_time > cooldown:
                    pyautogui.press("left")
                    last_action_time = time.time()

            # -------------------------
            # POINTER + LASER (unchanged)
            # -------------------------
            if index_only:

                screen_x = np.interp(x, [0, w], [50, screen_w-50])
                screen_y = np.interp(y, [0, h], [50, screen_h-50])

                pyautogui.moveTo(screen_x, screen_y, duration=0.01)

                pyautogui.keyDown("ctrl")
                pyautogui.mouseDown()

                if index_hold_start is None:
                    index_hold_start = time.time()

                elif time.time() - index_hold_start > index_hold_duration:
                    cv2.putText(frame,"DRAWING MODE",(10,90),
                                cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

            else:
                pyautogui.mouseUp()
                pyautogui.keyUp("ctrl")
                index_hold_start = None

            # -------------------------
            # Display gesture
            # -------------------------
            gesture_name = ""

            if index_only:
                gesture_name = "Pointer / Laser"

            elif two_fingers:
                gesture_name = "Next Slide"

            elif four_fingers:
                gesture_name = "Previous Slide"

            elif open_palm:
                gesture_name = "Unlock"

            elif fist:
                gesture_name = "Lock"

            cv2.putText(frame,f"Gesture: {gesture_name}",(10,30),
                        cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

    cv2.imshow("Gesture Controller",frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
Feature