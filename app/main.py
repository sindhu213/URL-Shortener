from flask import Flask, render_template, redirect, request, send_file
from utilities import generate_short_url
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from io import BytesIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

db = SQLAlchemy(app)

# models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
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


#services
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
    df = pd.DataFrame([(item.id, f"{request.url_root}{item.shortened_url}", item.long_url) for item in data], columns = ["ID", "Shortened URL","LONG URL"])

    excel_file = BytesIO()
    df.to_excel(excel_file, index=False, sheet_name="URLMapping")
    excel_file.seek(0)
    return send_file(excel_file, as_attachment=True, download_name='url_mapping.xlsx')

if __name__ == "__main__":  
    with app.app_context():
        db.drop_all()
        db.create_all()
        app.run(debug=True)