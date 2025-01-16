from flask import Blueprint, request, jsonify
from .model import add_professor, Course, Run

professor = Blueprint('professor', __name__)


@professor.route('/')
def index():
    return "Hello professor"


@professor.route('/add')
def add():
    add_professor()
    return "success"

# 获取指定老师所教授的课程列表
@professor.route('/courses', methods=['GET'])
def get_courses_by_professor():
    professor_name = request.args.get('professor')
    if not professor_name:
        return jsonify({"error": "Please provide a professor name"}), 400

    # 查询数据库
    courses = Course.query.filter_by(professor=professor_name).all()

    # 将查询结果转换为字典列表
    filtered_courses = [
        {
            'id': course.course_id,
            'title': course.title,
            'professor': course.professor,
            'number': course.number_of_students
        }
        for course in courses
    ]

    return jsonify({"success": True, "courses": filtered_courses}), 200


@professor.route('/courseRunList', methods=['GET'])
def get_course_run_list_by_id():
    course_id = request.args.get('courseId')
    if not course_id:
        return jsonify({"error": "Please provide a course_id"}), 400

    # 查询数据库
    runs = Run.query.filter_by(course_id=course_id).all()

    # 将查询结果转换为字典列表
    filtered_runs = [
        {
            'id': run.course_id,
            'runId': run.run_id,
            'classroom': run.classroom,
            'time': run.time,
            'professor': run.professor
        }
        for run in runs
    ]

    return jsonify({"success": True, "runs": filtered_runs}), 200


@professor.route('/register', methods=['POST'])
def register():
    username = request.form.get("username")
    name = request.form.get("name")
    subject = request.form.get("subject")
    course_ids = request.form.get("course_ids")
    file = request.form.get("file")
    if not username or not name or not subject or not file:
        return "Incomplete information"
    dir = ""  # 添加保存路径
    filename = name + ".jpg"
    filepath = os.path.join(dir, filename)
    image = base64.b64decode(file)
    with Image.open(io.BytesIO(image)) as img:
        img.save(filepath)
    # 原架构
    # sql = "SELECT * FROM student WHERE username = '" + username + "'"
    # data = mysql_operate.db.select_db(sql)
    # if data:
    #     return 'User exists'
    # else:
    #     sql1 = "insert into student(username, name, subject, course_ids) values('" + username + "','" + name + "','" + subject + "','" +course_ids + "')"
    #     mysql_operate.db.execute_db(sql1)
    #     return 'User created successfully'
    res, info = add(username, name, subject, course_ids)
    if not res:
        return "Register unsuccessfully"
    else:
        return "Register successfully"
