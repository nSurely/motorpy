from pydantic import BaseModel, Field
from typing import Optional
from ..custom import Exporter


class RiskApplication(BaseModel):
    """
    Risk application model
    """
    inheritance: bool = Field(
        default=False,
        alias="inheritance"
    )
    apply: bool = Field(
        default=False,
        alias="apply"
    )

    class Config:
        allow_population_by_field_name = True


class RiskRetro(BaseModel):
    """
    Risk model
    """
    rates: Optional[RiskApplication] = Field(
        alias="rates"
    )
    value: float = Field(
        default=0.0,
        alias="value"
    )
    weighting: float = Field(
        default=0.0,
        alias="weighting"
    )
    premium: Optional[RiskApplication] = Field(
        alias="premium"
    )

    class Config:
        allow_population_by_field_name = True


class DynamicRisk(BaseModel):
    """
    Dynamic risk model
    """
    apply: bool = Field(
        alias="apply"
    )
    process: str = Field(
        alias="process"
    )
    weighting: float = Field(
        alias="weighting"
    )

    class Config:
        allow_population_by_field_name = True


class Risk(BaseModel):
    """
    Risk model
    """
    lookback: Optional[RiskRetro] = Field(
        alias="lookback"
    )
    dynamic: Optional[DynamicRisk] = Field(
        alias="dynamic"
    )
    ihr: Optional[RiskRetro] = Field(
        alias="ihr"
    )

    class Config:
        allow_population_by_field_name = True


class CommonRisk(Exporter):
    risk: Optional[Risk] = Field(
        alias="risk"
    )

    class Config:
        allow_population_by_field_name = True
