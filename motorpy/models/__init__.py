from .risk import CommonRisk
from .custom import *
from .billing import BillingAccount, BillingEvent
from .policy import Policy
from .vehicles import VehicleType, Vehicle, DriverVehicle
from .drivers import Driver
from .fleets import FleetVehicle, FleetDriver, Fleet, FleetDriverVehicleAssignment

from typing import Union

# these are trackable assets, each can be used to create a different insurance solution
TrackableAsset = Union[
    # registered vehicle - for tracking a vehicle
    'Vehicle',
    # driver - for insurance tied to a person
    'Driver',
    # DRV - for multiple driver UBI policies
    'DriverVehicle',
    # fleet vehicle - for tracking a vehicle in a fleet
    'FleetVehicle',
    # fleet driver - for tracking a driver in a fleet
    'FleetDriver',
    # fleet driver vehicle assignment - for tracking a driver and vehicle in a fleet
    'FleetDriverVehicleAssignment'
]