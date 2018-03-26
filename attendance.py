# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 16:06:41 2018

@author: Daphne
"""

import random
from numpy.random import choice
from typing import List


DURATION_OF_STAY = range(1, 8)
prob_duration = [0.01, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1]  # Don't worry about normalising here
prob_arrival = [0.9, 0.6, 0.4, 0.2, 0.6, 0.4, 0.1, 0.01]  # Don't worry about normalising here
average_num_cars = 3.5
CHARGING_STATIONS = 4
SIMULATION_TIME = 8

# Normalise probabilities
prob_duration = [float(i)/sum(prob_duration) for i in prob_duration]
prob_arrival = [float(i) / sum(prob_arrival) for i in prob_arrival]


def make_attendance_grid() -> List[List[int]]:

    attendance_grid = [[0 for _ in range(CHARGING_STATIONS)] for _ in range(SIMULATION_TIME)]

    cars = 0
    for i in range(SIMULATION_TIME):
        val = random.uniform(0, 1)
        if val < prob_arrival[i] * average_num_cars:
            cars = cars + 1
            cars_available = 1
            duration_of_stay = choice(DURATION_OF_STAY, p=prob_duration)
            charge_station = 0
            while cars_available > 0 and charge_station < CHARGING_STATIONS:
                if attendance_grid[i][charge_station] == 0:
                    for stay in range(duration_of_stay):
                        if i + stay < SIMULATION_TIME:
                            attendance_grid[i + stay][charge_station] = cars
                            cars_available = cars_available - 1
                            
                charge_station = charge_station + 1
                
    return attendance_grid                    
