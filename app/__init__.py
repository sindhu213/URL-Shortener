import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    #updates the data like update()
    app.config.from_mapping(
        SECRET_KEY = "development",
        DATABASE = os.path.join(app.instance_path,'app.sqlite'),
    )

    if test_config is None:
        #if test_config is not provided, load configurations from "config.py" file in the instance folder. 
        app.config.from_pyfile("config.py",silent=True)
    else:
        app.config.from_mapping(test_config)

    #create instance folder, if it does not exist already. 
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass 

    @app.route('/')
    def index():
        return "Index page"
    return app