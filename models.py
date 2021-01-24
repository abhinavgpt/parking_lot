# -*- coding: utf-8 -*-
from enum import Enum
from heapq import heappop, heappush, heapify
from collections import defaultdict


class slot_state(Enum):
    """
    Enum for states of a slot
    """
    VACANT = 0
    OCCUPIED = 1


class Vehicle:
    """
    Class that has information about a vehicle and its driver
    Inputs: vehicle_num: A string containing the vehicle number in decided format
            driver_age: A positive integer showing the driver's age
    """
    def __init__(self, vehicle_num, driver_age):
        self.vehicle_num = vehicle_num
        self.driver_age = driver_age
 
       
class Slot:
    """
    Class to model a Parking Slot
    Inputs: slot_num: A positive integer
    """
    
    def __init__(self, slot_num):
        self.slot_num = slot_num
        self.state = slot_state.VACANT
        self.vehicle = None
    
    def add_vehicle(self, vehicle):
        """
        Marks a slot as OCCUPIED and saves the vehicle 
        """
        self.state = slot_state.OCCUPIED
        self.vehicle = vehicle
        return
    
    def leave(self):
        """
        Marks the slot as empty
        """
        self.state = slot_state.VACANT
        self.vehicle = None
        return
    

class ParkingLot:
    """
    Class to model a ParkingLot
    Inputs: num_slots: A positive integer denoting the number of slots in the lot
    """
    def __init__(self, num_slots):
        self.__num_slots = num_slots
        self.__slots = [Slot(i) for i in range(1, num_slots+1)]
        
        # Heap can be used to keep track of the nearest slot
        self.__empty_slots = [slot.slot_num for slot in self.__slots]
        heapify(self.__empty_slots)
        
        # A dictionary for mapping between vehicle number and slot number
        self.__vehicle_num_mapping = {}
        
        # Two dictionaries for mapping of driver's age to vehicle number & slot number
        # The values of keys are sets that allow for quick lookups, inserts and deletes
        self.__driver_vehicle_num_mapping = defaultdict(set)
        self.__driver_slot_mapping = defaultdict(set)
        
    
    def get_empty_slot(self):
        """
        Returns the nearest empty slot
        Returns None if parking lot is full
        """
        if not self.__empty_slots:
            return None
        slot_id = heappop(self.__empty_slots)
        slot = self.__slots[slot_id-1]
        return slot
    
    def park_vehicle(self, vehicle):
        """
        Assigns a vehicle to the nearest slot. 
        Checks whether the parking lot is full or the vehicle is already in the lot
        Inputs: vehicle: a Vehicle object
        Returns: a string message to be displayed
        """
        if vehicle.vehicle_num in self.__vehicle_num_mapping:
            return f"Vehicle with registration number \"{vehicle.vehicle_num}\"" +\
                    " is already parked in the parking lot"
        
        slot = self.get_empty_slot()
        if not slot:
            return "Sorry, the parking lot is currently full. Please come back" +\
                   " after some time"
        
        slot.add_vehicle(vehicle)
        self.__vehicle_num_mapping[vehicle.vehicle_num] = slot.slot_num
        self.__driver_vehicle_num_mapping[vehicle.driver_age].add(vehicle.vehicle_num)
        self.__driver_slot_mapping[vehicle.driver_age].add(slot.slot_num)
        return f"Car with vehicle registration number \"{vehicle.vehicle_num}\"" + \
               f" has been parked at slot number {slot.slot_num}"
    
    def empty_slot(self, slot_num):
        """
        Removes vehicle from a given slot
        Checks whether the slot exists in the parking lot and if it is empty
        Returns: a string message to be displayed
        """
        if not 1 <= slot_num <= self.__num_slots:
            return "Slot does not exist in the parking lot"
        
        slot = self.__slots[slot_num-1]
        if slot.state == slot_state.VACANT:
            return f"Slot {slot.slot_num} is already vacant"
        
        
        vehicle = slot.vehicle
        slot.leave()
        del self.__vehicle_num_mapping[vehicle.vehicle_num]
        self.__driver_vehicle_num_mapping[vehicle.driver_age].remove(vehicle.vehicle_num)
        self.__driver_slot_mapping[vehicle.driver_age].remove(slot_num)
        heappush(self.__empty_slots, slot_num)
        return f"Slot number {slot_num} vacated, the car with vehicle registration" +\
               f" number \"{vehicle.vehicle_num}\" left the space, the driver of the" +\
               f" car was of age {vehicle.driver_age}"
    
    def get_vehicle_nums_by_driver_age(self, driver_age):
        """
        Returns a message showing all the vehicle numbers parked by drivers
        of the given age
        """
        vehicle_nums = self.__driver_vehicle_num_mapping[driver_age]
        if not vehicle_nums:
            return f"No vehicles found for driver of age {driver_age}"
        vehicle_nums_joined = ", ".join(vehicle_num for vehicle_num in vehicle_nums)
        return vehicle_nums_joined
    
    def get_slot_nums_by_driver_age(self, driver_age):
        """
        Returns a message showing all the slot numbers in which drivers of the  
        given age have parked their cars
        """
        slot_nums = self.__driver_slot_mapping[driver_age]
        if not slot_nums:
            return f"No slots found for driver of age {driver_age}"
        slot_nums_joined = ", ".join(str(slot_num) for slot_num in slot_nums)
        return slot_nums_joined
    
    def get_slot_num_by_vehicle_num(self, vehicle_num):
        """
        Returns a message showing slot numbers in which a car with the given 
        registration number is parked
        """
        if vehicle_num in self.__vehicle_num_mapping:
            slot_num = self.__vehicle_num_mapping[vehicle_num]
            return slot_num
        return f"Car with vehicle registration number \"{vehicle_num}\"" +\
               f" is not present in the parking lot"
