from flask import Flask, render_template, redirect, request, send_file, flash, url_for
from utilities import generate_short_url
import pandas as pd
from io import BytesIO
from models import db, URLMapping, User
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
app.config["SECRET_KEY"] = "OdbXED9b9InYXa1AMXAW1k2epOYJ3EjD"
bcrypt = Bcrypt(app)
db.init_app(app)

login_manager = LoginManager(app)

#Routes
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form['long_url']
        existing_mapping = URLMapping.query.filter_by(long_url=long_url).first()
        if existing_mapping:
            shortened_url = existing_mapping.shortened_url
        else:
            short_url = generate_short_url(10)
            new_mapping = URLMapping(long_url=long_url, shortened_url=short_url, user_id = 1)
            db.session.add(new_mapping)
            db.session.commit()
            shortened_url = f"{request.url_root}{short_url}"
        return render_template("index.html", shortened_url=shortened_url)
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash(f"Your account has been created. You can now login!", 'success')
        return redirect(url_for('login'))
    
    return render_template("register.html")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else: 
            flash("Login unsuccessful. Please check your username and password", 'danger')

    return render_template("login.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/<short_url>")
def redirect_to_url(short_url):
    mapping = URLMapping.query.filter_by(shortened_url = short_url).first()
    if mapping:
        return redirect(mapping.long_url)
    else:
        return render_template("404.html"), 404


@app.route('/mapping')
def mapping():
    data = URLMapping.query.all()
    return render_template("mapping.html", data=data)


@app.route('/download')
def download_mapping():
    data = URLMapping.query.all()
    df = pd.DataFrame([(item.id, f"{request.url_root}{item.shortened_url}", item.long_url) for item in data],
                       columns = ["ID", "Shortened URL","LONG URL"])

    excel_file = BytesIO()
    df.to_excel(excel_file, index=False, sheet_name="URLMapping")
    excel_file.seek(0)
    return send_file(excel_file, as_attachment=True, download_name='url_mapping.xlsx')


if __name__ == "__main__":  
    with app.app_context():
        db.drop_all()
        db.create_all()
        app.run(debug=True)