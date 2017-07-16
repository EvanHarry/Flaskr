from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        user = {
            'id': self.id,
            'username': self.username,
            'admin': self.admin
        }
        return s.dumps(user).decode('ascii')

    def to_json(self):
        json_user = {
            'id': self.id,
            'username': self.username,
            'admin': self.admin,
            'tasks': [task.to_simple_json() for task in self.tasks]
        }
        return json_user

    def to_simple_json(self):
        json_user = {
            'id': self.id,
            'username': self.username,
            'admin': self.admin
        }
        return json_user

    @staticmethod
    def verify_auth_token(token):
        s = Serializer('secret key')
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128))
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_json(self):
        json_task = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed
        }
        return json_task

    def to_simple_json(self):
        json_task = {
            'id': self.id,
            'title': self.title
        }
        return json_task

    def __repr__(self):
        return '<Task %r>' % self.title
