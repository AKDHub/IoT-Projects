from flask_bcrypt import generate_password_hash
from main import app, db


class AdminUser(db.Model):
    # Flask app name
    __name__ = 'admin_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    @classmethod
    def create_admin(cls, username, password):
        with app.app_context():
            admin = cls(username=username, password=password)
            db.session.add(admin)
            db.session.commit()
            return admin


# create the database tables
with app.app_context():
    db.create_all()