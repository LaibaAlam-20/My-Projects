# ============================================
# EmotionCam - Final Improved Interactive Version
# ============================================

import cv2
import numpy as np
import os
from tensorflow.keras.models import load_model

# ============================================
# LOAD TRAINED MODEL
# ============================================

model = load_model("emotion_model.h5")

# ============================================
# EMOTIONS
# ============================================

emotions = [
    'angry',
    'happy',
    'neutral',
    'sad',
    'surprise'
]

# ============================================
# LOAD FACE DETECTOR
# ============================================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml'
)

# ============================================
# CREATE OUTPUT FOLDER
# ============================================

output_folder = "generated_stickers"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# ============================================
# CLEAR OLD STICKERS
# ============================================

def clear_generated_folder():

    for file in os.listdir(output_folder):

        file_path = os.path.join(output_folder, file)

        if os.path.isfile(file_path):
            os.remove(file_path)

# ============================================
# GENERATE STICKER FUNCTION
# ============================================

def generate_sticker(emotion, animal):

    sticker_path = f"stickers/{emotion}_{animal}.png"

    sticker = cv2.imread(sticker_path)

    if sticker is not None:

        # Resize sticker
        sticker = cv2.resize(sticker, (500,500))

        # ============================================
        # SHOW STICKER
        # ============================================

        cv2.namedWindow(
            "Generated Sticker",
            cv2.WINDOW_NORMAL
        )

        cv2.imshow(
            "Generated Sticker",
            sticker
        )

        # ============================================
        # SAVE STICKER
        # ============================================

        save_path = f"{output_folder}/{emotion}_{animal}.png"

        cv2.imwrite(
            save_path,
            sticker
        )

        print(f"\n{animal.upper()} sticker generated!")
        print(f"Saved in folder: {output_folder}")

        # ============================================
        # KEEP WINDOW OPEN
        # ============================================

        print("Press any key on sticker window...")

        cv2.waitKey(0)

        cv2.destroyWindow("Generated Sticker")

    else:

        print("Sticker not found!")

# ============================================
# MAIN PROGRAM LOOP
# ============================================

while True:

    # ============================================
    # RESET VARIABLES
    # ============================================

    current_emotion = ""
    emotion_counter = 0
    stable_emotion = "neutral"
    emotion_detected = False

    # ============================================
    # CLEAR OLD STICKERS
    # ============================================

    clear_generated_folder()

    # ============================================
    # OPEN WEBCAM
    # ============================================

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cv2.namedWindow("EmotionCam", cv2.WINDOW_NORMAL)

    print("\n===================================")
    print("WEBCAM STARTED")
    print("Show Your Emotion Clearly")
    print("Hold Expression For Few Seconds")
    print("===================================")

    # ============================================
    # DETECTION LOOP
    # ============================================

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Camera not working!")
            break

        frame = cv2.resize(frame, (900,700))

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30,30)
        )

        for (x, y, w, h) in faces:

            # ============================================
            # FACE PROCESSING
            # ============================================

            roi_gray = gray[y:y+h, x:x+w]

            roi_gray = cv2.resize(
                roi_gray,
                (48,48)
            )

            roi = roi_gray.astype('float') / 255.0

            roi = np.reshape(
                roi,
                (1,48,48,1)
            )

            # ============================================
            # PREDICT EMOTION
            # ============================================

            prediction = model.predict(
                roi,
                verbose=0
            )

            label = emotions[np.argmax(prediction)]

            # ============================================
            # STABILIZATION
            # ============================================

            if label == current_emotion:

                emotion_counter += 1

            else:

                current_emotion = label
                emotion_counter = 0

            # ============================================
            # REQUIRE STABLE FRAMES
            # ============================================

            if emotion_counter > 20:

                stable_emotion = label
                emotion_detected = True

            # ============================================
            # DRAW FACE BOX
            # ============================================

            cv2.rectangle(
                frame,
                (x,y),
                (x+w,y+h),
                (255,0,0),
                2
            )

            # ============================================
            # SHOW CURRENT DETECTION
            # ============================================

            cv2.putText(
                frame,
                f"Detecting: {label}",
                (20,50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,255),
                2
            )

            # ============================================
            # SHOW STABLE EMOTION
            # ============================================

            cv2.putText(
                frame,
                f"Stable Emotion: {stable_emotion}",
                (20,100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )

            # ============================================
            # SHOW STABILITY COUNT
            # ============================================

            cv2.putText(
                frame,
                f"Stability Count: {emotion_counter}",
                (20,150),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255,255,0),
                2
            )

            # ============================================
            # USER GUIDE
            # ============================================

            cv2.putText(
                frame,
                "Hold Expression For Few Seconds",
                (20,200),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255,255,255),
                2
            )

        # ============================================
        # SHOW WEBCAM
        # ============================================

        cv2.imshow(
            "EmotionCam",
            frame
        )

        # ============================================
        # STOP WHEN EMOTION DETECTED
        # ============================================

        if emotion_detected:

            print("\n===================================")
            print("Emotion Detected:", stable_emotion)
            print("===================================")

            break

        # ============================================
        # QUIT PROGRAM
        # ============================================

        if cv2.waitKey(1) & 0xFF == ord('q'):

            cap.release()

            cv2.destroyAllWindows()

            exit()

    # ============================================
    # RELEASE WEBCAM
    # ============================================

    cap.release()

    cv2.destroyWindow("EmotionCam")

    # ============================================
    # MENU LOOP
    # ============================================

    while True:

        print("\n===================================")
        print("1 = Cat Sticker")
        print("2 = Monkey Sticker")
        print("3 = Panda Sticker")
        print("4 = Dog Sticker")
        print("5 = Detect New Emotion")
        print("6 = Exit")
        print("===================================")

        choice = input("Enter Choice: ")

        # ============================================
        # CAT STICKER
        # ============================================

        if choice == "1":

            generate_sticker(
                stable_emotion,
                "cat"
            )

        # ============================================
        # MONKEY STICKER
        # ============================================

        elif choice == "2":

            generate_sticker(
                stable_emotion,
                "monkey"
            )

        # ============================================
        # PANDA STICKER
        # ============================================

        elif choice == "3":

            generate_sticker(
                stable_emotion,
                "panda"
            )

        # ============================================
        # DOG STICKER
        # ============================================

        elif choice == "4":

            generate_sticker(
                stable_emotion,
                "dog"
            )

        # ============================================
        # DETECT NEW EMOTION
        # ============================================

        elif choice == "5":

            cv2.destroyAllWindows()

            print("\nRestarting Detection...")

            break

        # ============================================
        # EXIT
        # ============================================

        elif choice == "6":

            cv2.destroyAllWindows()

            print("\nProgram Closed!")

            exit()

        else:

            print("\nInvalid Choice!")