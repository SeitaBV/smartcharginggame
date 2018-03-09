import os
import sys

from flask import Flask, render_template, session
import pandas as pd

from models import World, ChargingStation


def install_secret_key(app, filename='secret_key'):
    """Configure the SECRET_KEY from a file
    in the instance directory.

    If the file does not exist, print instructions
    to create it from a shell with a random key,
    then exit.
    """
    filename = os.path.join(app.instance_path, filename)
    try:
        app.config['SECRET_KEY'] = open(filename, 'rb').read()
    except IOError:
        print('Error: No secret key. Create it with:')
        if not os.path.isdir(os.path.dirname(filename)):
            print('mkdir -p', os.path.dirname(filename))
        print('head -c 24 /dev/urandom >', filename)
        sys.exit(1)

app = Flask(__name__)
install_secret_key(app)

@app.route('/')
def dashboard():
    if session.get("world") is None:
        solar_generation = pd.read_pickle("march9-9to16-8by8.pickle").forecast
        stations = []
        stations.append(ChargingStation(capacity=1, arrival_time=2, leave_time=5))
        stations.append(ChargingStation(capacity=2, arrival_time=4, leave_time=8))
        stations.append(ChargingStation(capacity=3, arrival_time=3, leave_time=5))
        session["world"] = World(solar_generation, stations)
    return render_template("dashboard.html", **dict(world=session.get("world")))

if __name__ == '__main__':
    app.run()
