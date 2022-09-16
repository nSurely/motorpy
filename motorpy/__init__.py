# docs config
__pdoc__ = {
    "motorpy.tests": False,
    "motorpy.actions": False,
    "motorpy.api": False,
    "motorpy.util": False,
    "motorpy.models.billing.tests": False,
    "motorpy.models.drivers.tests": False,
    "motorpy.models.fleets.tests": False,
    "motorpy.models.policy.tests": False,
    "motorpy.models.policy.tests": False
}

# core class for motorpy
from motorpy.base import Motor

from motorpy.api.exceptions import *

# auth needed for API requests
from motorpy.auth import Auth

# for advanced search on some methods
from motorpy.search import Search

# data models used to interact with records in the API
from motorpy.models import (
    Driver,
    Vehicle,
    DriverVehicle,
    VehicleType,
    Policy,
    BillingAccount,
    BillingEvent,
    Fleet,
    FleetDriver,
    FleetVehicle,
    CommonRisk
)