from flask import Blueprint, render_template, jsonify, request

devices_bp = Blueprint("devices", __name__)  # ✅ Dùng Blueprint để tích hợp vào app.py

# Dữ liệu trạng thái thiết bị
devices = {
    "phong_khach": {"Đèn": "tắt", "Máy lạnh": "mở"},
    "phong_ngu": {"Đèn": "mở", "Máy lạnh": "tắt"},
    "nha_bep": {"Đèn": "tắt", "Máy hút mùi": "mở"}
}

# 👉 Trang chính
@devices_bp.route('/')
def home():
    return render_template('index.html')  # Hiển thị trang HTML

# 👉 API lấy trạng thái thiết bị của phòng
@devices_bp.route('/status/<room>', methods=['GET'])
def get_status(room):
    if room in devices:
        return jsonify(devices[room])
    return jsonify({"error": "Phòng không tồn tại"}), 404

# 👉 API cập nhật trạng thái thiết bị
@devices_bp.route('/update', methods=['POST'])
def update_status():
    data = request.json
    room = data.get("room")
    device = data.get("device")
    status = data.get("status")
    
    if room in devices and device in devices[room]:
        devices[room][device] = status
        return jsonify({"message": "Cập nhật thành công"})
    return jsonify({"error": "Phòng hoặc thiết bị không hợp lệ"}), 400

# 👉 Route favicon (tránh lỗi 404 khi trình duyệt tìm favicon)
@devices_bp.route('/favicon.ico')
def favicon():
    return devices_bp.send_static_file('favicon.ico')




