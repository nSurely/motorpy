from motorpy import models
import uuid
from datetime import datetime, date


class TestDriverModel:

    def test_driver_model_init_dict(self):
        driver_dict = {
            "id": str(uuid.uuid4()),
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@email.com",
            "dob": "1990-01-01",
            "lang": "en",
            "drivingStartDate": "2020-01-01",
        }

        driver: models.Driver = models.Driver(**driver_dict)
        assert driver.id == driver_dict["id"]
        assert driver.first_name == driver_dict["firstName"]
        assert driver.last_name == driver_dict["lastName"]
        assert driver.email == driver_dict["email"]
        assert type(driver.date_of_birth) == date
        assert driver.date_of_birth == datetime.strptime(driver_dict["dob"], "%Y-%m-%d").date()
        assert driver.language == driver_dict["lang"]
        assert driver.driving_start_date == datetime.strptime(driver_dict["drivingStartDate"], "%Y-%m-%d").date()

