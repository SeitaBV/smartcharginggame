import os

from flask import Flask, request, session, render_template
from flask_sslify import SSLify

from utils import install_secret_key, load_world, save_world, make_custom_js

app = Flask(__name__)
sslify = SSLify(app)
install_secret_key(app)


@app.route('/')
def init(is_reset=False):
    if not os.path.exists("worlds"):
        raise Exception("Admin, please create the 'worlds' directory to save worlds!")
    world = load_world()
    current_turn = world.current_step  # We start at turn 0
    transaction_costs = 5  # in number of coins
    num_stations = len(world.charging_stations)
    num_turns = len(world.solar_park.generation)
    production = world.solar_park.generation
    consumption = world.demand
    imbalance = [world.imbalance_at(i) for i in range(num_turns)]
    imbalance_coin = [world.imbalance_coin(i) for i in range(num_turns)]
    max_imbalance = int(max(imbalance_coin))
    station_id = [station for station in world.charging_stations]
    max_capacity = [world.charging_stations.get(station).capacity for station in world.charging_stations]
    turn_id = range(9, 9+num_turns)
    station_has_car = [world.charging_stations.get(station).has_car_at(step=current_turn) for station in world.charging_stations]

    safe_js = make_custom_js(num_stations, num_turns, imbalance_coin[current_turn], max_imbalance, max_capacity, station_has_car)

    return render_template("dashboard.html", **dict(world=world),
                           num_stations=num_stations,
                           num_turns=num_turns,
                           current_turn=current_turn,
                           production=production,
                           consumption=consumption,
                           imbalance=imbalance,
                           imbalance_coin=imbalance_coin,
                           max_imbalance=max_imbalance,
                           max_capacity=max_capacity,
                           station_id=station_id,
                           profit_made=0,
                           turn_id=turn_id,
                           safe_js=safe_js,
                           resetted_the_game=is_reset
                           )


@app.route('/next', methods=['GET', 'POST'])
def next_step():
    world = load_world()
    orders = dict()
    for sid, station in world.charging_stations.items():
        if "order_%s" % sid not in request.form:
            raise Exception("Missing order_%s in request." % sid)
        orders[sid] = int(request.form.get("order_%s" % sid))
    move_summary = world.next_step(orders)
    save_world(world)

    current_turn = world.current_step  # We start at turn 0
    num_stations = len(world.charging_stations)
    num_turns = len(world.solar_park.generation)
    production = world.solar_park.generation
    consumption = world.demand
    imbalance = [world.imbalance_at(i) for i in range(num_turns)]
    imbalance_coin = [world.imbalance_coin(i) for i in range(num_turns)]
    max_imbalance = int(max(imbalance_coin))
    station_id = [station for station in world.charging_stations]
    max_capacity = [world.charging_stations.get(station).capacity for station in world.charging_stations]
    turn_id = range(9, 9+num_turns)
    station_has_car = [world.charging_stations.get(station).has_car_at(step=current_turn) for station in world.charging_stations]

    if current_turn < num_turns:
        safe_js = make_custom_js(len(world.charging_stations), len(world.solar_park.generation),
                                 imbalance_coin[current_turn], max_imbalance, max_capacity, station_has_car)
    else:
        safe_js = ""

    return render_template("dashboard.html", **dict(world=world),
                           num_stations=num_stations,
                           num_turns=num_turns,
                           current_turn=current_turn,
                           production=production,
                           consumption=consumption,
                           imbalance=imbalance,
                           imbalance_coin=imbalance_coin,
                           max_imbalance=max_imbalance,
                           max_capacity=max_capacity,
                           station_id=station_id,
                           completed_a_move=True,
                           move_summary=move_summary,
                           turn_id=turn_id,
                           safe_js=safe_js)


@app.route('/reset', methods=['GET'])
def reset():
    if "world_id" in session:
        del session["world_id"]
    return init(is_reset=True)


if __name__ == '__main__':
    app.run()
