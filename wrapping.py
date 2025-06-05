def warp_and_blend_region(src_frame, dst_frame, src_pts, dst_pts):
    # Calculate affine transform from src_pts to dst_pts
    if len(src_pts) < 3 or len(dst_pts) < 3:
        return dst_frame  # Not enough points

    M, _ = cv2.estimateAffinePartial2D(src_pts, dst_pts)
    warped = cv2.warpAffine(src_frame, M, (dst_frame.shape[1], dst_frame.shape[0]))

    # Create mask from dst_pts
    mask = np.zeros_like(dst_frame)
    cv2.fillConvexPoly(mask, dst_pts, (255, 255, 255))

    # Bitwise blend
    masked_dst = cv2.bitwise_and(dst_frame, cv2.bitwise_not(mask))
    masked_warp = cv2.bitwise_and(warped, mask)
    return cv2.add(masked_dst, masked_warp)
  ####################FOR EXTACT FACE REGION########
def extract_region(frame, landmarks, indices, width, height):
    pts = np.array([
        (int(landmarks[i].x * width), int(landmarks[i].y * height)) 
        for i in indices
    ])
    return pts


################################## MAIN LOOP ##############
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        width, height = frame.shape[1], frame.shape[0]

        # Define source and destination (driving and portrait)
        driving_pts = {
            "mouth": extract_region(frame, landmarks, MOUTH_IDX, width, height),
            "eyes": extract_region(frame, landmarks, EYES_IDX, width, height),
            "nose": extract_region(frame, landmarks, NOSE_IDX, width, height),
        }

        portrait_results = face_mesh.process(cv2.cvtColor(portrait, cv2.COLOR_BGR2RGB))
        if portrait_results.multi_face_landmarks:
            plm = portrait_results.multi_face_landmarks[0].landmark
            portrait_pts = {
                "mouth": extract_region(portrait, plm, MOUTH_IDX, width, height),
                "eyes": extract_region(portrait, plm, EYES_IDX, width, height),
                "nose": extract_region(portrait, plm, NOSE_IDX, width, height),
            }

            animated = portrait.copy()
            for region in ["mouth", "eyes", "nose"]:
                animated = warp_and_blend_region(
                    src_frame=frame,
                    dst_frame=animated,
                    src_pts=driving_pts[region],
                    dst_pts=portrait_pts[region]
                )

            cv2.imshow("LivePortrait Animation Sim", animated)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

