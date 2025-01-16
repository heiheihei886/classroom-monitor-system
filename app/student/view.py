import base64

from flask import Blueprint, request, jsonify
from .model import add, Student, Performance
from sqlalchemy import func
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


@student.route('/runDetail', methods=['GET'])
def get_course_run_detail_by_id():
    course_id = request.args.get('courseId')
    run_id = request.args.get('runId')
    print(f"course_id: {course_id}, run_id: {run_id}")

    if not course_id:
        return jsonify({"error": "Please provide a course_id"}), 400

    # 查询数据库
    students = Student.query.filter(
        func.json_contains(Student.course_ids, f'"{course_id}"')
    ).all()
    faces_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'faces')

    # 查询 performance 表中的签到结果
    performances = Performance.query.filter_by(course_id=course_id, run_id=run_id).all()
    performance_dict = {p.student_username: p for p in performances}


    # 将查询结果转换为字典列表，并添加图片信息
    filtered_students = []
    for student_f in students:
        # 构建图片文件路径
        image_path = os.path.join(faces_dir, student_f.name + ".jpg")

        # 读取图片并编码为 base64
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        else:
            encoded_image = None

        # 获取签到信息
        performance = performance_dict.get(student_f.username)
        if performance and performance.attendance_days is not None:
            checked_in = True
        else:
            checked_in = False

        # 构建学生信息字典
        student_info = {
            'username': student_f.username,
            'name': student_f.name,
            'image': encoded_image,
            'check_in': checked_in
        }

        filtered_students.append(student_info)

    return jsonify({"success": True, "students": filtered_students}), 200
