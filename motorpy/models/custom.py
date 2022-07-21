from pydantic import BaseModel, Field
from typing import Any, Optional, Set


class CustomBaseModel(BaseModel):
    # pass
    def dict(self, **kwargs):
        hidden_fields = set(
            attribute_name
            for attribute_name, model_field in self.__fields__.items()
            if model_field.field_info.extra.get("hidden") is True
        )
        kwargs.setdefault("exclude", hidden_fields)
        return super().dict(**kwargs)


class PrivateAPIHandler(CustomBaseModel):
    """
    This api handler is for private use only.
    It allows multiple models to reference the same API with the same credentials.
    """
    # private
    # ! workaround: this is Any type because pydantic Field doesn't support assignment in other models
    # this will always be None or api.APIHandler
    api: Any = Field(
        default=None,
        include=False,
        hidden=True
    )

    class Config:
        allow_populatiion_by_field_name = True

    async def _update(self, persist: bool = False, **kwargs) -> None:
        """
        Update a field on the model, call update to persist changes in the API.
        This tracks what has changed and only updates the API if something has changed or is set.

        Args:
            persist (bool): whether to persist the changes to the API. Defaults to False.
            **kwargs: the model fields to update.

        Note: when doing multiple updates, it is recommended to call update() after all updates are made.
        """
        if not kwargs:
            return
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)
            self.__fields_set__.add(key)
        if persist:
            await self._save()

    async def _save(self, url: str, fields: dict = None, exclude: Set[str] = None, params: dict = None) -> Optional[dict]:
        """
        Update via the API.

        Args:
            fields (dict, optional): the API formatted fields to update. If not supplied, any set fields in the model will be updated in the API. Defaults to None.
        """
        if not self.api:
            raise ValueError("APIHandler not set.")
        if not exclude:
            exclude = set()
        data = self.dict(
            by_alias=True,
            exclude={'api', 'id', 'created_at'}.union(exclude),
            exclude_defaults=True,
            exclude_unset=True
        ) if not fields else fields
        if not data:
            return
        return await self.api.request(
            "PATCH",
            url,
            data=data,
            params=params
        )
