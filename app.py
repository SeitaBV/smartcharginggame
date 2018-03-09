from flask import Flask, render_template
import pandas as pd

from models import World, ChargingStation
from utils import install_secret_key, init_charging_stations


app = Flask(__name__)
install_secret_key(app)

world = None


@app.route('/')
def dashboard():
    global world
    if world is None:
        solar_generation = pd.read_pickle("march9-9to16-8by8.pickle").forecast
        stations = init_charging_stations()
        world = World(solar_generation, stations)
    return render_template("dashboard.html", **dict(world=world))


if __name__ == '__main__':
    app.run()
