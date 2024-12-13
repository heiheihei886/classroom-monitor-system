from flask import Blueprint, request, jsonify
from .model import add
import os


student = Blueprint('student', __name__)


@student.route('/')
def index():
    return "Hello student"


@student.route('/register', methods=['POST'])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    name = request.form.get("name")
    subject = request.form.get("subject")
    course_ids = request.form.get("course_ids")
    file = request.files.get("file")

    print(
        f"Received data - username: {username}, password: {password}, name: {name}, subject: {subject}, course_ids: {course_ids}, file: {file is not None}")

    if not username or not password or not name or not subject or not file:
        print("Error: Incomplete information")
        return "Incomplete information"
    dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'faces')  # 添加保存路径
    filename = name + ".jpg"
    filepath = os.path.join(dir, filename)

    try:
        file.save(filepath)
        print(f"Image saved to {filepath}")
    except Exception as e:
        print(f"Error saving image: {e}")
        return "Failed to save image"
    # 原架构
    # sql = "SELECT * FROM student WHERE username = '" + username + "'"
    # data = mysql_operate.db.select_db(sql)
    # if data:
    #     return 'User exists'
    # else:
    #     sql1 = "insert into student(username, name, subject, course_ids) values('" + username + "','" + name + "','" + subject + "','" +course_ids + "')"
    #     mysql_operate.db.execute_db(sql1)
    #     sql2 = "insert into user(username, password, permission) values('" + username + "','" + password + "','" + 4 + "')"
    #     mysql_operate.db.execute_db(sql2)
    #     return 'User created successfully'
    res, info = add(username, password, name, subject, course_ids)
    print(f"Database insert result: {info}, Database return info: {res}")

    if not res:
        print("Error: Register unsuccessful")
        return jsonify({
            "success": False,
            "message": "Register unsuccessfully"
        }), 400  # 返回 400 状态码表示客户端错误
    else:
        print("Success: Register successfully")
        return jsonify({
            "success": True,
            "message": "Register successfully"
        }), 200  # 返回 200 状态码表示成功
