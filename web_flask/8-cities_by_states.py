#!/usr/bin/python3

"""Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def states_lists():
    """number integer message"""
    states = storage.all(State)
    states_list = states.values()
    return render_template('8-cities_by_states.html', states=states_list)


@app.teardown_appcontext
def close_session(exception):
    """Close session"""
    storage.close()


if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')
