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

   # set your authorization method
   auth = motorpy.Auth(
      api_key="<<key>>",
      api_secret="<<secret>"
   )

   # create a Motor object that makes requests to Inaza's Motor APIs
   motor = motorpy.Motor(
      org_id="<<org id>>",
      auth=auth,
      region="eu-1"
   )

   # the Motor object will return pydantic models with convenience methods
   driver = motor.get_driver("2c299d7f-7cc3-4e1b-8810-ae180c971c75")

   print(driver.full_name()) # John Doe

   print(driver.get_primary_billing_account()) # {...}



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
      api_key="<<key>>",
      api_secret="<<secret>"
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

