import os
import sys
import random
import time
import pickle
import uuid
from typing import Dict

import pandas as pd
from flask import session

from attendance import make_attendance_grid, custom_default_grid
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
    session_location = "worlds/%s.pickle" % session["world_id"]
    if not os.path.exists(session_location):
        init_world()
        session_location = "worlds/%s.pickle" % session["world_id"]
        print("Creating new world %s" % session["world_id"])
    else:
        print("Loading world %s" % session["world_id"])
    with open(session_location, "rb") as world_pickle:
        world = pickle.load(world_pickle)
    return world


def save_world(world: World):
    if "world_id" not in session:
        raise Exception("You have a world but no world_id. That should not happen.")
    print("Saving world %s" % session["world_id"])
    with open("worlds/%s.pickle" % session["world_id"], "wb") as world_pickle:
        pickle.dump(world, world_pickle)


def init_charging_stations() -> Dict[str, ChargingStation]:
    """Initialise charging stations with capacities and car attendance.
    Attendance is a list stating the car number at each turn.
    An attendance grid is a list of attendance for each charging station"""
    default_attendance_grid = custom_default_grid()
    attendance_grid = make_attendance_grid(default_attendance_grid)
    stations = dict()
    for station_i, attendance_station in enumerate(attendance_grid):
        station_id = "ChargingStation%s" % int(station_i)
        stations[station_id] = ChargingStation(station_id=station_id,
                                               capacity=random.randint(2, 5),
                                               attendances=attendance_station)
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


def make_custom_js(charging_stations, max_tokens, current_turn):
    safe_js = f"""
        <script type='text/javascript'>
        True = true;
        False = false;
        
        function update_market() {{
            for (i = 0; i < $('#my_input_market').val(); i++) {{
                $('#token-holder-' + i).html('<i class="icon-token"></i>');
            }}
            for (i = $('#my_input_market').val(); i < {max_tokens}; i++) {{
                $('#token-holder-' + i).html('');
            }}
        }}
        
        function update_station_tokens(station_id, turn_j) {{
            
            car_target = parseInt($('#car-at-station-' + station_id + '-' + turn_j).data("target"));
            car_current = parseInt($('#car-at-station-' + station_id + '-' + turn_j).data("current"));
            car_change = parseInt($('#my_input_' + station_id).val());
            car_id = $('#car-at-station-' + station_id + '-' + turn_j).data("car_id");
            
            token_string = '';
            for (i = 0; i < (car_current + car_change); i++) {{
                if (i < car_current) {{
                    token_string += '<i class="icon-token ' + car_id + '"></i>';                    
                }} else {{
                    token_string += '<i class="icon-token"></i>';
                }}
            }}
            if (car_change > 0) {{
                for (i = 0; i < (car_target - (car_current + car_change)); i++) {{
                    token_string += '<i class="icon-token-empty"></i>';
                }}
            }} else {{
                for (i = 0; i < -car_change; i++) {{
                    token_string += '<i class="icon-token-empty ' + car_id + '"></i>';
                }}
                for (i = 0; i < (car_target - car_current); i++) {{
                    token_string += '<i class="icon-token-empty"></i>';
                }}
            }}
            $('#token-holder-station-' + station_id + '-{current_turn}').html(token_string);
        }}
    
        function update_all_station_actions() {{    
    """
    for station_id, station in charging_stations.items():
        safe_js = safe_js + f"""
            car_target = parseInt($('#car-at-station-' + '{station_id}' + '-' + {current_turn}).data("target"));
            car_current = parseInt($('#car-at-station-' + '{station_id}' + '-' + {current_turn}).data("current"));
            car_change = parseInt($('#my_input_' + '{station_id}').val());
            if (car_change < {station.capacity} &&
                car_current + car_change < car_target &&
                $('#my_input_market').val() > 0) {{
                $('#add_one_' + '{station_id}').prop("disabled", false);
            }} else {{
                $('#add_one_' + '{station_id}').prop("disabled", true);
            }}
            if (-car_change < {station.capacity} &&
                car_current + car_change > 0 &&
                $('#my_input_market').val() < {max_tokens}) {{
                $('#remove_one_' + '{station_id}').prop("disabled", false);
            }} else {{
                $('#remove_one_' + '{station_id}').prop("disabled", true);
            }}
            $('[data-toggle="tooltip"]').tooltip("hide");
    """
    safe_js = safe_js + f"""
        }}
    """
    
    for station_id, station in charging_stations.items():
        if station.has_car_at(step=current_turn):
            safe_js = safe_js + f"""
                $('#add_one_{station_id}').click(function() {{
                    $('#my_input_{station_id}').val(function(i, val) {{ return +val+1 }});
                    $('#my_input_market').val(function(i, val) {{ return +val-1 }});
                    update_market();
                    update_station_tokens('{station_id}', '{current_turn}');
                    update_all_station_actions();
                }});
                $('#remove_one_{station_id}').click(function() {{
                    $('#my_input_{station_id}').val(function(i, val) {{ return +val-1 }});
                    $('#my_input_market').val(function(i, val) {{ return +val+1 }});
                    update_market();
                    update_station_tokens('{station_id}', '{current_turn}');
                    update_all_station_actions();
                }});
            """
    safe_js = safe_js + "</script>"
    return safe_js
