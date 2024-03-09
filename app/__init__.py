from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
app.config["SECRET_KEY"] = "OdbXED9b9InYXa1AMXAW1k2epOYJ3EjD"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)   
from app import routes
