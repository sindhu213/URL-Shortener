from flask import Flask, render_template, redirect, request
from utilities import generate_short_url

app = Flask(__name__)

URLMapping = {}

# Takes a long_url as input and generates a shortened_url
# Checks for the pre-existence of long_url and short_url in the mapping
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form['long_url']
        for shortURL, longURL in URLMapping.items():
            if long_url == longURL:
                shortened_url = f"{request.root_url}{shortURL}"
                return render_template("index.html", shortened_url = shortened_url)
            
        short_url = generate_short_url(10)
        while short_url in URLMapping:
            short_url = generate_short_url(10)

        URLMapping[short_url] = long_url    
        shortened_url = f"{request.root_url}{short_url}"
        return render_template("index.html", shortened_url = shortened_url)
    
    return render_template("index.html")


# Searches for short_url in the URLMapping and automatically redirects to the corresponding long_url
# If long_url is not found, renders the 404.html page
@app.route("/<short_url>")
def redirect_to_url(short_url):
    if short_url in URLMapping:
        long_url = URLMapping[short_url]
        return redirect(long_url)
    else:
        return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)