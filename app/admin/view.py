from flask import Blueprint, request
from .model import add_admin

admin = Blueprint('admin', __name__)


@admin.route('/')
def index():
    return "Hello admin"


@admin.route('/add')
def add():
    add_admin()
    return "success"


@admin.route('/register', methods=['POST'])
def register():
    username = request.form.get("username")
    name = request.form.get("name")
    if not username or not name:
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
