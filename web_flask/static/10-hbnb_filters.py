#!/usr/bin/python3
"""a script that starts a flask web application"""
from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """ hello """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ hbnb """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """ c """
    return 'c {}'.format(text.replace("_", " "))


@app.route('/python', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text):
    """ python """
    return 'Python {}'.format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """ num """
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>')
def number_template(n):
    """ template """
    return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """odd/even """
    if n % 2 == 0:
        p = 'even'
    else:
        p = 'odd'
    return render_template('6-number_odd_or_even.html', number=n, parity=p)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ states  """
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def close(error):
    """ err """
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """ cities """
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """ states and /states/<id> """
    not_found = False
    if id is not None:
        states = storage.all(State, id)
        with_id = True
        if len(states) == 0:
            not_found = True
    else:
        states = storage.all(State)
        with_id = False
    return render_template('9-states.html', states=states,
                           with_id=with_id, not_found=not_found)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb2():
    """static filter """
    amenities = storage.all(Amenity)
    states = storage.all(State)
    return render_template('10-hbnb_filters.html', states=states, amenities=amenities)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
