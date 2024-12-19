from flask import Flask, request, jsonify
from flask_cors import CORS
from exts import db
import config
import jwt
import datetime

app = Flask(__name__)
CORS(app, origins="http://localhost:9527")
app.config.from_object(config)
db.init_app(app)


class User(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45))
    password = db.Column(db.String(45))
    permission = db.Column(db.String(45))

    def __repr__(self):
        return f'<User {self.username}>'


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

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print('获取的数据')
    print(data)# 获取 JSON 数据
    username = data.get("username")
    password = data.get("password")
    print(username, password)
    if not username:
        return jsonify({"error": "Please enter username"}), 400
    if not password:
        return jsonify({"error": "Please enter password"}), 400
    user = User.query.filter_by(username=username).first()
    if not user or user.password != password:  # 假设未使用加密存储
        return jsonify({"error": "Username or password incorrect"}), 401

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


if __name__ == '__main__':
    create_blueprint()
    app.run(debug=True)
