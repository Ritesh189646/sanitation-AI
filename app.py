import os
import io
import base64
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, send_from_directory
from ultralytics import YOLO

app = Flask(__name__, template_folder='templates', static_folder='static')

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DETECTION_MODEL_PATH = os.path.join(BASE_DIR, "runs", "segment", "weights", "segment.pt")
CLASSIFICATION_MODEL_PATH = os.path.join(BASE_DIR, "runs", "classify", "weights", "classify.pt")
TEST_IMAGES_DIR = os.path.join(BASE_DIR, "test_images")
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
RESULTS_DIR = os.path.join(BASE_DIR, "static", "results_ui")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Lazy loading models
detector = None
classifier = None

def get_models():
    global detector, classifier
    if detector is None:
        if os.path.exists(DETECTION_MODEL_PATH):
            detector = YOLO(DETECTION_MODEL_PATH)
        else:
            raise FileNotFoundError(f"Detection model not found at {DETECTION_MODEL_PATH}")
    if classifier is None:
        if os.path.exists(CLASSIFICATION_MODEL_PATH):
            classifier = YOLO(CLASSIFICATION_MODEL_PATH)
        else:
            raise FileNotFoundError(f"Classification model not found at {CLASSIFICATION_MODEL_PATH}")
    return detector, classifier

def cv2_to_base64(image_np):
    _, buffer = cv2.imencode('.jpg', image_np)
    encoded = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{encoded}"

def analyze_image_numpy(image, filename="image.jpg", conf_thresh=0.4, pad=10, min_size=50):
    det, cls = get_models()
    h, w = image.shape[:2]
    annotated = image.copy()
    
    results = det(image)[0]
    
    detected_objects = []
    status_counts = {"good": 0, "average": 0, "bad": 0}
    
    if results.boxes is not None and len(results.boxes) > 0:
        for i in range(len(results.boxes)):
            conf_det = float(results.boxes.conf[i])
            if conf_det < conf_thresh:
                continue
                
            cls_id = int(results.boxes.cls[i])
            cls_name = det.names[cls_id]
            x1, y1, x2, y2 = map(int, results.boxes.xyxy[i])
            
            # Add padding
            px1 = max(0, x1 - pad)
            py1 = max(0, y1 - pad)
            px2 = min(w, x2 + pad)
            py2 = min(h, y2 + pad)
            
            crop = image[py1:py2, px1:px2]
            if crop.size == 0 or crop.shape[0] < min_size or crop.shape[1] < min_size:
                continue
                
            resized_crop = cv2.resize(crop, (224, 224))
            cls_res = cls(resized_crop)[0]
            
            rating = cls_res.names[cls_res.probs.top1].lower()
            conf_cls = float(cls_res.probs.top1conf)
            
            status_counts[rating] = status_counts.get(rating, 0) + 1
            
            # Bounding box color based on rating
            if rating == "bad":
                color = (0, 0, 255) # Red (BGR)
            elif rating == "average":
                color = (0, 215, 255) # Yellow/Amber (BGR)
            else:
                color = (0, 255, 128) # Green (BGR)
                
            label = f"{cls_name}: {rating} ({conf_cls:.2f})"
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            
            # Draw label background box for crisp legibility
            (lbl_w, lbl_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(annotated, (x1, max(0, y1 - 22)), (x1 + lbl_w + 6, max(0, y1)), color, -1)
            cv2.putText(annotated, label, (x1 + 3, max(14, y1 - 6)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            
            crop_b64 = cv2_to_base64(crop)
            
            detected_objects.append({
                "id": i + 1,
                "class_name": cls_name,
                "det_confidence": round(conf_det, 3),
                "rating": rating,
                "rating_confidence": round(conf_cls, 3),
                "bbox": [x1, y1, x2, y2],
                "crop_b64": crop_b64
            })
            
    # Calculate overall image status
    if status_counts["bad"] > 0:
        overall_status = "BAD"
    elif status_counts["average"] > 0:
        overall_status = "AVERAGE"
    elif status_counts["good"] > 0:
        overall_status = "GOOD"
    else:
        overall_status = "NO OBJECTS DETECTED"
        
    annotated_b64 = cv2_to_base64(annotated)
    original_b64 = cv2_to_base64(image)
    
    return {
        "filename": filename,
        "width": w,
        "height": h,
        "overall_status": overall_status,
        "status_counts": status_counts,
        "total_objects": len(detected_objects),
        "objects": detected_objects,
        "annotated_b64": annotated_b64,
        "original_b64": original_b64
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        conf_thresh = float(request.form.get('conf_thresh', 0.4))
        pad = int(request.form.get('pad', 10))
        
        if 'image' in request.files:
            file = request.files['image']
            filename = file.filename
            image_bytes = file.read()
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        elif request.json and 'test_filename' in request.json:
            filename = request.json['test_filename']
            conf_thresh = float(request.json.get('conf_thresh', conf_thresh))
            pad = int(request.json.get('pad', pad))
            img_path = os.path.join(TEST_IMAGES_DIR, filename)
            if not os.path.exists(img_path):
                return jsonify({"error": f"Test image '{filename}' not found"}), 404
            img = cv2.imread(img_path)
        else:
            return jsonify({"error": "No image uploaded or test filename provided"}), 400
            
        if img is None:
            return jsonify({"error": "Failed to decode image"}), 400
            
        res = analyze_image_numpy(img, filename=filename, conf_thresh=conf_thresh, pad=pad)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/test_images', methods=['GET'])
def get_test_images():
    if not os.path.exists(TEST_IMAGES_DIR):
        return jsonify([])
    valid_exts = ('.jpg', '.jpeg', '.png', '.webp')
    files = [f for f in os.listdir(TEST_IMAGES_DIR) if f.lower().endswith(valid_exts)]
    return jsonify(files)

@app.route('/api/batch', methods=['POST'])
def run_batch():
    try:
        conf_thresh = float(request.json.get('conf_thresh', 0.4))
        pad = int(request.json.get('pad', 10))
        
        if not os.path.exists(TEST_IMAGES_DIR):
            return jsonify({"error": "test_images directory not found"}), 404
            
        valid_exts = ('.jpg', '.jpeg', '.png', '.webp')
        files = [f for f in os.listdir(TEST_IMAGES_DIR) if f.lower().endswith(valid_exts)]
        
        batch_results = []
        summary = {"good": 0, "average": 0, "bad": 0, "no_objects": 0, "total_images": len(files), "total_objects": 0}
        
        for filename in files:
            img_path = os.path.join(TEST_IMAGES_DIR, filename)
            img = cv2.imread(img_path)
            if img is None:
                continue
            res = analyze_image_numpy(img, filename=filename, conf_thresh=conf_thresh, pad=pad)
            
            batch_results.append({
                "filename": filename,
                "overall_status": res["overall_status"],
                "total_objects": res["total_objects"],
                "status_counts": res["status_counts"],
                "annotated_b64": res["annotated_b64"]
            })
            
            st = res["overall_status"].lower()
            if st in summary:
                summary[st] += 1
            else:
                summary["no_objects"] += 1
            summary["total_objects"] += res["total_objects"]
            
        return jsonify({
            "summary": summary,
            "results": batch_results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    det, cls = get_models()
    return jsonify({
        "detection_model": os.path.basename(DETECTION_MODEL_PATH),
        "classification_model": os.path.basename(CLASSIFICATION_MODEL_PATH),
        "detector_classes": list(det.names.values()),
        "classifier_classes": list(cls.names.values()),
        "test_images_count": len(os.listdir(TEST_IMAGES_DIR)) if os.path.exists(TEST_IMAGES_DIR) else 0
    })

if __name__ == '__main__':
    print("🚀 Starting Sanitation AI Web Dashboard on http://127.0.0.1:5000 ...")
    app.run(host='127.0.0.1', port=5000, debug=False)
