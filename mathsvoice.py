import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import tkinter as tk
from PIL import Image, ImageTk
import threading
import pyttsx3

# Initialize MediaPipe and Voice Engine
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)
engine = pyttsx3.init()

# Global Variables
expression = ""
result = ""
last_update_time = 0
update_delay = 1.25
voice_enabled = True

# Voice Feedback
def speak(text):
    if voice_enabled:
        engine.say(text)
        engine.runAndWait()

# Euclidean Distance
def euclidean_distance(p1, p2):
    return np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

# Finger Counting
def count_fingers(hand_landmarks, label):
    tip_ids = [4, 8, 12, 16, 20]
    fingers = []
    if label == "Left":
        fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0] - 1].x else 0)
    else:
        fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x else 0)
    for i in range(1, 5):
        fingers.append(1 if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y else 0)
    return fingers.count(1)

# Gesture Detection
def detectGesture(hand1_data, hand2_data):
    (hand1, label1), (hand2, label2) = hand1_data, hand2_data
    f1 = count_fingers(hand1, label1)
    f2 = count_fingers(hand2, label2)
    dist = euclidean_distance(hand1.landmark[8], hand2.landmark[8])
    if f1 == 1 and f2 == 1:
        if dist < 0.06:
            return "exit"
        return "+"
    elif (f1 == 1 and f2 == 2) or (f1 == 2 and f2 == 1):
        return "-"
    elif (f1 == 1 and f2 == 3) or (f1 == 3 and f2 == 1):
        return "*"
    elif (f1 == 1 and f2 == 4) or (f1 == 4 and f2 == 1):
        return "/"
    elif f1 == 2 and f2 == 2:
        return "del"
    elif (f1 == 1 and f2 == 5) or (f1 == 5 and f2 == 1):
        return "6"
    elif (f1 == 2 and f2 == 5) or (f1 == 5 and f2 == 2):
        return "7"
    elif (f1 == 3 and f2 == 5) or (f1 == 5 and f2 == 3):
        return "8"
    elif (f1 == 4 and f2 == 5) or (f1 == 5 and f2 == 4):
        return "9"
    elif f1 == 0 and f2 == 0:
        return "="
    elif f1 == 5 and f2 == 5:
        return "clear"
    return None

# GUI Update Function
def update_gui():
    expr_label.config(text=f"Expression: {expression}")
    result_label.config(text=f"Result: {result}")

# Gesture Processing Thread
def run_hand_tracking():
    global expression, result, last_update_time
    cap = cv.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            continue
        frame = cv.flip(frame, 1)
        img_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        result_hand = hands.process(img_rgb)
        hand_data = []
        current_time = time.time()

        if result_hand.multi_hand_landmarks and result_hand.multi_handedness:
            for hand_landmarks, handedness in zip(result_hand.multi_hand_landmarks, result_hand.multi_handedness):
                label = handedness.classification[0].label
                hand_data.append((hand_landmarks, label))
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if len(hand_data) == 1:
                hand_landmarks, label = hand_data[0]
                fingers_up = count_fingers(hand_landmarks, label)
                if fingers_up in [0, 1, 2, 3, 4, 5] and current_time - last_update_time > update_delay:
                    expression += str(fingers_up)
                    speak(str(fingers_up))
                    last_update_time = current_time

            elif len(hand_data) == 2:
                gesture = detectGesture(hand_data[0], hand_data[1])
                if gesture == "exit":
                    break
                elif gesture == "clear":
                    expression = ""
                    result = ""
                    speak("Cleared")
                elif gesture == "del" and current_time - last_update_time > update_delay:
                    expression = expression[:-1]
                    speak("Deleted")
                    last_update_time = current_time
                elif gesture == "=" and current_time - last_update_time > update_delay:
                    try:
                        result = str(eval(expression))
                        speak(f"The result is {result}")
                    except:
                        result = "Error"
                        speak("Error")
                    last_update_time = current_time
                elif gesture and current_time - last_update_time > update_delay:
                    expression += gesture
                    speak(gesture)
                    last_update_time = current_time

        # Convert to tkinter-compatible image
        img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
        update_gui()

    cap.release()
    cv.destroyAllWindows()
    root.quit()

# GUI Setup
root = tk.Tk()
root.title("Gesture-Based Math Solver")

video_label = tk.Label(root)
video_label.pack()

expr_label = tk.Label(root, text="Expression: ", font=("Arial", 16))
expr_label.pack()

result_label = tk.Label(root, text="Result: ", font=("Arial", 18), fg="blue")
result_label.pack()

exit_button = tk.Button(root, text="Exit", font=("Arial", 14), command=root.quit)
exit_button.pack(pady=10)

# Start Processing in Thread
t = threading.Thread(target=run_hand_tracking)
t.daemon = True
t.start()

# Run the GUI
root.mainloop()
