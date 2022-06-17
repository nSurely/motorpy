import motorpy.api as api
from pydantic import BaseModel, Field


class CustomBaseModel(BaseModel):
    def dict(self, **kwargs):
        hidden_fields = set(
            attribute_name
            for attribute_name, model_field in self.__fields__.items()
            if model_field.field_info.extra.get("hidden") is True
        )
        kwargs.setdefault("exclude", hidden_fields)
        return super().dict(**kwargs)


class PrivateAPIHandler(CustomBaseModel):
    # private
    _api: api.APIHandler = Field(
        default=None,
        include=False,
        hidden=True
    )

    class Config:
        allow_populatiion_by_field_name = True
