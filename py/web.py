from flask import Flask
from login import login_bp  # ✅ Import Blueprint từ login.py
from devices import devices_bp  # ✅ Import Blueprint từ devices.py
from face_auth import face_auth_bp  # Import Blueprint
from user_management import user_management_bp  # ✅ Thêm dòng này

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Để sử dụng session

# 👉 Đăng ký Blueprint login
app.register_blueprint(login_bp)
# 👉 Đăng ký Blueprint cho devices
app.register_blueprint(devices_bp)
# Đăng ký Blueprint
app.register_blueprint(face_auth_bp)
app.register_blueprint(user_management_bp)  # ✅ Đăng ký blueprint mới
if __name__ == "__main__":
    app.run(debug=True)
