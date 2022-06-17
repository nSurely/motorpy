from pydantic import BaseModel, Field
from typing import Any


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

    # def connect_api(self, api: api.APIHandler):
    #     "Reset the API connection."
    #     self.api = api
