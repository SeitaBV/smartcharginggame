from flask import Flask, render_template
import pandas as pd

from models import World
from utils import install_secret_key, init_charging_stations


app = Flask(__name__)
install_secret_key(app)

world = None


@app.route('/')
def init():
    global world
    if world is None:
        solar_generation = pd.read_pickle("march9-9to16-8by8.pickle").forecast
        stations = init_charging_stations()
        world = World(solar_generation, stations)
    return render_template("dashboard.html", **dict(world=world))


@app.route('/next')
def next_step():
    # put together which values we expect (using "order_" and number of stations)
    # complain if the values are not sent
    # call world.next, parse a dict with StationIDs as keys and actions as values
    # render_template
    pass


if __name__ == '__main__':
    app.run()
