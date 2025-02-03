from app.run import db


class Professor(db.Model):
    __tablename__ = 'professor'
    username = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(45))
    occupation = db.Column(db.String(45))
    course_ids = db.Column(db.String(45))

    def __repr__(self):
        return f'<User {self.username}>'


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


class Run(db.Model):
    __tablename__ = 'run'
    course_id = db.Column(db.String(45), primary_key=True)
    run_id = db.Column(db.Integer)
    classroom = db.Column(db.String(45))
    time = db.Column(db.String(45))
    professor = db.Column(db.String(45))
    # 其他字段...

    def __repr__(self):
        return f'<Course {self.name}>'


class Performance(db.Model):
    __table_args__ = {'extend_existing': True}
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

def add_professor():
    new_user = Professor(username='john_doe', name='john@example.com', occupation='test', course_ids='test')
    db.session.add(new_user)
    db.session.commit()
    return "success"
