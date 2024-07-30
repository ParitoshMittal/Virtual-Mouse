import cv2
import mediapipe as mp
import pyautogui

# Capture Camera using Opencv
cap = cv2.VideoCapture(0)

# Detect hand using Mediapipeline
hand_detector = mp.solutions.hands.Hands()

# Drawing Utils for drawing Landmarks
drawing_utils = mp.solutions.drawing_utils

# Get Screen Size using pyAutoGui
screen_width, screen_height = pyautogui.size()

index_y = 0

# Creating Continues While loop
while True:

    # Capture Frame
    _, frame = cap.read()

    # Flip Frame's axis
    frame = cv2.flip(frame, 1)

    # Getting Frame Size
    frame_height, frame_width, _ = frame.shape

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect Hand Using Mediapipe
    output = hand_detector.process(rgb_frame)

    # Identifying Landmarks on Hands
    hands = output.multi_hand_landmarks

    # Checking if hand Detected
    if hands:
        for hand in hands:

            # Draw Landmarks on Hands
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):

                # Creating the x & y Position for Mouse
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)

                # Setting condition for Index Finger (Landmark for tip of Index finger is 8)
                if id == 8:

                    # Draw Circle around Index Finger
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                    index_x = screen_width/frame_width*x
                    index_y = screen_height/frame_height*y

                # Setting condition when Thumb meets Index Finger (Landmark for tip of Thumb is 4)
                if id == 4:
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width/frame_width*x
                    thumb_y = screen_height/frame_height*y

                    # Perform click event if Distance between Thumb and Index Finger is less then 20
                    if abs(index_y - thumb_y) < 20:
                        pyautogui.click()
                        pyautogui.sleep(1)
                    # or Move the Cursor on Screen
                    elif abs(index_y - thumb_y) < 100:
                        pyautogui.moveTo(index_x, index_y)

    # Create Live Camera Frame
    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)