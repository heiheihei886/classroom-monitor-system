from app.run import db


class User(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45))
    password = db.Column(db.String(45))
    permission = db.Column(db.String(45))

    def __repr__(self):
        return f'<User {self.username}>'


class Student(db.Model):
    __tablename__ = 'student'
    username = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(45))
    subject = db.Column(db.String(45))
    course_ids = db.Column(db.String(45))

    def __repr__(self):
        return f'<User {self.username}>'


def add(username, password, name, subject, course_ids):
    new_user = User(username=username, password=password, permission=4)
    new_student = Student(username=username, name=name, subject=subject, course_ids=course_ids)
    try:
        db.session.add(new_user)
        db.session.add(new_student)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, "Fail to add data"
    return True, "Succeed in adding data"
