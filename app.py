from flask import Flask, render_template
import pandas as pd

from models import World, ChargingStation
from utils import install_secret_key, init_charging_stations, make_custom_js

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

    current_turn = world.current_step  # We start at turn 0
    transaction_costs = 5  # in number of coins
    num_stations = len(world.charging_stations)
    num_turns = len(world.solar_park.generation)
    production = world.solar_park.generation
    production = [float(i) for i in production]  # convert to integers
    max_production = int(max(production))
    consumption = [[0, 0, 0, 1, 0, 0, 0],
                   [0, 0, 0, 1, 1, 0, 0],
                   [0, 0, 0, 0, 1, 2, 0]]
    station_id = [station for station in world.charging_stations]
    max_capacity = [world.charging_stations.get(station).capacity for station in world.charging_stations]
    arrivals = [[0, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0]]
    departures = [[0, 0, 0, 1, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0],
                  [0, 0, 0, 0, 0, 0, 1]]
    target_consumption = [[0, 0, 0, 3, 0, 0, 0],
                          [0, 0, 0, 0, 5, 0, 0],
                          [0, 0, 0, 0, 0, 0, 1]]

    safe_js = make_custom_js(num_stations, num_turns)

    return render_template("dashboard.html", **dict(world=world),
                           num_stations=num_stations,
                           num_turns=num_turns,
                           current_turn=current_turn,
                           production=production,
                           max_production=max_production,
                           max_capacity=max_capacity,
                           station_id=station_id,
                           safe_js=safe_js
                           )


@app.route('/next')
def next_step():
    # put together which values we expect (using "order_" and number of stations)
    # complain if the values are not sent
    # call world.next, parse a dict with StationIDs as keys and actions as values
    # render_template
    pass


if __name__ == '__main__':
    app.run()
