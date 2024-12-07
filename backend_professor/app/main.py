from flask import Flask  # 需自行下载Flask包，并导入这几个内容
from flask import jsonify
from flask import request
from common import mysql_operate  # 从common包中导入mysql_operate，使用其db

app = Flask(__name__)


# 初始化生成一个app对象，这个对象就是Flask的当前实例对象，后面的各个方法调用都是这个实例
# Flask会进行一系列自己的初始化，比如web API路径初始化，web资源加载，日志模块创建等。然后返回这个创建好的对象给你


@app.route("/")  # 自定义路径
def index():
    return 'Hello!'


# @app.route("/query")  # 自定义query路径
# def get_all_users():
#     """获取所有用户信息"""
#     sql = "SELECT * FROM favorites"  # sql语句，可自行对应自己数据相应的表进行操作
#     data = mysql_operate.db.select_db(sql)  # 用mysql_operate文件中的db的select_db方法进行查询
#     print("获取所有用户信息 == >> {}".format(data))  # 在pycharm下打印信息
#     return jsonify(data)  # 在页面输出返回信息的json格式
#
#
# @app.route("/insert", methods=["GET", "POST"])  # 表示GET和POST方法都可以进行操作
# def insert():
#     """插入信息"""
#     url = str(request.args.get('url'))  # url为页面端输入的值
#     title = str(request.args.get('title'))
#     sql = "SELECT * FROM favorites WHERE url = '" + url + "'"
#     data = mysql_operate.db.select_db(sql)
#     if data:  # 判断是否有返回数据，如果有则表示已经存在
#         return '已收藏'
#     else:  # 如果没有，则插入新数据
#         sql1 = "insert into favorites(url,title) values('" + url + "','" + title + "');"
#         mysql_operate.db.execute_db(sql1)
#         return '收藏成功'
#
#
# @app.route("/delete", methods=["GET", "POST"])  #
# def delete():
#     """删除信息"""
#     id = str(request.args.get('id'))
#     sql = "SELECT * FROM favorites WHERE id =" + id
#     data = mysql_operate.db.select_db(sql)
#     if data:
#         sql1 = "DELETE FROM favorites WHERE id =" + id
#         mysql_operate.db.execute_db(sql1)
#         return '删除成功'
#     else:
#         return '不存在此id'


# 教师端
# login
@app.route("/login", methods=["GET"])
def login():
    username = str(request.args.get('username'))
    password = str(request.args.get('password'))
    if not username:
        return 'Please enter username'
    elif not password:
        return 'Please enter password'
    sql = "SELECT * FROM user WHERE username = '" + username + "' AND password = '" + password + "'"
    data = mysql_operate.db.select_db(sql)
    if not data:
        return 'Username or password is incorrect'
    else:
        sql1 = "SELECT permission FROM user WHERE username = '" + username + "' AND password = '" + password + "'"
        data1 = mysql_operate.db.select_db(sql)
        return data1


# register
@app.route("/get_all_courses", methods=["GET"])
def get_all_courses():
    sql = "SELECT title FROM course"
    data = mysql_operate.db.select_db(sql)
    if not data:
        return 'Error getting all courses'
    else:
        return jsonify(data)


@app.route("/create_professor", methods=["GET", "POST"])
def create_professor():
    username = str(request.args.get('username'))
    name = str(request.args.get('name'))
    # gender = str(request.args.get('gender'))
    # occupation = str(request.args.get('occupation'))
    course_ids = str(request.args.get('course_ids'))
    if not username or not name or not course_ids:
        return 'Information error'
    sql = "SELECT * FROM professor WHERE username = '" + username + "'"
    data = mysql_operate.db.select_db(sql)
    if data:
        return 'User exists'
    else:
        sql1 = "insert into professor(username, name, course_ids) values('" + username + "','" + name + "','" + course_ids + "')"
        mysql_operate.db.execute_db(sql1)
        return 'User created successfully'


# view personal information
@app.route("/get_information", methods=["GET"])
def get_information():
    username = str(request.args.get('username'))
    if not username:
        return 'Error getting username'
    sql = "SELECT * FROM professor WHERE username = '" + username + "'"
    data = mysql_operate.db.select_db(sql)
    if not data:
        return 'No personal information'
    else:
        return jsonify(data)


# view courses list
@app.route("/get_courses", methods=["GET"])
def get_courses():
    username = str(request.args.get('username'))
    if not username:
        return 'Error getting username'
    sql = "SELECT course_ids FROM professor WHERE username = '" + username + "'"
    data = mysql_operate.db.select_db(sql)
    if not data:
        return 'No course registered'
    else:
        return jsonify(data)


# view run list
@app.route("/get_runs", methods=["GET"])
def get_runs():
    course_id = str(request.args.get('course_id'))
    if not course_id:
        return 'Error getting course_id'
    sql = "SELECT * FROM run WHERE course_id = '" + course_id + "'"
    data = mysql_operate.db.select_db(sql)
    if not data:
        return 'No runs for this course'
    else:
        return jsonify(data)


# view run information
@app.route("/get_run_information", methods=["GET"])
def get_run_information():
    course_id = str(request.args.get('course_id'))
    run_id = str(request.args.get('course_id'))
    if not course_id or not run_id:
        return 'Error getting course_id or run_id'
    sql = "SELECT * FROM run WHERE course_id = '" + course_id + "' AND run_id = '" + run_id + "'"
    data = mysql_operate.db.select_db(sql)
    if not data:
        return 'No run information'
    else:
        return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8888)  #
# flask默认是没有开启debug模式的，开启debug模式，可以帮助我们查找代码里面的错误
# host = '127.0.0.1' 表示设置的ip，如果需要连接手机等设备，可以将手机和电脑连接同一个热点，将host设置成对应的ip
