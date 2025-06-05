import cv2
import mediapipe as mp
import numpy as np

# Initialize mediapipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False)

# Load static portrait image
portrait = cv2.imread("portrait.jpg")
portrait = cv2.resize(portrait, (640, 480))

# Open driving video
cap = cv2.VideoCapture("driving.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize for performance
    frame = cv2.resize(frame, (640, 480))

    # Detect landmarks in frame
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0]

        # Extract only mouth landmarks (example: 61 to 88 in MediaPipe)
        mouth_points = []
        for idx in range(61, 88):
            lm = landmarks.landmark[idx]
            x, y = int(lm.x * 640), int(lm.y * 480)
            mouth_points.append((x, y))

        # Draw landmarks on portrait
        output = portrait.copy()
        for point in mouth_points:
            cv2.circle(output, point, 2, (0, 255, 0), -1)

        cv2.imshow("Retargeted Animation", output)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
