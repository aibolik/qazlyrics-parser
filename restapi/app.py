from grab import Grab
from grab.spider import Spider, Task
import logging
import sys
from parsing import mymodel
from parsing import db
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
