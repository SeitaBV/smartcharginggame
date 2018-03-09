# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 16:06:41 2018

@author: Daphne
"""

import random
from typing import List


DURATION_OF_STAY = [2, 4]
prob_arrival = [0.5, 0.4, 0.5, 0.2, 0.2, 0.2, 0.9, 0.9, 0.8, 0.6]
CHARGING_STATIONS = 4
SIMULATION_TIME = 8


def make_attendance_grid() -> List[List[int]]:

    attendance_grid = [[0 for _ in range(CHARGING_STATIONS)] for _ in range(SIMULATION_TIME)]

    cars = 0
    for i in range(SIMULATION_TIME):
        val = random.uniform(0, 1)
        if val < prob_arrival[i]:
            cars = cars + 1
            cars_available = 1
            duration_of_stay = random.randint(*DURATION_OF_STAY)
            charge_station = 0
            while cars_available > 0 and charge_station < CHARGING_STATIONS:
                if attendance_grid[i][charge_station] == 0:
                    for stay in range(duration_of_stay):
                        if i + stay < SIMULATION_TIME:
                            attendance_grid[i + stay][charge_station] = cars
                            cars_available = cars_available - 1
                            
                charge_station = charge_station + 1
                
    return attendance_grid                    
