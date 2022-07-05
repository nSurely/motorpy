from pydantic import BaseModel, Field
from datetime import date
from typing import Optional



class PolicyDriverBase(BaseModel):
    # -- * driver
    # -- * esignature
    driver_esignature: Optional[str] = Field(
        alias="esignature",
        description="The driver's electronic signature"
    )
    # exclude from tree search
    driver_esignature_fingerprint: Optional[dict] = Field(
        alias="esignatureFingerprint",
        description="The driver's electronic signature fingerprint"
    )
    # -- * agreed by policy holder(driver)
    driver_policy_agreed_at: Optional[date] = Field(
        alias="agreedAt",
        description="The date the driver agreed to the policy"
    )


class PolicyDriver(PolicyDriverBase):
    pass

    class Config:
        allow_population_by_field_name = True
