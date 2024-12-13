from app.run import db


class Professor(db.Model):
    __tablename__ = 'professor'
    username = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(45))
    occupation = db.Column(db.String(45))
    course_ids = db.Column(db.String(45))

    def __repr__(self):
        return f'<User {self.username}>'


def add_professor():
    new_user = Professor(username='john_doe', name='john@example.com', occupation='test', course_ids='test')
    db.session.add(new_user)
    db.session.commit()
    return "success"
