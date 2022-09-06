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
import asyncio

async def main():
    auth = motorpy.Auth(api_key="<<my api key>>")

    async with motorpy.Motor(org_id='my-org-id', auth=auth, region="eu-1") as motor:
        # the Motor object will return pydantic models with convenience methods
        driver = await motor.get_driver("2c299d7f-7cc3-4e1b-8810-ae180c971c75")

        print(driver.full_name()) # "John Doe"

        ba = await driver.get_primary_billing_account()
        print(ba) # <BillingAccount>

if __name__ == "__main__":
    asyncio.run(main())
```  
