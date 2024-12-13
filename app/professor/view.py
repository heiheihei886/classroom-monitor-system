from flask import Blueprint
from .model import add_professor

professor = Blueprint('professor', __name__)


@professor.route('/')
def index():
    return "Hello professor"


@professor.route('/add')
def add():
    add_professor()
    return "success"


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
