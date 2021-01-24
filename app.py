# -*- coding: utf-8 -*-

from models import Vehicle, ParkingLot

input_str = "Welcome to the parking lot application.\n" +\
            "Please enter the input filepath. If the file is present in the" +\
            " same directory, just enter the filename.\n"
                   
filepath = input(input_str)

with open(filepath, 'r') as inp:
    commands = inp.readlines()


lot = None

for command_line in commands:
    command = command_line.strip().split()
    if not command:
        print("Empty line found")
        
    elif command[0] == "Create_parking_lot":
        try:
            num_slots = int(command[1])
        except:
            print("Please provide a positive integer as argument")
            
        if type(num_slots) == int and num_slots <= 0:
            print("Please provide a positive integer as argument")
        lot = ParkingLot(num_slots)
        print(f"Created parking of {num_slots} slots")
    
    # No commands will be run unless there is a valid parking lot
    elif not lot:
        print("Please create a parking lot first")
        
    elif command[0] == "Park":
        vehicle_num = command[1]
        driver_age = int(command[3])
        vehicle = Vehicle(vehicle_num, driver_age)
        print(lot.park_vehicle(vehicle))
        
    elif command[0] == "Leave":
        print(lot.empty_slot(int(command[1])))
        
    elif command[0] == "Vehicle_registration_number_for_driver_of_age":
        print(lot.get_vehicle_nums_by_driver_age(int(command[1])))
        
    elif command[0] == "Slot_numbers_for_driver_of_age":
        print(lot.get_slot_nums_by_driver_age(int(command[1])))
    
    elif command[0] == "Slot_number_for_car_with_number":
        print(lot.get_slot_num_by_vehicle_num(command[1]))
    
    else:
        print("Did not understand")
        
    
    





