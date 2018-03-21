import os
import sys
import random
import time
import pickle
import uuid
from typing import Dict

import pandas as pd
from flask import session

from attendance import make_attendance_grid
from models import World, ChargingStation


def init_world():
    """Make a new world for this session and save it.
    We save and load the world as pickles (it's a hackathon!)."""
    world_id = uuid.uuid4()
    print("Initialising world %s" % world_id)
    random.seed(time.time())
    solar_generation = pd.read_pickle("march9-9to16-8by8.pickle").forecast
    stations = init_charging_stations()
    world = World(solar_generation, stations)
    session["world_id"] = world_id
    save_world(world)


def load_world() -> World:
    """Load an existing or otherwise new world"""
    if "world_id" not in session:
        init_world()
    print("Loading world %s" % session["world_id"])
    with open("worlds/%s.pickle" % session["world_id"], "rb") as world_pickle:
        world = pickle.load(world_pickle)
    return world


def save_world(world: World):
    if "world_id" not in session:
        raise Exception("You have a world but no world_id. That should not happen.")
    print("Saving world %s" % session["world_id"])
    with open("worlds/%s.pickle" % session["world_id"], "wb") as world_pickle:
        pickle.dump(world, world_pickle)


def init_charging_stations() -> Dict[str, ChargingStation]:
    """We believe Daphne that attendances will not collide or be interrupted."""
    attendance_grid = make_attendance_grid()
    stations = dict()
    attendance_df = pd.DataFrame(attendance_grid)
    for col in attendance_df.columns:
        station_id = "ChargingStation%s" % int(col)
        stations[station_id] = ChargingStation(station_id=station_id,
                                               capacity=random.randint(2, 5),
                                               attendances=list(attendance_df.loc[:, col].values))
    return stations


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


def make_custom_js(num_stations, num_turns, current_imbalance_coins, max_imbalance, max_capacity, station_has_car):

    safe_js = f"""
        <script type='text/javascript'>
        True = true;
        False = false;
        
        function update_market() {{
            for (i = 0; i < $('#my_input_market').val(); i++) {{
                $('#token-holder-' + i).html('<i class="icon-token"></i>');
            }}
            for (i = $('#my_input_market').val(); i < {max_imbalance}; i++) {{
                $('#token-holder-' + i).html('');
            }}
        }}
        
        function update_station(station_i, turn_j, station_max, max_imbalance) {{
            
            car_target = parseInt($('#target-station-' + station_i).data("target"));
            car_current = parseInt($('#target-station-' + station_i).data("current"));
            car_change = parseInt($('#my_input_' + station_i + '_' + turn_j).val());
            car_id = $('#target-station-' + station_i).data("car_id");
            
            tokenstring = '';
            for (i = 0; i < (car_current + car_change); i++) {{
                if (i < car_current) {{
                    tokenstring += '<i class="icon-token ' + car_id + '"></i>';                    
                }} else {{
                    tokenstring += '<i class="icon-token"></i>';
                }}
            }}
            // $('#remove_one_' + station_i + '_' + turn_j).html(tokenstring);
            // tokenstring = '';
            if (car_change > 0) {{
                for (i = 0; i < (car_target - (car_current + car_change)); i++) {{
                    tokenstring += '<i class="icon-token-empty"></i>';
                }}
            }} else {{
                for (i = 0; i < -car_change; i++) {{
                    tokenstring += '<i class="icon-token-empty ' + car_id + '"></i>';
                }}
                for (i = 0; i < (car_target - car_current); i++) {{
                    tokenstring += '<i class="icon-token-empty"></i>';
                }}
            }}
            // $('#add_one_' + station_i + '_' + turn_j).html(tokenstring);
            $('#token-holder-station-' + station_i).html(tokenstring);
            
            if (car_change < station_max && car_current + car_change < car_target && $('#my_input_market').val() > 0) {{
                $('#add_one_' + station_i + '_' + turn_j).addClass('btn-success').prop("disabled", false);
            }} else {{
                $('#add_one_' + station_i + '_' + turn_j).removeClass('btn-success').prop("disabled", true);
            }}
            if (-car_change < station_max && car_current + car_change > 0 && $('#my_input_market').val() < max_imbalance) {{
                $('#remove_one_' + station_i + '_' + turn_j).addClass('btn-danger').prop("disabled", false);
            }} else {{
                $('#remove_one_' + station_i + '_' + turn_j).removeClass('btn-danger').prop("disabled", true);
            }}
            
        }}
    """
    for i in range(num_stations):
        for j in range(num_turns):
            safe_js = safe_js + f"""
                $('#add_one_{i}_{j}').click(function() {{
                    $('#my_input_{i}_{j}').val(function(i, val) {{ return +val+1 }});
                    $('#my_input_market').val(function(i, val) {{ return +val-1 }});
                    update_market();
                    for (station_i = 0; station_i < {num_stations}; station_i++) {{
                        station_has_car = {station_has_car};
                        if (station_has_car[station_i]) {{
                            update_station(station_i, {j}, {max_capacity[i]}, {max_imbalance});
                        }}                        
                    }}
                }});
                $('#remove_one_{i}_{j}').click(function() {{
                    $('#my_input_{i}_{j}').val(function(i, val) {{ return +val-1 }});
                    $('#my_input_market').val(function(i, val) {{ return +val+1 }});
                    update_market();
                    for (station_i = 0; station_i < {num_stations}; station_i++) {{
                        station_has_car = {station_has_car};
                        if (station_has_car[station_i]) {{
                            update_station(station_i, {j}, {max_capacity[i]}, {max_imbalance});
                        }}                        
                    }}
                }});
            """
    safe_js = safe_js + "</script>"
    return safe_js
