# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 15:16:03 2018

@author: Daphne
"""

import itertools
import random
import numpy as np

import simpy
#s = np.random.poisson(5, 10)

RANDOM_SEED = 42
GAS_STATION_SIZE = 200     # liters
THRESHOLD = 10             # Threshold for calling the tank truck (in %)
FUEL_TANK_SIZE = 50        # liters
DURATION_OF_STAY = [1, 4]  # Min/max levels of fuel tanks (in liters)
REFUELING_SPEED = 10        # liters / second
TANK_TRUCK_TIME = 300      # Seconds it takes the tank truck to arrive
T_INTER = [1, 5]        # Create a car every [min, max] hours
SIM_TIME = 100            # Simulation time in seconds


def car(name, env, gas_station, charging_station):
    """A car arrives at the gas station for refueling.

    It requests one of the gas station's fuel pumps and tries to get the
    desired amount of gas from it. If the stations reservoir is
    depleted, the car has to wait for the tank truck to arrive.

    """
    duration_of_stay = random.randint(*DURATION_OF_STAY)
    print('%s arriving at charging station at %.1f' % (name, env.now))
    with gas_station.request() as req:
        start = env.now
        # Request one of the charging stations
        yield req

        # Stay the required amount of time 
        yield charging_station.get(duration_of_stay)

        # The "actual" refueling process takes some time
        yield env.timeout(duration_of_stay)

        print('%s leaves at %.1f hours.' % (name,env.now - start))


def gas_station_control(env, charging_station):
    """Periodically check the level of the *charging_station* and call the tank
    truck if the level falls below a threshold."""
    while True:
        if charging_station.level / charging_station.capacity * 100 < THRESHOLD:
            # We need to call the tank truck now!
            print('Calling tank truck at %d' % env.now)
            # Wait for the tank truck to arrive and refuel the station
            yield env.process(tank_truck(env, charging_station))

        yield env.timeout(10)  # Check every 10 seconds


def tank_truck(env, charging_station):
    """Arrives at the gas station after a certain delay and refuels it."""
    yield env.timeout(TANK_TRUCK_TIME)
    print('Tank truck arriving at time %d' % env.now)
    ammount = charging_station.capacity - charging_station.level
    print('Tank truck refuelling %.1f liters.' % ammount)
    yield charging_station.put(ammount)


def car_generator(env, gas_station, charging_station):
    """Generate new cars that arrive at the gas station."""
    for i in itertools.count():
        yield env.timeout(random.randint(*T_INTER))
        env.process(car('Car %d' % i, env, gas_station, charging_station))


# Setup and start the simulation
print('Gas Station refuelling')
random.seed(RANDOM_SEED)

# Create environment and start processes
env = simpy.Environment()
gas_station = simpy.Resource(env, 3)
charging_station = simpy.Container(env, GAS_STATION_SIZE, init=GAS_STATION_SIZE)
env.process(gas_station_control(env, charging_station))
env.process(car_generator(env, gas_station, charging_station))

# Execute!
env.run(until=SIM_TIME)