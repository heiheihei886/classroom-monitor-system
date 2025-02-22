from app.run import db


class User(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45))
    password = db.Column(db.String(45))
    name = db.Column(db.String(45))

    def __repr__(self):
        return f'<User {self.username}>'


def query_user_by_name(username):
    user = User.query.filter_by(username=username).first()
    return user


def query_user_by_id(user_id):
    user = User.query.get(user_id)
    return user
