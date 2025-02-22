from flask import Flask, Blueprint, request, jsonify
from flask_redis import FlaskRedis
import jwt
import datetime
from .model import query_user_by_name, query_user_by_id

app = Flask(__name__)
redis_client = FlaskRedis(app)
auth = Blueprint('auth', __name__)


@auth.route('/')
def index():
    return "Hello auth"


@auth.route('/login', methods=['POST'])
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
    user = query_user_by_name(username)
    if not user or user.password != password:  # 假设未使用加密存储
        return jsonify({"error": "Username or password incorrect"}), 401
    value = redis_client.get(username).decode()
    print(value)
    if not value or value != captcha:
        return jsonify({"error": "Otp incorrect"}), 401
    # email_captcha = Captcha.query.filter_by(email=username).first()
    # if not email_captcha or email_captcha.captcha != captcha:
    #     return jsonify({"error": "captcha incorrect"}), 401

    # 生成 token
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # token 过期时间为1天
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    print('成功生成token' + token)
    redis_client.handle_redis_token(username, token)
    return jsonify({"code": 200, "message": "Login successful", "token": token}), 200


@auth.route('/get_user_info', methods=['GET'])
def get_user_info():
    # token = request.headers.get('Authorization')
    token = request.args.get('token')
    if not token:
        return jsonify({"error": "Token is missing"}), 401

    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = payload['user_id']
        print(f'请求的的id{user_id}')
        user = query_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # 返回用户信息
        user_info = {
            'code': 200,  # 添加 code 字段
            'data': {
                'id': user.id,
                'username': user.username,
                # 'roles': 'admin'
                'roles': 'admin' if user.permission == 3 else 'editor' if user.permission == 4 else 'unknown'
            }
        }

        return jsonify(user_info), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


@auth.route('/logout', methods=['POST', 'GET'])
def log_out():
    return jsonify({"code": 200, "message": "Log out successful"}), 200
