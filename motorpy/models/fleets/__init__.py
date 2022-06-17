from pydantic import Field
from typing import Optional, List, Any
from motorpy.models import PrivateAPIHandler
from motorpy.models.risk import Risk
from datetime import datetime
from motorpy.models.constants import LANG


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

    def get_tags(self) -> Optional[List[str]]:
        """Get the tags for the fleet."""
        return self.tags.split(",") if self.tags else None

    def update_field(self, field: str, value: Any, persist: bool = False) -> None:
        """
        Update a field on the fleet model, call update to persist changes in the API.
        
        Args:
            field (str): the field to update
            value (Any): the value to set the field to
            persist (bool): whether to persist the changes to the API. Defaults to False.
        
        Note: when doing multiple updates, it is recommended to call update() after all updates are made.
        """
        self.__setattr__(field, value)
        self.__fields_set__.add(field)
        if persist:
            self.update()

    def update(self, fields: dict = None) -> Optional[dict]:
        """
        Update the fleet via the API.

        Args:
            fields (dict, optional): the API formatted fields to update. If not supplied, any set fields in the model will be updated in the API. Defaults to None.
        """
        return self.api.request(
            "PATCH",
            f"/fleets/{self.id}",
            json=self.dict(
                by_alias=True,
                exclude={'_api', 'id'},
                skip_defaults=True,
                exclude_unset=True
            ) if not fields else fields
        )
    
    def refresh(self) -> None:
        """
        Refresh the fleet model from the API.
        """
        self.__init__(self.api.request("GET", f"/fleets/{self.id}"))
    
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
    
