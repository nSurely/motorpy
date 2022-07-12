from pydantic import BaseModel, Field, HttpUrl
from ..update import Mutable


# * terms


class PolicyTermsBase(BaseModel, Mutable):
    terms_url: HttpUrl = Field(
        default=None,
        alias="url",
        title="Terms URL",
        description="""URL to terms and conditions."""
    )
    terms_html: str = Field(
        default=None,
        alias="html",
        title="Terms HTML",
        description="""HTML to terms and conditions."""
    )
    terms_attachments: list = Field(
        default=None,
        alias="attachments",
        title="Terms attachments",
        description="""Attachments to terms and conditions."""
    )
    terms_requires_driver_esignature: bool = Field(
        default=False,
        alias="requiresDriverEsignature",
        title="Terms requires driver esignature",
        description="""Terms requires driver e-signature."""
    )


class PolicyTerms(PolicyTermsBase):
    pass

    class Config:
        allow_population_by_field_name = True
