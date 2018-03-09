from typing import List

import pandas as pd

"""
Models for the scc game. At the moment, we play on a simple 8 by 8 grid.
(eight hours, eight possible chargin values)
"""

class SolarPark:
    """
    """
    generation: pd.Series

    def __init__(self, generation: pd.Series):
        self.generation = generation


class ChargingStation:
    """
    An electric vehicle charging station.  
    """

    capacity: int
    arrival_time: int
    leave_time: int
    actions: pd.Series

    def __init__(self, capacity: int, arrival_time: int, leave_time: int):
        self.capacity = capacity
        self.arrival_time = arrival_time
        self.leave_time = leave_time
        self.actions = pd.Series([0] * 8)

    def level_at(self, step: int):
        return sum([self.action[i] for i in range(step)])

    def has_car_at(self, step: int):
        return step > self.arrival_time and step <= self.leave_time


class World:
    """
    The game world. Intialise this to get the rest.
    """

    solar_park: SolarPark
    charging_stations: List[ChargingStation]
    current_step: int

    def __init__(self,
                 solar_generation: pd.Series,
                 charging_stations: List[ChargingStation]):
        assert(solar_generation.size == 8)
        for gen in solar_generation:
            assert(gen in range(1, 9))
        
        self.solar_park = SolarPark(solar_generation)

        self.current_step = 0

    def imbalance_at(self, time_step: int):
        """
        compute the imbalance over the whole game
        """
        imbalance = 0
        charging = sum([cs.action.values[time_step] for cs in self.charging_stations])
        solar = self.solar_park.generation.values[time_step]
        return solar - charging
    
    def imbalance(self, until:int=8):
        return sum([self.imbalance_at(i) for i in range(until)]) 

    def step(self):
        self.current_step += 1

