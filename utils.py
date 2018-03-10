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


def make_custom_js(num_stations, num_turns):
    safe_js = "<script type='text/javascript'>"
    for i in range(num_turns):
        for j in range(num_stations):
            safe_js = safe_js + "$('#add_one_" + str(i) + "_" + str(j) + "').click(function() {" \
                                                                         "$('#my_counter_" + str(i) + "_" + str(
                j) + "').html(function(i, val) { return +val+1 });" \
                     "$('#my_input_" + str(i) + "_" + str(j) + "').val(function(i, val) { return +val+1 });" \
                                                               "});" \
                                                               "$('#remove_one_" + str(i) + "_" + str(
                j) + "').click(function() {" \
                     "$('#my_counter_" + str(i) + "_" + str(j) + "').html(function(i, val) { return +val-1 });" \
                                                                 "$('#my_input_" + str(i) + "_" + str(
                j) + "').val(function(i, val) { return +val-1 });" \
                     "});"
    safe_js = safe_js + "</script>"
    return safe_js
