import cv2
import numpy as np
import mediapipe as mp

# Load portrait image and resize
portrait = cv2.imread("portrait.jpg")
portrait = cv2.resize(portrait, (640, 480))

# Load driving video
cap = cv2.VideoCapture("driving.mp4")

# Initialize face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False)

# Function to extract specific facial region (eyes, mouth, etc.)
def get_landmark_region(landmarks, region_indices, width, height):
    return [(int(lm.x * width), int(lm.y * height)) for i, lm in enumerate(landmarks.landmark) if i in region_indices]

# Indices for lips (you can modify this)
mouth_indices = list(range(61, 88))  # Inner and outer lips

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0]
        # Get mouth region landmarks
        mouth_points = get_landmark_region(landmarks, mouth_indices, 640, 480)

        # Create mask
        mask = np.zeros_like(frame)
        cv2.fillPoly(mask, [np.array(mouth_points, dtype=np.int32)], (255, 255, 255))
        mouth_only = cv2.bitwise_and(frame, mask)

        # Blend mouth region onto portrait
        mouth_gray = cv2.cvtColor(mouth_only, cv2.COLOR_BGR2GRAY)
        _, mouth_mask = cv2.threshold(mouth_gray, 1, 255, cv2.THRESH_BINARY)
        mouth_mask_inv = cv2.bitwise_not(mouth_mask)

        portrait_bg = cv2.bitwise_and(portrait, portrait, mask=mouth_mask_inv)
        mouth_fg = cv2.bitwise_and(mouth_only, mouth_only, mask=mouth_mask)

        stitched = cv2.add(portrait_bg, mouth_fg)

        cv2.imshow("Animated Portrait", stitched)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
