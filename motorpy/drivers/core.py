import core
from auth import Auth


class Drivers(core.MotorBase):

    def __init__(self, org_id: str, auth: Auth, region: str = None, url: str = None) -> None:
        super().__init__(org_id, auth, region, url)

    def get_driver(self, driver_id: str, **query) -> dict:
        """Get a driver record.

        Args:
            driver_id (str): the UUID of the driver.

        Returns:
            dict: the driver record.
        """
        return self.api.request("GET", f"drivers/{driver_id}", params=query)
