import sqlite3
import click

#g(type:object) - created (or reused) for each request. 
#current_app(type:object) - points to the Flask app handling the request
from flask import current_app, g