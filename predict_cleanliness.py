from ultralytics import YOLO
import cv2
import os

# =============================
# PATHS
# =============================
DETECTION_MODEL = r"runs/segment/weights/segment.pt"
CLASSIFICATION_MODEL = r"runs/classify/weights/classify.pt"

SOURCE = "test_images"
SAVE_DIR = "results2"

os.makedirs(SAVE_DIR, exist_ok=True)

detector = YOLO(DETECTION_MODEL)
classifier = YOLO(CLASSIFICATION_MODEL)

# =============================
for img_name in os.listdir(SOURCE):

    img_path = os.path.join(SOURCE, img_name)
    image = cv2.imread(img_path)

    if image is None:
        continue

    annotated = image.copy()
    result = detector(image)[0]

    # =========================
    # BOUNDING BOX CROPPING
    # =========================
    if result.boxes is not None:

        for i in range(len(result.boxes)):

            cls_id = int(result.boxes.cls[i])
            cls_name = detector.names[cls_id]

            conf_det = float(result.boxes.conf[i])

            # filter weak detections
            if conf_det < 0.4:
                continue

            x1, y1, x2, y2 = map(int, result.boxes.xyxy[i])

            # padding
            pad = 10
            h, w = image.shape[:2]
            x1 = max(0, x1 - pad)
            y1 = max(0, y1 - pad)
            x2 = min(w, x2 + pad)
            y2 = min(h, y2 + pad)

            crop = image[y1:y2, x1:x2]

            if crop.size == 0:
                continue

            if crop.shape[0] < 50 or crop.shape[1] < 50:
                continue

            crop = cv2.resize(crop, (224, 224))

            # =========================
            # CLASSIFICATION
            # =========================
            cls_result = classifier(crop)[0]

            rating = cls_result.names[cls_result.probs.top1].lower()
            conf_cls = float(cls_result.probs.top1conf)

            # =========================
            # DRAW ONLY BOX + LABEL
            # =========================
            color = (0, 255, 0)

            if rating == "bad":
                color = (0, 0, 255)
            elif rating == "average":
                color = (0, 255, 255)

            label = f"{cls_name}: {rating} ({conf_cls:.2f})"

            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            cv2.putText(annotated, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # =========================
    # PRINT ONLY AREA RESULTS
    # =========================
    print(f"{img_name} processed")

    # SAVE IMAGE
    cv2.imwrite(os.path.join(SAVE_DIR, img_name), annotated)

print("🎉 DONE! Clean minimal output ready!")