from flask import Blueprint, request, jsonify, session
import cv2
import face_recognition
import numpy as np
from database import connect_db  # Import kết nối DB từ database.py

face_auth_bp = Blueprint("face_auth", __name__)  # Tạo Blueprint

# 👉 API đăng ký khuôn mặt
@face_auth_bp.route('/register-face', methods=['POST'])
def register_face():
    try:
        name = request.form['name']
        email = request.form['email']

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return jsonify({"error": "Không thể mở camera!"}), 500

        ret, frame = cap.read()

        cap.release()
        cv2.destroyAllWindows()

        if not ret:
            return jsonify({"error": "Lỗi chụp ảnh!"}), 500

        # Xử lý ảnh
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_frame)

        if not face_encodings:
            return jsonify({"error": "Không tìm thấy khuôn mặt!"}), 400

        face_encoding_str = ','.join(map(str, face_encodings[0]))

        # Lưu vào database
        conn = connect_db()
        cursor = conn.cursor()
        sql = "INSERT INTO users (name, email, face_encoding) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, email, face_encoding_str))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Đăng ký khuôn mặt thành công!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 👉 API đăng nhập bằng Face ID
@face_auth_bp.route('/face-login', methods=['GET'])
def face_login():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return jsonify({"error": "Không thể mở camera!"}), 500

        ret, frame = cap.read()
        print("ret:", ret)
        print("frame is None:", frame is None)  
        cap.release()
        cv2.destroyAllWindows()

        if not ret:
            return jsonify({"error": "Lỗi chụp ảnh!"}), 500

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_frame)

        if not face_encodings:
            return jsonify({"error": "Không nhận diện được khuôn mặt!"}), 400

        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        for user in users:
            db_encoding = np.array([float(x) for x in user["face_encoding"].split(",")])
            matches = face_recognition.compare_faces([db_encoding], face_encodings[0])

            if matches[0]:  # Nếu khuôn mặt khớp
                session["email"] = user["email"]
                session["name"] = user["name"]
                return jsonify({"status": "success", "name": user["name"]})

        return jsonify({"error": "Không tìm thấy tài khoản phù hợp!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


