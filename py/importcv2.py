import cv2
import face_recognition
import numpy as np
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load dataset khuôn mặt
known_encodings = []
known_names = []

face_dir = "faces"
for filename in os.listdir(face_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(face_dir, filename)
        image = face_recognition.load_image_file(img_path)
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_encodings.append(encoding[0])
            known_names.append(filename.split(".")[0])  # Lấy tên file làm username

@app.route('/face-login', methods=['POST'])
def face_login():
    file = request.files['image']
    image = face_recognition.load_image_file(file)
    unknown_encoding = face_recognition.face_encodings(image)

    if not unknown_encoding:
        return jsonify({"error": "Không phát hiện khuôn mặt"}), 400

    matches = face_recognition.compare_faces(known_encodings, unknown_encoding[0])
    name = "Unknown"
    
    if True in matches:
        matched_idx = np.where(matches)[0][0]
        name = known_names[matched_idx]

    if name == "Unknown":
        return jsonify({"error": "Xác thực thất bại"}), 401

    return jsonify({"message": "Đăng nhập thành công", "user": name})

if __name__ == '__main__':
    app.run(debug=True)
