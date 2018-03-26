from typing import List, Dict, Tuple
import random

import pandas as pd


"""
Models for the scc game. At the moment, we play on a simple 8 by 8 grid.
(eight hours, eight possible charging values)
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

    def get_final_payoff(self) -> int:
        if self.current_charge is 0:
            payoff = -100  # Penalty if you let the car leave empty
        else:
            payoff = 50 * self.current_charge  # Reward for each energy token in the car
        return payoff


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
        self.cars = dict()
        for car_number in [n for n in pd.Series(attendances).drop_duplicates().values if n > 0]:
            car_id = "Car%s" % car_number
            self.cars[car_id] = Car(car_id=car_id, target_charge=random.randint(2, 4))

    def __repr__(self):
        return "<%s: cap:%d att: %s>" % (self.id, self.capacity, self.car_attendances)

    def has_car_at(self, step: int) -> bool:
        if step < 0 or step >= len(self.car_attendances):
            return False
        return self.car_attendances[step] > 0

    def get_car_at(self, step: int):
        if self.has_car_at(step):
            return self.cars["Car%s" % self.car_attendances[step]]


class World:
    """
    The game world. Initialise this to get the rest.
    """

    solar_park: SolarPark
    demand: List[int]
    market_prices: List[int]
    charging_stations: Dict[str, ChargingStation]
    current_step: int
    money: int

    def __init__(self,
                 solar_generation: pd.Series,
                 charging_stations: Dict[str, ChargingStation]):
        assert(solar_generation.size == 8)
        for gen in solar_generation:
            assert(gen in range(1, 9))
        
        self.solar_park = SolarPark(solar_generation)
        self.demand = [7, 7, 5, 3, 6, 6, 7, 2]
        self.market_prices = [100, 60, 30, 15, 8, 4, 2, 1]
        self.charging_stations = charging_stations

        self.current_step = 0
        self.money = 1000

    def __repr__(self):
        return "<step: %d money: %d,\ngeneration: %s,\ndemand: %s,\nstations: %s>"\
               % (self.current_step, self.money, self.solar_park.generation.values, self.demand, self.charging_stations)

    def imbalance_at(self, time_step: int):
        """
        Compute the imbalance at time_step
        """
        charging = 0
        for station in self.charging_stations.values():
            car = station.get_car_at(time_step)
            if car is not None:
                charging += car.charging_actions[time_step]
        generation = self.solar_park.generation.values
        return int(generation[time_step]) - self.demand[time_step] - charging

    def available_tokens(self, time_step: int) -> int:
        """
        Compute the tokens to display at time_step
        """
        return self.imbalance_at(time_step) + 4

    def imbalance(self, until: int=8):
        """Aggregated imbalance up until a time step"""
        return sum([self.imbalance_at(i) for i in range(until)])

    def calculate_profits(self, action: int) -> int:
        result = 0
        index = self.imbalance_at(self.current_step) + 4
        if action > 0:  # buy
            for _ in range(action):
                result -= self.market_prices[index - 1]
                index -= 1
        elif action < 0:  # sell
            for _ in range(abs(action)):
                result += self.market_prices[index]
                index += 1
        return result

    def check_validity_of_orders(self, orders: Dict[str, int]) -> bool:
        combined_action = sum(orders.values())
        if self.imbalance_at(self.current_step) - combined_action not in range(-4, 4):
            raise Exception('Resulting imbalance outside of allowed range')
        for station_id, action in orders.items():
            station = self.charging_stations.get(station_id)
            car = station.get_car_at(self.current_step)
            if action is not 0:
                if car is None:
                    raise Exception('An action is attempted on a station where there is no car: ' + station_id)
                elif abs(action) > station.capacity:
                    raise Exception('Action is larger than station capacity: ' + station_id)
                elif car.current_charge + action < 0:
                    raise Exception('Cars cannot have negative charge: ' + str(car.id))
        return True

    def next_step(self, orders: Dict[str, int]) -> Tuple[int, int]:
        self.check_validity_of_orders(orders)

        # First, get the costs/value of the combined actions
        overall_action = sum(orders.values())
        profits = self.calculate_profits(overall_action)
        self.money += profits
        summary = ""
        if overall_action > 0:
            summary = "Overall you charged %d token(s)." % overall_action
        elif overall_action < 0:
            summary = "Overall you discharged %d token(s)." % -overall_action
        if profits > 0:
            summary += " This earned you %d coins (minus %d coin(s) due to charging inefficiency)."\
                % (profits, -overall_action)
        elif profits < 0:
            summary += " This cost you %d coins, as well as %d coin(s) due to charging inefficiency."\
                % (-profits, overall_action)

        # Now record the action on the cars
        for station_id, action in orders.items():
            station = self.charging_stations.get(station_id)
            car = station.get_car_at(self.current_step)
            if car is not None:
                car.charging_actions[self.current_step] = action
                car.current_charge += action
                if station.get_car_at(self.current_step + 1) != car:
                    # account for payoff when a car leaves
                    final_payoff = car.get_final_payoff()
                    self.money += final_payoff
                    profits += final_payoff
                    if summary != "":
                        summary += "<br/>"
                    summary += "The car at %s left." % station_id
                    if final_payoff > 0:
                        summary += "Your reward for achieving a charge level of %d was %d coins."\
                                   % (car.current_charge, final_payoff)
                    else:
                        summary += "Your penalty for achieving a charge level of %d was %d coins." \
                                   % (car.current_charge, -final_payoff)
                # account transaction costs for charging
                self.money -= abs(action)
                profits -= abs(action)
        self.current_step += 1
        return summary
