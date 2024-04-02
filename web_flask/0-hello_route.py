#!/usr/bin/python3

"""Flask web application"""

from flask import Flask

skill_app = Flask(__name__)

@skill_app.route('/', strict_slashes=False)
def hello():
    """Hello HBNB message"""
    return "Hello HBNB!"

if __name__ == "__main__":
    skill_app.run(port=5000, host='0.0.0.0')