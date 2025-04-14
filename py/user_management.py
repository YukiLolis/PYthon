from flask import Blueprint, jsonify
from database import connect_db  # kết nối MySQL
from flask import request  # 👈 cần import thêm nếu chưa có

user_management_bp = Blueprint('user_management', __name__)

@user_management_bp.route('/api/users')
def get_users():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, pass, status, phone, address,CCCD FROM users WHERE role != 'admin'")  # tùy bảng bạn
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)
@user_management_bp.route('/api/users/add', methods=['POST'])
def add_user():

    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    email = data.get('email')
    password = data.get('pass')
    phone = data.get('phone')
    cccd = data.get('cccd')

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (name, address, email, pass, phone, role, status, CCCD)
            VALUES (%s, %s, %s, %s, %s, 'user', 'Hoạt động',%s)
        """, (name, address, email, password, phone, cccd))
        conn.commit()
        return jsonify({"message": "Người dùng đã được thêm thành công."}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
@user_management_bp.route('/api/users/update', methods=['POST'])
def update_user():
    data = request.get_json()
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET name=%s, address=%s, email=%s, pass=%s, phone=%s,CCCD=%s,status=%s
            WHERE id=%s
        """, (data['name'], data['address'], data['email'], data['pass'], data['phone'],data['cccd'] ,data['status'], data['id']))
        conn.commit()
        return jsonify({"message": "Đã cập nhật người dùng!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@user_management_bp.route('/api/users/delete', methods=['POST'])
def delete_user():
    data = request.get_json()
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (data['id'],))
        conn.commit()
        return jsonify({"message": "Xóa thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
