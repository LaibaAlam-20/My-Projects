# ============================================================
# HCI MULTI-MODAL DETECTION SYSTEM (FINAL FIXED)
# ============================================================

import cv2
import numpy as np
import mediapipe as mp
from deepface import DeepFace
import time
import random

mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands


# ============================================================
# INPUT SOURCE
# ============================================================

def select_input_source():
    print("\n1. Webcam\n2. Video File\n3. Image")
    choice = input("Choose input (1-3): ")

    if choice == "1":
        return 0
    elif choice == "2":
        return input("Enter video path: ")
    elif choice == "3":
        return input("Enter image path: ")
    else:
        return 0


# ============================================================
# UNIVERSAL IMAGE CHECK
# ============================================================

def is_image(source):
    return isinstance(source, str) and source.lower().endswith((".jpg",".jpeg",".png"))


# ============================================================
# LIPS
# ============================================================

def run_lips_detection(source):
    """
    Lips Detection Module:
    - Smile Detection (T1)
    - MAR Tracking (T2)
    - Lip-Sync Counter (T3)
    """

    import cv2
    import mediapipe as mp

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh()

    # T3 variables
    mouth_open = False
    lip_sync_count = 0

    def process(frame):
        nonlocal mouth_open, lip_sync_count

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        mar = 0
        label = "Neutral"

        if results.multi_face_landmarks:
            for face in results.multi_face_landmarks:

                # Landmarks
                top = face.landmark[13]
                bottom = face.landmark[14]
                left = face.landmark[61]
                right = face.landmark[291]

                # Face reference
                face_left = face.landmark[234]
                face_right = face.landmark[454]

                # 🔹 MAR (T2)
                mar = abs(top.y - bottom.y) / max(abs(left.x - right.x), 1e-6)

                # 🔹 T1 Smile Detection (FIXED METHOD)
                mouth_center_y = (top.y + bottom.y) / 2

                if left.y < mouth_center_y and right.y < mouth_center_y:
                    label = "Smiling"
                else:
                    label = "Neutral"

                # 🔹 T3 Lip Sync Counter (Hysteresis)
                if mar > 0.55 and not mouth_open:
                    mouth_open = True

                elif mar < 0.35 and mouth_open:
                    lip_sync_count += 1
                    mouth_open = False

        # T2 RED BORDER (YAWN DETECTION)
        if mar > 0.55:
            h, w = frame.shape[:2]
            cv2.rectangle(frame, (0,0), (w,h), (0,0,255), 10)

        # 🔹 DISPLAY
        cv2.putText(frame, f"MAR: {mar:.2f}", (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        cv2.putText(frame, f"State: {label}", (20,80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

        cv2.putText(frame, f"Lip Sync Count: {lip_sync_count}", (20,120),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,200,255), 2)

        frame = cv2.resize(frame, (800, 600))
        return frame

    # ---------- IMAGE ----------
    if is_image(source): #extension chak krta ha image ki
        frame = cv2.imread(source)  # read image

        if frame is None:
            print("Image not found")
            return

        while True:
            cv2.imshow("Lips Detection", process(frame.copy()))
            if cv2.waitKey(0) & 0xFF == 27:
                break

        cv2.destroyAllWindows()
        return

    # ---------- VIDEO / WEBCAM ----------
    cap = cv2.VideoCapture(source)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Lips Detection", process(frame))

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# ============================================================
# EYES
# ============================================================

def run_eyes_detection(source):
    """
    Eyes Detection Module:
    - Blink Counter (T1)
    - EAR Display (T2)
    - Drowsiness Alert (T3)
    """

    import cv2
    import mediapipe as mp

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh()

    blink_count = 0 
    eye_closed = False

    drowsy_counter = 0 # kitni bar drowsiness hui 
    normal_counter = 0 # consecutive frames jis main eyes open hain
    drowsy_active = False # drowsy ha yan nhi

    EAR_THRESHOLD = 0.25

    def process(frame):
        nonlocal blink_count, eye_closed
        nonlocal drowsy_counter, normal_counter, drowsy_active

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            for face in results.multi_face_landmarks:

                # -------- EAR FUNCTION --------
                def EAR(eye):
                    p = [face.landmark[i] for i in eye]
                    return (abs(p[1].y - p[5].y) + abs(p[2].y - p[4].y)) / (2 * abs(p[0].x - p[3].x))

                # -------- T2: LEFT + RIGHT EAR --------
                left = EAR([33,160,158,133,153,144])
                right = EAR([362,385,387,263,373,380])
                avg = (left + right) / 2

                # -------- T1: BLINK DETECTION --------
                if avg < EAR_THRESHOLD and not eye_closed:
                    eye_closed = True

                elif avg > EAR_THRESHOLD and eye_closed:
                    blink_count += 1
                    eye_closed = False

                # -------- T3: DROWSINESS --------
                if avg < EAR_THRESHOLD:
                    drowsy_counter += 1
                    normal_counter = 0
                else:
                    normal_counter += 1
                    drowsy_counter = 0

                if drowsy_counter >= 20:
                    drowsy_active = True

                if drowsy_active and normal_counter >= 5:
                    drowsy_active = False

                # -------- DISPLAY --------
                cv2.putText(frame, f"Left EAR: {left:.3f}", (20,40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)

                cv2.putText(frame, f"Right EAR: {right:.3f}", (20,80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,200,255), 2)

                cv2.putText(frame, f"Avg EAR: {avg:.3f}", (20,120),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)

                cv2.putText(frame, f"Blinks: {blink_count}", (20,160),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

                # T3: PROMINENT RED BANNER
                if drowsy_active:
                    h, w = frame.shape[:2]

                    cv2.rectangle(frame, (0, h//2 - 60),
                                  (w, h//2 + 60), (0,0,255), -1)

                    cv2.putText(frame, "DROWSY! Wake Up!",
                                (w//6, h//2 + 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                                (255,255,255), 3)

        frame = cv2.resize(frame, (800, 600))
        return frame

    # ---------- IMAGE ----------
    if is_image(source):
        frame = cv2.imread(source)

        if frame is None:
            print("Image not found")
            return

        while True:
            cv2.imshow("Eyes Detection", process(frame.copy()))
            if cv2.waitKey(0) & 0xFF == 27:
                break

        cv2.destroyAllWindows()
        return

    # ---------- VIDEO / WEBCAM ----------
    cap = cv2.VideoCapture(source)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Eyes Detection", process(frame))

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


# ============================================================
# FACE
# ============================================================

def run_face_detection(source):
    """
    Face Detection Module:
    - Emotion Recognition (DeepFace)
    - Head Pose (MediaPipe)
    - Emotion History (5 sec)
    - Supports webcam, video, and image
    """

    import cv2
    import time
    import mediapipe as mp
    from deepface import DeepFace

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh()

    # Haar Cascade
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    history = []
    frame_count = 0

    # ---------------- PROCESS FUNCTION ----------------
    def process(frame):
        nonlocal frame_count, history

        current_time = time.time()
        emotion = "N/A"
        confidence = 0

        # ---------------- FACE DETECTION ----------------
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # 🔹 T1: Emotion (every 5 frames)
        if frame_count % 5 == 0:
            for (x, y, w, h) in faces:
                face_roi = frame[y:y+h, x:x+w]

                try:
                    res = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
                    emotion = res[0]['dominant_emotion']
                    confidence = res[0]['emotion'][emotion]

                    history.append((emotion, current_time))
                except:
                    pass

        # 🔹 T3: Emotion history (last 5 sec)
        history[:] = [(e, t) for e, t in history if current_time - t <= 5]

        if history:
            emotions_only = [e for e, _ in history]
            mood = max(set(emotions_only), key=emotions_only.count)
        else:
            mood = "N/A"

        # 🔹 T2: Head Pose (FIXED)
        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        direction = "Forward"

        if results.multi_face_landmarks:
            for face in results.multi_face_landmarks:
                nose = face.landmark[1]
                left_eye = face.landmark[33]
                right_eye = face.landmark[263]
                chin = face.landmark[152]   # 👈 IMPORTANT

                eye_mid_x = (left_eye.x + right_eye.x) / 2
                eye_mid_y = (left_eye.y + right_eye.y) / 2

                dx = eye_mid_x - nose.x
                dy = nose.y - eye_mid_y
                chin_dist = chin.y - nose.y   # 👈 KEY FIX

                # 🔥 FINAL LOGIC
                if dx > 0.06:
                    direction = "Right"
                elif dx < -0.06:
                    direction = "Left"
                elif dy > 0.10:
                    direction = "Down"
                elif dy < -0.02 and chin_dist > 0.12:
                    direction = "Up"
                else:
                    direction = "Forward"

        # Draw face box
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        # ---------------- DISPLAY ----------------
        cv2.putText(frame, f"Emotion: {emotion} ({confidence:.1f}%)",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        cv2.putText(frame, f"Head: {direction}",
                    (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)

        cv2.putText(frame, f"Recent Mood: {mood}",
                    (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,200,255), 2)

        frame_count += 1
        frame = cv2.resize(frame, (800, 600))
        return frame

    # ---------------- IMAGE MODE ----------------
    if isinstance(source, str) and source.lower().endswith((".jpg", ".png", ".jpeg")):
        frame = cv2.imread(source)

        if frame is None:
            print("Image not found")
            return

        while True:
            cv2.imshow("Face Detection", process(frame.copy()))
            if cv2.waitKey(0) & 0xFF == 27:
                break

        cv2.destroyAllWindows()
        return

    # ---------------- VIDEO / WEBCAM ----------------
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("Error opening video/webcam")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Face Detection", process(frame))

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# ============================================================
# HAND
# ============================================================

def run_hand_detection(source):
    """Hand Detection: Finger Count + Gesture + Game"""

    import random
    import time
    import cv2
    import mediapipe as mp

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    hands = mp_hands.Hands(max_num_hands=2)

    score = 0
    gestures = ["Fist","One","Peace","Three","Four","Open Hand","Thumbs Up"]
    target = random.choice(gestures)
    hold_start = None

    # ---------- Finger Count ----------
    def get_finger_count(hand, hand_label):
        count = 0

        # Thumb (LEFT/RIGHT fix)
        if hand_label == "Right":
            if hand.landmark[4].x < hand.landmark[3].x:
                count += 1
        else:
            if hand.landmark[4].x > hand.landmark[3].x:
                count += 1

        # Other fingers
        tips = [8, 12, 16, 20]
        for tip in tips:
            if hand.landmark[tip].y < hand.landmark[tip - 2].y:
                count += 1

        return count

    # ---------- Gesture Mapping ----------
    def get_gesture(count, thumb_up=False):
        if thumb_up:
            return "Thumbs Up"

        mapping = {
            0: "Fist",
            1: "One",
            2: "Peace",
            3: "Three",
            4: "Four",
            5: "Open Hand"   
        }

        return mapping.get(count, "Unknown")

    # ---------- Process Frame ----------
    def process(frame):
        nonlocal score, target, hold_start

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        gesture = "None"
        count = 0

        if results.multi_hand_landmarks:
            for i, hand in enumerate(results.multi_hand_landmarks):

                hand_label = results.multi_handedness[i].classification[0].label

                count = get_finger_count(hand, hand_label)

                # 👍 Thumbs Up detection
                thumb_up = (
                    hand.landmark[4].y < hand.landmark[3].y and
                    all(hand.landmark[t].y > hand.landmark[t - 2].y for t in [8,12,16,20])
                )

                gesture = get_gesture(count, thumb_up)

                # Draw landmarks
                mp_drawing.draw_landmarks(
                    frame,
                    hand,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0,255,0), thickness=2),
                    mp_drawing.DrawingSpec(color=(255,0,0), thickness=2)
                )

        # ---------- GAME ----------
        if gesture == target:
            if hold_start is None:
                hold_start = time.time()

            elapsed = time.time() - hold_start

            # Progress bar
            bar_width = int(300 * min(elapsed / 1.0, 1))
            cv2.rectangle(frame, (20, 240), (20 + bar_width, 270), (0,255,0), -1)

            if elapsed >= 1:
                score += 1
                target = random.choice(gestures)
                hold_start = None
        else:
            hold_start = None

        # ---------- DISPLAY ----------
        cv2.putText(frame, f"Fingers: {count}", (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        cv2.putText(frame, f"Gesture: {gesture}", (20,80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

        cv2.putText(frame, f"Target: {target}", (20,120),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,200,0), 2)

        cv2.putText(frame, f"Score: {score}", (20,200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,200,255), 2)

        frame = cv2.resize(frame, (800, 600))
        return frame

    # ---------- IMAGE ----------
    if is_image(source):
        frame = cv2.imread(source)

        if frame is None:
            print("Image not found")
            return

        while True:
            cv2.imshow("Hand Detection", process(frame.copy()))
            if cv2.waitKey(0) & 0xFF == 27:
                break

        cv2.destroyAllWindows()
        return

    # ---------- VIDEO / WEBCAM ----------
    cap = cv2.VideoCapture(source)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Hand Detection", process(frame))

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


# ============================================================
# MAIN
# ============================================================

def main():
    while True:
        print("\n1. Lips\n2. Eyes\n3. Face\n4. Hand\n0. Exit")
        choice=input("Choose: ")

        if choice=="1":
            run_lips_detection(select_input_source())
        elif choice=="2":
            run_eyes_detection(select_input_source())
        elif choice=="3":
            run_face_detection(select_input_source())
        elif choice=="4":
            run_hand_detection(select_input_source())
        elif choice=="0":
            break


if __name__=="__main__":
    main()