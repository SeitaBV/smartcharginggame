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
    num_turns = len(world.solar_park.generation)
    # production = world.solar_park.generation
    # consumption = world.demand
    available_tokens = [world.available_tokens(i) for i in range(num_turns)]
    max_tokens = int(max(available_tokens))
    turn_hours = [str(h).rjust(2, "0") for h in range(9, 9+num_turns)]

    safe_js = make_custom_js(world.charging_stations, max_tokens, world.current_step)

    return render_template("dashboard.html", **dict(world=world),
                           num_turns=num_turns,
                           current_turn=current_turn,
                           available_tokens=available_tokens,
                           max_tokens=max_tokens,
                           turn_hours=turn_hours,
                           safe_js=safe_js,
                           resetted_the_game=is_reset)


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
    num_turns = len(world.solar_park.generation)
    # production = world.solar_park.generation
    # consumption = world.demand
    available_tokens = [world.available_tokens(i) for i in range(num_turns)]
    max_tokens = int(max(available_tokens))
    turn_hours = [str(h).rjust(2, "0") for h in range(9, 9+num_turns)]

    if current_turn < num_turns:
        safe_js = make_custom_js(world.charging_stations, max_tokens, world.current_step)
    else:
        safe_js = ""

    return render_template("dashboard.html", **dict(world=world),
                           num_turns=num_turns,
                           current_turn=current_turn,
                           available_tokens=available_tokens,
                           max_tokens=max_tokens,
                           completed_a_move=True,
                           move_summary=move_summary,
                           turn_hours=turn_hours,
                           safe_js=safe_js)


@app.route('/reset', methods=['GET'])
def reset():
    if "world_id" in session:
        del session["world_id"]
    return init(is_reset=True)


if __name__ == '__main__':
    app.run()
