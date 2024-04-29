from sqlalchemy.testing.pickleable import User

from exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)
    about_me = db.Column(db.Text())
    location = db.Column(db.String(64))
    def ping(self):
        self.last_login = datetime.utcnow()
        db.session.add(self)

    posts = db.relationship('BlogModel', backref='author', lazy='dynamic')


class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)

class BlogModel(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)

    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    blog = db.relationship(BlogModel, backref=db.backref('comments', order_by=create_time.desc()))
    author = db.relationship(UserModel, backref="comments")