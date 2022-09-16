"""
# MotorPy  

MotorPy is the python library for the **Inaza Motor API**.

---  

## Basic Usage  

```python
import motorpy
import asyncio

async def main():
    # with context manager
    async with motorpy.Motor(org_id='my-org-id',
                             region="eu-1") as motor:
        # perform actions here...
        org_settings = await motor.org_settings()
        print(org_settings) # OrgSettings object

if __name__ == "__main__":
    asyncio.run(main())

```

## Authentication

```python	
import motorpy
import asyncio

async def main():
    # create an Auth object
    auth = motorpy.Auth(api_key="<<my api key>>")

    # pass auth to the Motor object
    # auth is now scoped on this Motor object   
    async with motorpy.Motor(org_id='my-org-id', auth=auth, region="eu-1") as motor:
	    # as an example, we are iterating over drivers in the system
	    async for driver in motor.list_drivers(max_records=10):
		    print(driver.first_name) # John Doe

if __name__ == "__main__":
    asyncio.run(main())

```
  
"""


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