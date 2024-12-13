from flask import Flask, request
from exts import db
import config

app = Flask(__name__)
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


@app.route('/login', methods=['GET'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if not username:
        return "Please enter username"
    if not password:
        return "Please enter password"
    user = User.query.filter_by(username=username).first()
    print(user)
    if not user:
        return "Username or password incorrect"
    return "sss"


if __name__ == '__main__':
    create_blueprint()
    app.run(debug=True)
