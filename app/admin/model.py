from app.run import db


class Admin(db.Model):
    __tablename__ = 'admin'
    username = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(45))

    def __repr__(self):
        return f'<User {self.username}>'


def add_admin():
    new_user = Admin(username='john_doe', name='john@example.com')
    db.session.add(new_user)
    db.session.commit()
    return "success"
