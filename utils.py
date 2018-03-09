import os
import sys
import random
from typing import List

import pandas as pd

from attendance import make_attendance_grid
from models import ChargingStation


def init_charging_stations() -> List[ChargingStation]:
    """We believe Daphne that attendances will not collide or be interrupted."""
    attendance_grid = make_attendance_grid()
    stations = list()
    attendance_df = pd.DataFrame(attendance_grid)
    for col in attendance_df.columns:
        stations.append(ChargingStation(station_id="ChargingStation%s" % int(col),
                                        capacity=random.randint(2, 5),
                                        attendances=list(attendance_df.loc[:, col].values)))
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
