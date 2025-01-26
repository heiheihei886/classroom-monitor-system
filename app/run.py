from flask import Flask, request, jsonify
from flask_cors import CORS
from exts import db
import config
import jwt
import datetime
from flask_mail import Message, Mail
import string
import random

app = Flask(__name__)
CORS(app)
app.config.from_object(config)
db.init_app(app)
mail = Mail(app)


# @app.route("/mail/test", methods=['GET'])
# def mail_test():
#     # recipients是接收人，是一个数组可以给多人同时发送邮件
#     message = Message(subject="测试", recipients=['e1221716@u.nus.edu'], body="这是一条测试邮件！！！")
#     mail.send(message)
#     return "邮件发送成功"


class User(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45))
    password = db.Column(db.String(45))
    permission = db.Column(db.String(45))

    def __repr__(self):
        return f'<User {self.username}>'


class Captcha(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'captcha'
    email = db.Column(db.String(45), primary_key=True,)
    captcha = db.Column(db.String(6))

    def __repr__(self):
        return f'<Captcha {self.email}>'


def create_blueprint():
    from admin.view import admin  # 延迟导入
    from professor.view import professor
    from student.view import student
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(professor, url_prefix='/professor')
    app.register_blueprint(student, url_prefix='/student')


# @app.route('/login', methods=['GET'])
# def login():
#     username = request.args.get("username")  # 使用 args 获取查询参数
#     password = request.args.get("password")
#     if not username:
#         return "Please enter username"
#     if not password:
#         return "Please enter password"
#     user = User.query.filter_by(username=username).first()
#     if not user or user.password != password:  # 假设未使用加密存储
#         return "Username or password incorrect"
#     return "sss"


@app.route('/get_captcha', methods=['GET', 'POST'])
def get_captcha():
    email = request.form.get("email")
    print(email)
    if not email:
        return jsonify({"success": False, "message": "Please enter email"}), 400
    source = string.digits * 6
    captcha = random.sample(source, 6)
    # 列表变成字符串
    captcha = "".join(captcha)  # 965083
    print(captcha)
    # I/O 操作
    message = Message(subject="2FA", recipients=[email], body=f"Your captcha is: {captcha}")
    mail.send(message)
    # 使用数据库存储
    email_captcha = Captcha.query.filter_by(email=email).first()
    if email_captcha:
        Captcha.query.filter_by(email=email).update({'captcha': captcha})
        db.session.commit()
    else:
        email_captcha = Captcha(email=email, captcha=captcha)
        db.session.add(email_captcha)
        db.session.commit()
    return jsonify({"success": True, "message": "Get captcha successfully"}), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print('获取的数据')
    print(data)# 获取 JSON 数据
    username = data.get("username")
    password = data.get("password")
    captcha = data.get("captcha")
    if not username:
        return jsonify({"error": "Please enter username"}), 400
    if not password:
        return jsonify({"error": "Please enter password"}), 400
    if not captcha:
        return jsonify({"error": "Please enter captcha"}), 400
    user = User.query.filter_by(username=username).first()
    if not user or user.password != password:  # 假设未使用加密存储
        return jsonify({"error": "Username or password incorrect"}), 401
    email_captcha = Captcha.query.filter_by(email=username).first()
    if not email_captcha or email_captcha.captcha != captcha:
        return jsonify({"error": "captcha incorrect"}), 401

    # 生成 token
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # token 过期时间为1天
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    print('成功生成token' + token)

    return jsonify({"code": 200, "message": "Login successful", "token": token}), 200


@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    # token = request.headers.get('Authorization')
    token = request.args.get('token')
    if not token:
        return jsonify({"error": "Token is missing"}), 401

    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = payload['user_id']
        print(f'请求的的id{user_id}')
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # 返回用户信息
        user_info = {
            'code': 200,  # 添加 code 字段
            'data': {
                'id': user.id,
                'username': user.username,
                'roles': 'admin'
            }
        }
        return jsonify(user_info), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

@app.route('/logout', methods=['POST'])
def log_out():
    return jsonify({"code": 200, "message": "Log out successful"}), 200


if __name__ == '__main__':
    create_blueprint()
    app.run(debug=True)
