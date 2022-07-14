from pydantic import Field
from typing import Optional, List, Union, Generator
import motorpy.models as models
# from motorpy.models.risk import Risk
from datetime import datetime
from motorpy.models.constants import LANG
from .drivers import FleetDriver
from .vehicles import FleetVehicle
from .assigned import FleetDriverVehicleAssignment


class Fleet(models.PrivateAPIHandler):
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
    risk: models.risk.Risk = Field(
        default=models.risk.Risk(),
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
    risk: models.risk.Risk = Field(
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

    def _check_id(self) -> None:
        if not self.id:
            raise ValueError("id must be set.")

    def refresh(self) -> None:
        """
        Refresh the model from the API.
        """
        self._check_id()
        api = self.api
        self.__init__(
            **self.api.request("GET",
                               f"/fleets/{self.id}"),
            api=api
        )

    def delete(self) -> None:
        """
        Delete this record via the API.
        """
        self._check_id()
        self.api.request(
            "DELETE",
            f"/fleets/{self.id}"
        )

    def save(self, fields: dict = None) -> Optional[dict]:
        """
        Persist any changes in the API.

        Args:
            fields (dict, optional): the API formatted fields to update. If not supplied, any set fields in the model will be updated in the API. Defaults to None.
        """
        self._check_id()

        return self._save(
            url=f"/fleets/{self.id}",
            fields=fields,
            exclude={'vehicle_type'}
        )

    def update(self, persist: bool = False, **kwargs) -> None:
        """
        Update a field on the model, call save or keyword persist to persist changes in the API.

        Args:
            persist (bool): whether to persist the changes to the API. Defaults to False.
            **kwargs: the model fields to update.

        Note: when doing multiple updates, it is recommended to call update() after all updates are made.
        """
        self._update(persist=persist, **kwargs)

    def get_parent(self) -> Optional['Fleet']:
        """
        Get the parent fleet of the current fleet.
        """
        if not self.has_parent():
            return None
        return Fleet(api=self.api, **self.api.request("GET", f"/fleets/{self.parent_id}"))

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
        driver = FleetDriver(api=self.api, **driver_res)
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
        return FleetDriver(api=self.api, **self.api.request(
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
            yield FleetDriver(api=self.api, **d)

    def assign_vehicle(self, vehicle_id: str, is_active: bool = True, is_open_to_all: bool = True) -> FleetVehicle:
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
        return FleetVehicle(api=self.api, **self.api.request(
            "POST",
            f"/fleets/{self.id}/vehicles",
            data=data
        ))

    def remove_vehicle(self, vehicle_id: str) -> None:
        """Remove a vehicle from the fleet

        Args:
            vehicle_id (str): the vehicle ID
        """
        self.api.request(
            "DELETE", f"/fleets/{self.id}/vehicles/{vehicle_id}"
        )

    def update_vehicle_assignment(self,
                                  vehicle_id: str,
                                  is_active: bool = True,
                                  is_open_to_all: bool = True) -> FleetVehicle:
        """Update a vehicle assignment

        Args:
            vehicle_id (str): the vehicle ID
            is_active (bool, optional): if active in the fleet. Defaults to True.
            is_open_to_all (bool, optional): if open to all drivers. Defaults to True.

        Returns:
            dict: the API response
        """
        data = {
            "isActive": is_active,
            "isOpenToAll": is_open_to_all
        }
        return FleetVehicle(api=self.api, **self.api.request(
            "PATCH",
            f"/fleets/{self.id}/vehicles/{vehicle_id}",
            data=data
        ))

    def list_vehicles(self) -> Generator[FleetVehicle, None, None]:
        """List the vehicles in the fleet

        Returns:
            Generator[FleetVehicle, None, None]: the vehicle assignments
        """
        for v in self.api.batch_fetch(f"/fleets/{self.id}/vehicles"):
            yield FleetVehicle(api=self.api, **v)

    def list_policies(self) -> Generator['models.policies.Policy', None, None]:
        """List all policies for this fleet.

        Returns:
            Generator[Policy, None, None]: policies
        """
        for p in self.api.batch_fetch(f"policy", params={"fleetIds": self.id}):
            yield models.policies.Policy(api=self.api, **p)


Fleet.update_forward_refs()
