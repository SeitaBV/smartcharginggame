from flask import Flask, request, render_template
from flask_sslify import SSLify
import pandas as pd

from models import World, ChargingStation
from utils import install_secret_key, init_charging_stations, make_custom_js

app = Flask(__name__)
sslify = SSLify(app)
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
    consumption = world.demand
    imbalance = [world.imbalance_at(i) for i in range(num_turns)]
    max_imbalance = int(max(imbalance))
    station_id = [station for station in world.charging_stations]
    max_capacity = [world.charging_stations.get(station).capacity for station in world.charging_stations]
    turn_id = range(9, 9+num_turns)

    safe_js = make_custom_js(num_stations, num_turns)

    return render_template("dashboard.html", **dict(world=world),
                           num_stations=num_stations,
                           num_turns=num_turns,
                           current_turn=current_turn,
                           production=production,
                           consumption=consumption,
                           imbalance=imbalance,
                           max_imbalance=max_imbalance,
                           max_capacity=max_capacity,
                           station_id=station_id,
                           profit_made=0,
                           turn_id=turn_id,
                           safe_js=safe_js
                           )


@app.route('/next', methods=['GET', 'POST'])
def next_step():
    global world
    orders = dict()
    for sid, station in world.charging_stations.items():
        if "order_%s" % sid not in request.form:
            raise Exception("Missing order_%s in request." % sid)
        orders[sid] = int(request.form.get("order_%s" % sid))
    imbalance_change, profit_made = world.next_step(orders)

    current_turn = world.current_step  # We start at turn 0
    transaction_costs = 5  # in number of coins
    num_stations = len(world.charging_stations)
    num_turns = len(world.solar_park.generation)
    production = world.solar_park.generation
    consumption = world.demand
    imbalance = [world.imbalance_at(i) for i in range(num_turns)]
    max_imbalance = int(max(imbalance))
    station_id = [station for station in world.charging_stations]
    max_capacity = [world.charging_stations.get(station).capacity for station in world.charging_stations]
    turn_id = range(9, 9+num_turns)

    safe_js = make_custom_js(len(world.charging_stations), len(world.solar_park.generation))

    return render_template("dashboard.html", **dict(world=world),
                           num_stations=num_stations,
                           num_turns=num_turns,
                           current_turn=current_turn,
                           production=production,
                           consumption=consumption,
                           imbalance=imbalance,
                           max_imbalance=max_imbalance,
                           max_capacity=max_capacity,
                           station_id=station_id,
                           imbalance_change=imbalance_change,
                           profit_made=profit_made,
                           turn_id=turn_id,
                           safe_js=safe_js)


if __name__ == '__main__':
    app.run()
