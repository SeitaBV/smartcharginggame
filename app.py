import os
import sys

from flask import Flask, render_template, session
import pandas as pd

from models import World, ChargingStation
from utils import install_secret_key

app = Flask(__name__)
install_secret_key(app)

world = None

@app.route('/')
def dashboard():
    global world
    if world is None:
        solar_generation = pd.read_pickle("march9-9to16-8by8.pickle").forecast
        stations = []
        stations.append(ChargingStation(capacity=1, arrival_time=2, leave_time=5))
        stations.append(ChargingStation(capacity=2, arrival_time=4, leave_time=8))
        stations.append(ChargingStation(capacity=3, arrival_time=3, leave_time=5))
        world = World(solar_generation, stations)
    return render_template("dashboard.html", **dict(world=world))

if __name__ == '__main__':
    app.run()
