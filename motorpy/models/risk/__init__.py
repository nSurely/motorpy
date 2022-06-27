from pydantic import BaseModel, Field


class RiskApplication(BaseModel):
    """
    Risk application model
    """
    inheritance: bool = Field(default=False)
    apply: bool = Field(default=False)


class RiskRetro(BaseModel):
    """
    Risk model
    """
    rates: RiskApplication = Field(default=RiskApplication())
    value: float = Field(default=0.0)
    weighting: float = Field(default=0.0)
    premium: RiskApplication = Field(default=RiskApplication())


class DynamicRisk(BaseModel):
    """
    Dynamic risk model
    """
    apply: bool = Field(default=False)
    process: str = Field(default="std")
    weighting: float = Field(default=0.0)


class Risk(BaseModel):
    """
    Risk model
    """
    lookback: RiskRetro = Field(default=RiskRetro())
    dynamic: DynamicRisk = Field(default=DynamicRisk())
    ihr: RiskRetro = Field(default=RiskRetro())


class CommonRisk(BaseModel):
    risk: Risk = Field(default=None, alias="risk")
