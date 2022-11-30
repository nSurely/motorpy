from pydantic import BaseModel, Field
from typing import Any, Optional, Set


class Exporter(BaseModel):
    "Class for exporting models"

    def dict(self,
             exclude: Optional[Set[str]] = None,
             include: Optional[Set[str]] = None,
             by_alias: bool = False,
             exclude_unset: bool = False,
             exclude_defaults: bool = False) -> dict:
        """Export the model as a dict. This will recursively export any nested models.

        Args:
            exclude (Optional[Set[str]], optional): fields to exclude. Defaults to None.
            include (Optional[Set[str]], optional): fields to include. Defaults to None.
            by_alias (bool, optional): whether to use the alias for the field name. Defaults to False.
            exclude_unset (bool, optional): whether to exclude unset fields. Defaults to False.
            exclude_defaults (bool, optional): whether to exclude default fields. Defaults to False.

        Returns:
            dict: a dict of the model.
        """
        _ex_keys = {"api", "api_path"}

        if not exclude:
            exclude = set()

            # hidden_fields = set(
            #     attribute_name
            #     for attribute_name, model_field in self.__fields__.items()
            #     if model_field.field_info.extra.get("hidden") is True
            # )

            # exclude = exclude.union(hidden_fields)
        if not include:
            include = set()

        result = dict()

        for key, value in self.__dict__.items():
            if key in exclude:
                continue
            if key in include:
                result[key] = value
                continue
            if key.startswith("_"):
                continue

            if key not in self.__fields_set__ and exclude_unset:
                continue

            # remove hidden fields here
            if key in _ex_keys:
                continue

            # set key to alias if it exists
            key = self.__fields__[key].alias if by_alias and self.__fields__[key].alias else key

            if isinstance(value, BaseModel):
                result[key] = value.dict(
                    exclude=exclude,
                    include=include,
                    exclude_unset=exclude_unset,
                    exclude_defaults=exclude_defaults,
                    by_alias=by_alias
                )
            else:
                result[key] = value

        return result


class PrivateAPIHandler(Exporter):
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

    api_path: str = Field(
        None,
        include=False,
        hidden=True,
        alias='apiPath'
    )

    class Config:
        allow_populatiion_by_field_name = True

    def get_api_path(self) -> Optional[str]:
        """Get the API path for the model.

        Returns:
            Optional[str]: the API path.
        """
        return self.api_path

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
