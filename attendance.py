# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 16:06:41 2018

@author: Daphne
"""

import random
from numpy.random import choice
from typing import List


NUMBER_OF_CARS = range(3, 7)
DURATION_OF_STAY = range(1, 8)
TIME_OF_ARRIVAL = range(0, 8)
average_num_cars = 5
CHARGING_STATIONS = 4
SIMULATION_TIME = 8

# Numerical probabilities (don't worry about normalising here)
prob_num_cars = [0.3, 0.4, 0.5, 0.3]
prob_duration = [0.01, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1]
prob_arrival = [0.9, 0.6, 0.4, 0.3, 0.8, 0.4, 0.1, 0.01]

# Normalise probabilities
prob_num_cars = [float(i) / sum(prob_num_cars) for i in prob_num_cars]
prob_duration = [float(i)/sum(prob_duration) for i in prob_duration]
prob_arrival = [float(i) / sum(prob_arrival) for i in prob_arrival]


def empty_grid() -> List[List[int]]:
    """No cars here"""
    default_attendance_grid = [[0 for _ in range(SIMULATION_TIME)] for _ in range(CHARGING_STATIONS)]
    return default_attendance_grid


def custom_default_grid() -> List[List[int]]:
    """Always let one car arrive at one of the charging stations at the first turn, staying there for 4 turns"""
    attendance_grid = empty_grid()
    station_i = choice(range(CHARGING_STATIONS))
    for turn_j in range(4):
        attendance_grid[station_i][turn_j] = 1
    return attendance_grid


def make_attendance_grid(attendance_grid: List[List[int]] = empty_grid()) -> List[List[int]]:
    """Add cars to the grid according to our global probability distributions"""
    starting_car_number = max(max(attendance_station_i) for attendance_station_i in attendance_grid) + 1
    num_cars = choice(NUMBER_OF_CARS, p=prob_num_cars) - (starting_car_number-1)
    for c in range(starting_car_number, num_cars + starting_car_number):
        car_arrival = choice(TIME_OF_ARRIVAL, p=prob_arrival)
        car_duration = choice(DURATION_OF_STAY, p=prob_duration)
        car_departure = min(car_arrival+car_duration, SIMULATION_TIME)
        for station_i in range(CHARGING_STATIONS):
            if all(v == 0 for v in attendance_grid[station_i][car_arrival:car_departure]):  # Station is free
                for turn_j in range(car_arrival, car_departure):
                    attendance_grid[station_i][turn_j] = c
                break
    return attendance_grid
