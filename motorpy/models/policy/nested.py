from pydantic import Field
from typing import Optional

from .base import PolicyBase
from .approval import PolicyApproval
from .cancellation import PolicyCancellation
from .config import PolicyConfig
from .contribution import PolicyContribution
from .driver import PolicyDriver
from .duration import PolicyDuration
from .excess import PolicyExcess
from .extras import PolicyExtrasNested
from .fees import PolicyFees
from .final import PolicyFinalPricing
from .issuer import PolicyIssuer
from .noclaims import PolicyNoClaims
from .premium import PolicyBasePremium
from .rates import PolicyRates
from .rewards import PolicyRewards
from .telematics import PolicyTelematics

# for defaults
from .rates import PolicyRates
from .premium import PolicyBasePremium


class Policy(PolicyBase):
    approval: PolicyApproval = Field(
        default=PolicyApproval(),
        alias="approval",
        description="The approval details for the policy"
    )
    cancellation: PolicyCancellation = Field(
        default=PolicyCancellation(),
        alias="cancellation",
        description="The cancellation details for the policy"
    )
    config: PolicyConfig = Field(
        default=PolicyConfig(),
        alias="config",
        description="The configuration details for the policy"
    )
    contribution: PolicyContribution = Field(
        default=PolicyContribution(),
        alias="contribution",
        description="The contribution details for the policy"
    )
    driver: PolicyDriver = Field(
        default=PolicyDriver(),
        alias="driver",
        description="The driver details for the policy"
    )
    duration: PolicyDuration = Field(
        default=PolicyDuration(),
        alias="duration",
        description="The duration details for the policy"
    )
    excess: PolicyExcess = Field(
        default=PolicyExcess(),
        alias="excess",
        description="The excess details for the policy"
    )
    extras: PolicyExtrasNested = Field(
        default=PolicyExtrasNested(),
        alias="extras",
        description="The extras details for the policy"
    )
    fees: PolicyFees = Field(
        default=PolicyFees(),
        alias="fees",
        description="The fees details for the policy"
    )
    final: PolicyFinalPricing = Field(
        default=PolicyFinalPricing(),
        alias="final",
        description="The final details for the policy"
    )
    issuer: PolicyIssuer = Field(
        default=PolicyIssuer(),
        alias="issuer",
        description="The issuer details for the policy"
    )
    noclaims: PolicyNoClaims = Field(
        default=PolicyNoClaims(),
        alias="noClaims",
        description="The no claims details for the policy"
    )
    premium: PolicyBasePremium = Field(
        default=PolicyBasePremium(),
        alias="premium",
        description="The premium details for the policy"
    )
    rates: PolicyRates = Field(
        default=PolicyRates(),
        alias="rates",
        description="The rates details for the policy"
    )
    rewards: PolicyRewards = Field(
        default=PolicyRewards(),
        alias="rewards",
        description="The rewards details for the policy"
    )
    telematics: PolicyTelematics = Field(
        default=PolicyTelematics(),
        alias="telematics",
        description="The telematics details for the policy"
    )

    class Config:
        allow_population_by_field_name = True

    def is_cancelled(self) -> bool:
        """
        Is the policy cancelled?
        """
        return self.cancellation.is_cancelled()
    
    def is_approved(self) -> bool:
        """
        Is the policy approved?
        """
        return self.approval.is_approved()
    
    def is_expired(self) -> bool:
        """
        Is the policy expired?
        """
        return self.duration.is_expired()
    
    def is_driver_agreed(self) -> bool:
        """
        Has the driver agreed to the policy?
        """
        return self.driver.is_agreed()
    
    def is_live(self) -> bool:
        """
        Is the policy live? ie. active, approved, driver agreed, not cancelled and not expired.
        """
        return (
            self.is_active
            and self.is_approved()
            and not self.is_cancelled()
            and not self.is_expired()
            and self.is_driver_agreed()
        )
    
    def rate_per_km(self) -> Optional[float]:
        """
        The rate per km for the policy.

        Returns:
            The rate per km for the policy. None, if rates do not apply to the policy.
        """
        if not self.rates.rates_active:
            return None
        return self.final.final_rates.final_rates_value
    
    def premium_amount(self) -> float:
        """
        The premium amount for the policy.
        """
        return self.final.final_base_premium.base_premium_value
    