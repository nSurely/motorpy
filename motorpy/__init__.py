# docs config
__pdoc__ = {
    "tests": False,
    "actions": False,
    "api": False,
    "util": False,
    "models.billing.tests": False,
    "models.drivers.tests": False,
    "models.fleets.tests": False,
    "models.policy.tests": False,
    "models.policy.tests": False
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