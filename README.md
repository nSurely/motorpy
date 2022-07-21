# MotorPy

MotorPy provides a simple interface to the Inaza Motor APIs.

The goal of motorpy and other Inaza libraries and SDKs are to provide a layer of abstraction above the core Inaza services. By doing so, new solutions can be created in a shorter period of time as common areas such as auth, API routing and data parsing is taken care of.

---

## Installation

`pip install motorpy`

---

## Usage

```python
import motorpy

# set your authorization method
auth = motorpy.Auth(
    api_key="<<key>>",
    api_secret="<<secret>"
)

# create a Motor object that interacts with Inaza's Motor APIs
motor = motorpy.Motor(
    org_id="<<org id>>",
    auth=auth,
    region="eu-1"
)

# the Motor object will return pydantic models with convenience methods
driver = motor.get_driver("2c299d7f-7cc3-4e1b-8810-ae180c971c75")

print(driver.full_name()) # John Doe

print(driver.get_primary_billing_account()) # {...}
```