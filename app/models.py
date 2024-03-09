from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    history = db.relationship('URLMapping',backref="user", lazy=True)

    def __repr__(self) -> str:
        return f"Username : {self.username}, Email: {self.email}"

class URLMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(100), nullable=False)
    shortened_url = db.Column(db.String(100),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return f"Long URL: {self.long_url}, Shortened URL: {self.shortened_url}"