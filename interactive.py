from flask import Flask, render_template
from benandjerrys import *
import sqlite3

DBNAME = 'benandjerrys.db'
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('default.html')

if __name__ == '__main__':
    app.run(debug=True)
