import os

from flask import Flask, request, session, render_template
from flask_sslify import SSLify
from bokeh.resources import CDN

from utils import install_secret_key, load_world, save_world, make_custom_js
from data_plotting import build_game_data_plots

app = Flask(__name__)
sslify = SSLify(app)
install_secret_key(app)


@app.route('/')
def init(is_reset=False):
    if not os.path.exists("worlds"):
        raise Exception("Admin, please create the 'worlds' directory to save worlds!")
    world = load_world()
    num_turns = len(world.solar_park.generation)
    available_tokens = [world.available_tokens(i) for i in range(num_turns)]
    max_tokens = int(max(available_tokens))
    turn_hours = [str(h).rjust(2, "0") for h in range(9, 9+num_turns)]

    safe_js = make_custom_js(world.charging_stations, max_tokens, world.current_step)
    data_plots_html, data_plots_js = build_game_data_plots(world)

    return render_template("board.html", **dict(world=world),
                           num_turns=num_turns,
                           available_tokens=available_tokens,
                           max_tokens=max_tokens,
                           turn_hours=turn_hours,
                           safe_js=safe_js,
                           resetted_the_game=is_reset,
                           bokeh_css_resources=CDN.render_css(),
                           bokeh_js_resources=CDN.render_js(),
                           data_plots_html=data_plots_html,
                           data_plots_js=data_plots_js)


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

    num_turns = len(world.solar_park.generation)
    available_tokens = [world.available_tokens(i) for i in range(num_turns)]
    max_tokens = int(max(available_tokens))
    turn_hours = [str(h).rjust(2, "0") for h in range(9, 9+num_turns)]

    if world.current_step < num_turns:
        safe_js = make_custom_js(world.charging_stations, max_tokens, world.current_step)
    else:
        safe_js = ""
    data_plots_html, data_plots_js = build_game_data_plots(world)

    return render_template("board.html", **dict(world=world),
                           num_turns=num_turns,
                           available_tokens=available_tokens,
                           max_tokens=max_tokens,
                           completed_a_move=True,
                           move_summary=move_summary,
                           turn_hours=turn_hours,
                           safe_js=safe_js,
                           bokeh_css_resources=CDN.render_css(),
                           bokeh_js_resources=CDN.render_js(),
                           data_plots_html=data_plots_html,
                           data_plots_js=data_plots_js)


@app.route('/reset', methods=['GET'])
def reset():
    world = load_world()
    world.reset()
    save_world(world)
    return init(is_reset=True)


@app.route('/new', methods=['GET'])
def new():
    if "world_id" in session:
        del session["world_id"]
    return init(is_reset=True)


if __name__ == '__main__':
    app.run()
