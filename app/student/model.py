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


class Performance(db.Model):
    __tablename__ = 'performance'
    course_id = db.Column(db.String(45), primary_key=True)
    run_id = db.Column(db.Integer, primary_key=True)
    student_username = db.Column(db.String(45), primary_key=True)
    attendance_days = db.Column(db.Integer)
    completed_days = db.Column(db.Integer)
    angry = db.Column(db.Integer)
    disgust = db.Column(db.Integer)
    fear = db.Column(db.Integer)
    happy = db.Column(db.Integer)
    neutral = db.Column(db.Integer)
    sad = db.Column(db.Integer)
    surprise = db.Column(db.Integer)

    def __repr__(self):
        return (f'<Performance course_id={self.course_id}, run_id={self.run_id}, '
                f'student_username={self.student_username}>')


class Course(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'course'
    course_id = db.Column(db.String(45), primary_key=True)
    title = db.Column(db.String(45))
    professor = db.Column(db.String(45))
    introduction = db.Column(db.String(100))
    number_of_students = db.Column(db.Integer)
    total_days = db.Column(db.Integer)
    # 其他字段...

    def __repr__(self):
        return f'<Course {self.name}>'


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
