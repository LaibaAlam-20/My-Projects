import cv2 as cv
import mediapipe as mp

from mediapipe.tasks.python import vision as mp_vision
from mediapipe.tasks.python import BaseOptions as MPBaseOptions


class FaceMeshApp:
    def __init__(self, model_path):
        self.detector = self._init_model(model_path)
        self.camera = cv.VideoCapture(0)

    def _init_model(self, model_path):
        base = MPBaseOptions(model_asset_path=model_path)

        config = mp_vision.FaceLandmarkerOptions(
            base_options=base,
            num_faces=1
        )

        return mp_vision.FaceLandmarker.create_from_options(config)

    def _detect_faces(self, frame):
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        return self.detector.detect(mp_image)

    def _render_landmarks(self, frame, landmarks):
        height, width, _ = frame.shape

        for point in landmarks:
            px = int(point.x * width)
            py = int(point.y * height)
            cv.circle(frame, (px, py), 1, (0, 255, 0), -1)

    def run(self):
        while True:
            grabbed, frame = self.camera.read()
            if not grabbed:
                break

            results = self._detect_faces(frame)

            if results.face_landmarks:
                for face in results.face_landmarks:
                    self._render_landmarks(frame, face)

            cv.imshow("Face Mesh (MediaPipe Tasks)", frame)

            if cv.waitKey(1) & 0xFF == 27:
                break

        self.camera.release()
        cv.destroyAllWindows()


# --------- Run App ---------
if __name__ == "__main__":
    app = FaceMeshApp("face_landmarker.task")
    app.run()