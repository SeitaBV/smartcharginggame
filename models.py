from typing import List, Dict
import random

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


class Car:
    id: str
    initial_charge: int
    target_charge: int
    charging_actions: List[int]
    capacity: int
    current_charge: int

    def __init__(self, car_id: str, target_charge: int):
        """ We make some useful simplifications here"""
        self.id = car_id
        self.initial_charge = 0
        self.target_charge = self.capacity = target_charge
        self.charging_actions = [0] * 8
        self.current_charge = 0


class ChargingStation:
    """
    An electric vehicle charging station.
    It can accept one car at a time.
    """
    id: str
    capacity: int
    car_attendances: List[int]  # int-based IDs of attending cars (>0 means attendance)
    cars: Dict[str, Car]
    actions: pd.Series

    def __init__(self, station_id: str, capacity: int, attendances: List[int]):
        """
        We parse attendances, and create cars accordingly.
        """
        self.id = station_id
        self.capacity = capacity
        self.car_attendances = attendances
        for car_number in [n for n in pd.DataFrame(attendances).drop_duplicates() if n > 0]:
            car_id = "Car%s" % car_number
            self.cars[car_id] = Car(car_id=car_id, target_charge=random.randint(2, 4))

    def has_car_at(self, step: int):
        return self.car_attendances[step] > 0

    def get_car_at(self, step: int):
        if self.has_car_at(step):
            return self.cars["Car%s" % self.car_attendances[step]]


class World:
    """
    The game world. Initialise this to get the rest.
    """

    solar_park: SolarPark
    charging_stations: List[ChargingStation]
    current_step: int
    money: int

    def __init__(self,
                 solar_generation: pd.Series,
                 charging_stations: List[ChargingStation]):
        assert(solar_generation.size == 8)
        for gen in solar_generation:
            assert(gen in range(1, 9))
        
        self.solar_park = SolarPark(solar_generation)
        self.charging_stations = charging_stations

        self.current_step = 0
        self.money = 0

    def imbalance_at(self, time_step: int):
        """
        compute the imbalance over the whole game
        """
        charging = sum([cs.actions.values[time_step] for cs in self.charging_stations])
        solar = self.solar_park.generation.values[time_step]
        return solar - charging
    
    def imbalance(self, until: int=8):
        return sum([self.imbalance_at(i) for i in range(until)]) 

    def step(self):
        self.current_step += 1
