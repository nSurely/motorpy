.. motorpy documentation master file, created by
   sphinx-quickstart on Mon Jul 18 17:16:12 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to motorpy's documentation!
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Getting Started
===================================

.. code-block:: python
   :linenos:

   import motorpy
   import asyncio

   async def main():
      # create an Auth object
      # here we are using an API key
      auth = motorpy.Auth(api_key="<<my api key>>")

      # pass auth to the Motor object
      # auth is now scoped on this Motor object
      async with motorpy.Motor(org_id='my-org-id', auth=auth, region="eu-1") as motor:
         # as an example, we are iterating over drivers in the system
         async for driver in motor.list_drivers(max_records=10):
            print(driver.first_name) # John Doe
   
   if __name__ == "__main__":
      asyncio.run(main())


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



Motor
===================

The Motor object should be set **once** per application.

.. automodule:: motorpy.base
   :members: Motor




Auth
===================
.. automodule:: motorpy.auth
   :members: Auth


Using an API Key:

.. code-block:: python
   :linenos:

   import motorpy

   # set your API key
   auth = motorpy.Auth(
      api_key="<<key>>"
   )

Using JWT auth for a User (not recommended):

.. code-block:: python
   :linenos:

   import motorpy

   # set your API key
   auth = motorpy.Auth(
      email="<<email>>",
      password="<<password>",
      account_type="user"
   )

Using JWT auth for a Driver (not recommended):

.. code-block:: python
   :linenos:

   import motorpy

   # set your API key
   auth = motorpy.Auth(
      email="<<email>>",
      password="<<password>",
      account_type="driver"
   )


Models
===================
.. automodule:: motorpy.models
   :members: Driver, BillingAccount, BillingEvent, Policy, Vehicle, VehicleType, DriverVehicle, Fleet, FleetVehicle, FleetDriver, FleetDriverVehicleAssignment

