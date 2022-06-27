from pydantic import Field
from typing import Optional, List, Union, Generator
from motorpy.models import PrivateAPIHandler
from motorpy.models.risk import Risk
from datetime import datetime
from motorpy.models.constants import LANG
from .drivers import FleetDriver


class Fleet(PrivateAPIHandler):
    """
    Fleet model
    """
    id: str = Field(default=...)
    external_id: Optional[str] = Field(
        default=None,
        alias="externalId"
    )
    display: str = Field(
        alias="display"
    )
    description: Optional[str] = Field(
        default=None,
        alias="description"
    )
    tags: Optional[str] = Field(
        default=None,
        alias="tags"
    )
    is_active: bool = Field(
        default=True,
        alias="isActive"
    )
    requires_driver_assignment: bool = Field(
        default=False,
        alias="requiresDriverAssignment"
    )
    base_premium_billing_proc: str = Field(
        default="self",
        alias="basePremiumBillingProc"
    )
    rates_billing_proc: str = Field(
        default="self",
        alias="ratesBillingProc"
    )
    parent_id: Optional[str] = Field(
        default=None,
        alias="parentId"
    )
    created_at: datetime = Field(
        default=datetime.now(),
        alias="createdAt"
    )
    translations: dict = Field(
        default={},
        alias="translations"
    )
    risk: Risk = Field(
        default=Risk(),
        alias="risk"
    )
    vehicle_count: int = Field(
        default=0,
        alias="vehicleCount"
    )
    driver_count: int = Field(
        default=0,
        alias="driverCount"
    )
    sub_fleet_count: int = Field(
        default=0,
        alias="subFleetCount"
    )
    risk: Risk = Field(
        default=None,
        alias="risk"
    )

    class Config:
        allow_population_by_field_name = True

    def _get_translation(self, key: str, lang: str = None) -> str:
        """Get the translation for the given key, optionally restricting to a specific language."""
        if not lang:
            return self.__getattribute__(key)
        if lang not in LANG:
            raise ValueError(f"{lang} is not a valid language code")
        val = self.translations.get(key, {}).get(lang, None)
        if val:
            return val
        return self.__getattribute__(key)

    def get_display(self, lang: str = None) -> str:
        """Get the display name for the fleet, optionally restricting to a specific language.

        Args:
            lang (str, optional): the ISO language code to retrieve. Defaults to None.

        Raises:
            ValueError: invalid language code

        Returns:
            str: the display name for the fleet. If language is not specified, the display name for the default language is returned.
        """
        return self._get_translation("display", lang)

    def get_description(self, lang: str = None) -> str:
        """Get the description for the fleet, optionally restricting to a specific language.

            Args:
                lang (str, optional): the ISO language code to retrieve. Defaults to None.

            Raises:
                ValueError: invalid language code

            Returns:
                str: the description for the fleet. If language is not specified, the description for the default language is returned.
            """
        return self._get_translation("description", lang)

    def has_parent(self) -> bool:
        """Check if the fleet has a parent fleet."""
        return self.parent_id is not None

    def get_tags(self) -> List[str]:
        """Get the tags for the fleet."""
        return self.tags.split(",") if self.tags else []

    def update(self, persist: bool = False, **kwargs) -> None:
        """
        Update a field on the fleet model, call update to persist changes in the API.

        Args:
            field (str): the field to update
            value (Any): the value to set the field to
            persist (bool): whether to persist the changes to the API. Defaults to False.

        Note: when doing multiple updates, it is recommended to call update() after all updates are made.
        """
        if not kwargs:
            return
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)
            self.__fields_set__.add(key)
        if persist:
            self.save()

    def save(self, fields: dict = None) -> Optional[dict]:
        """
        Update the fleet via the API.

        Args:
            fields (dict, optional): the API formatted fields to update. If not supplied, any set fields in the model will be updated in the API. Defaults to None.
        """
        data = self.dict(
            by_alias=True,
            exclude={'api', 'id'},
            skip_defaults=True,
            exclude_unset=True
        ) if not fields else fields
        print(data)
        if not data:
            return
        return self.api.request(
            "PATCH",
            f"/fleets/{self.id}",
            data=data
        )

    def refresh(self) -> None:
        """
        Refresh the fleet model from the API.
        """
        api = self.api
        self.__init__(**self.api.request("GET", f"/fleets/{self.id}"), api=api)

    def delete(self) -> None:
        """
        Delete the fleet via the API.
        """
        self.api.request("DELETE", f"/fleets/{self.id}")

    def get_parent(self) -> Optional['Fleet']:
        """
        Get the parent fleet of the current fleet.
        """
        if not self.has_parent():
            return None
        return Fleet(**self.api.request("GET", f"/fleets/{self.parent_id}"))

    def assign_driver(self,
                      driver_id: str,
                      is_vehicle_manager: bool = False,
                      is_driver_manager: bool = False,
                      is_billing_manager: bool = False,
                      expires_at: datetime = None,
                      is_active: bool = True,
                      vehicle_ids: List[str] = None,
                      vehicle_expires_at: Union[List[datetime], datetime] = None) -> FleetDriver:
        """Assign a driver to the fleet

        Args:
            driver_id (str): the driver ID
            is_vehicle_manager (bool, optional): can manage vehicles. Defaults to False.
            is_driver_manager (bool, optional): can manage drivers. Defaults to False.
            is_billing_manager (bool, optional): can manage billing details. Defaults to False.
            expires_at (datetime, optional): if and when the driver assignment expires. Defaults to None.
            is_active (bool, optional): if active in the fleet. Defaults to True.
            vehicle_ids (List[str], optional): the vehicle IDs to assign to the driver. Defaults to None.
            vehicle_expires_at (List[datetime], optional): the vehicle assignment expiration dates. Defaults to None.
                Note: Supply a single datetime for all vehicles, or a list of datetimes for each vehicle.

        Returns:
            FleetDriver: the API response
        """
        if vehicle_ids is None:
            vehicle_ids = []
        data = {
            "driverId": driver_id,
            "isVehicleManager": is_vehicle_manager,
            "isDriverManager": is_driver_manager,
            "isBillingManager": is_billing_manager,
            "expiresAt": expires_at.isoformat() if expires_at else None,
            "isActive": is_active
        }
        driver_res = self.api.request(
            "POST",
            f"/fleets/{self.id}/drivers",
            data=data
        )
        driver = FleetDriver(**driver_res)
        driver.api = self.api

        if not vehicle_ids:
            return driver
        
        try:
            if isinstance(vehicle_expires_at, datetime) or vehicle_expires_at is None:
                for vehicle_id in vehicle_ids:
                    self.api.request(
                        "POST",
                        f"/fleets/{self.id}/drivers/{driver_id}/vehicles/{vehicle_id}",
                        data={
                            "expiresAt": vehicle_expires_at.isoformat() if vehicle_expires_at else None
                        }
                    )
                return driver

            # each vehicle has a different expiration date
            for vehicle_id, expires_at in zip(vehicle_ids, vehicle_expires_at):
                self.api.request(
                    "POST",
                    f"/fleets/{self.id}/drivers/{driver_id}/vehicles/{vehicle_id}",
                    data={
                        "expiresAt": expires_at.isoformat() if expires_at else None
                    }
                )
        except Exception as e:
            # equivalent to a rollback
            self.api.request(
                "DELETE", f"/fleets/{self.id}/drivers/{driver_id}")
            raise e
        return driver

    def remove_driver(self, driver_id: str) -> None:
        """Remove a driver from the fleet

        Args:
            driver_id (str): the driver ID
        """
        self.api.request(
            "DELETE", f"/fleets/{self.id}/drivers/{driver_id}"
        )

    def update_driver_assignment(self,
                                 driver_id: str,
                                 is_vehicle_manager: bool = False,
                                 is_driver_manager: bool = False,
                                 is_billing_manager: bool = False,
                                 expires_at: datetime = None,
                                 is_active: bool = True) -> FleetDriver:
        """Update a driver assignment

        Args:
            driver_id (str): the driver ID
            is_vehicle_manager (bool, optional): can manage vehicles. Defaults to False.
            is_driver_manager (bool, optional): can manage drivers. Defaults to False.
            is_billing_manager (bool, optional): can manage billing details. Defaults to False.
            expires_at (datetime, optional): if and when the driver assignment expires. Defaults to None.
            is_active (bool, optional): if active in the fleet. Defaults to True.

        Returns:
            dict: the API response
        """
        data = {
            "isVehicleManager": is_vehicle_manager,
            "isDriverManager": is_driver_manager,
            "isBillingManager": is_billing_manager,
            "expiresAt": expires_at.isoformat() if expires_at else None,
            "isActive": is_active
        }
        return FleetDriver(**self.api.request(
            "PATCH",
            f"/fleets/{self.id}/drivers/{driver_id}",
            data=data
        ))

    def list_drivers(self) -> Generator[List[FleetDriver], None, None]:
        """List the drivers in the fleet

        Returns:
            List[FleetDriver]: the drivers
        """
        for d in self.api.batch_fetch(f"/fleets/{self.id}/drivers"):
            yield FleetDriver(**d)

    def assign_vehicle(self, vehicle_id: str, is_active: bool = True, is_open_to_all: bool = True) -> dict:
        """Assign a vehicle to the fleet

        Args:
            vehicle_id (str): the vehicle ID
            is_active (bool, optional): if active in the fleet. Defaults to True.
            is_open_to_all (bool, optional): if open to all drivers. Defaults to True.

        Returns:
            dict: the API response
        """
        data = {
            "isActive": is_active,
            "isOpenToAll": is_open_to_all,
            "registeredVehicleId": vehicle_id
        }
        return self.api.request(
            "POST",
            f"/fleets/{self.id}/vehicles",
            data=data
        )
