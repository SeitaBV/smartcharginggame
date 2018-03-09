# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 16:06:41 2018

@author: Daphne
"""

import random


#NUMBER_OF_CARS = [20,30]
DURATION_OF_STAY = [2,4]
prob_arrival = [0.5, 0.4, 0.5, 0.2, 0.2, 0.2, 0.9, 0.9, 0.8, 0.6]
CHARGING_STATIONS = 4
SIMULATION_TIME = 10

ArrivalGrid = [[0 for x in range(CHARGING_STATIONS)] for y in range(SIMULATION_TIME)] 

charging = []
cars=0
arrivals = random.randint(*NUMBER_OF_CARS)
for i in range(SIMULATION_TIME):
    val = random.uniform(0,1)
    if val < prob_arrival[i]:
        cars = cars+1
        cars_available = 1;
        duration_of_stay = random.randint(*DURATION_OF_STAY)
        charg_station = 0
        while cars_available > 0 and charg_station < CHARGING_STATIONS:
            if ArrivalGrid[i][charg_station] == 0:
                for stay in range(duration_of_stay):
                    if i+stay< SIMULATION_TIME:
                        ArrivalGrid[i+stay][charg_station] = cars
                        cars_available = cars_available - 1
                        
            charg_station = charg_station + 1
            
                    
                    
                    
    
    