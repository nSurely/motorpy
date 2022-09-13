from datetime import datetime
from pydantic import Field
from typing import Optional

from .enums import PolicyGroup

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

    @property
    def rate_per_km(self) -> Optional[float]:
        """
        The rate per km for the policy.

        Returns:
            The rate per km for the policy. None, if rates do not apply to the policy.
        """
        if not self.rates.rates_active:
            return None
        return self.final.final_rates.final_rates_value

    @property
    def rate_per_mile(self) -> Optional[float]:
        """
        The rate per mile for the policy.

        Returns:
            The rate per mile for the policy. None, if rates do not apply to the policy.
        """
        if not self.rates.rates_active:
            return None
        return self.final.final_rates.final_rates_value * 1.60934

    @property
    def premium_amount(self) -> float:
        """
        The premium amount for the policy.
        """
        return self.final.final_base_premium.final_base_premium_value

    async def driver_approve(self, refresh=True) -> None:
        """
        Approve the the policy on behalf of the driver.

        Args:
            refresh: Refresh the policy after approval.
        """
        self._check_id()

        body = {
            "driver": {
                "agreedAt": datetime.utcnow().isoformat()
            }
        }

        await self.api.request("PATCH", f"policies/{self.id}", body=body)
        if refresh:
            await self.refresh()
    
    async def internal_approve(self, refresh=True, approved_by_id: str = None) -> None:
        """
        Approve the the policy internally.

        Args:
            refresh: Refresh the policy after approval.
        """
        self._check_id()

        body = {
            "approval": {
                "approvedAt": datetime.utcnow().isoformat()
            }
        }
        if approved_by_id:
            body["approval"]["approvedBy"] = approved_by_id

        await self.api.request("PATCH", f"policies/{self.id}", body=body)
        if refresh:
            await self.refresh()
    
    async def cancel(self, refresh=True, message: str = None) -> None:
        """
        Cancel the policy.

        Args:
            refresh: Refresh the policy after cancellation.
        """
        self._check_id()

        body = {
            "cancellation": {
                "cancelledAt": datetime.utcnow().isoformat()
            }
        }
        if message:
            body["cancellation"]["message"] = message

        await self.api.request("PATCH", f"policies/{self.id}", body=body)
        if refresh:
            await self.refresh()

    def _check_id(self) -> None:
        if not self.id:
            raise ValueError("id must be set.")

    async def refresh(self) -> None:
        """
        Refresh the model from the API.
        """
        self._check_id()
        api = self.api
        self.__init__(
            **(await self.api.request("GET",
                                      f"/policy/{self.id}")),
            api=api
        )

    async def delete(self) -> None:
        """
        Delete this record via the API.
        """
        self._check_id()
        await self.api.request(
            "DELETE",
            f"/policy/{self.id}"
        )

    async def save(self, fields: dict = None) -> Optional[dict]:
        """
        Persist any changes in the API.

        Args:
            fields (dict, optional): the API formatted fields to update. If not supplied, any set fields in the model will be updated in the API. Defaults to None.
        """
        self._check_id()

        return await self._save(
            url=f"/policy/{self.id}",
            fields=fields,
            exclude=None
        )

    async def update(self, persist: bool = False, **kwargs) -> None:
        """
        Update a field on the model, call save or keyword persist to persist changes in the API.

        When updating nested fields, you must call update on the nested object.
        Call save here when done updating a nested object.

        Args:
            persist (bool): whether to persist the changes to the API. Defaults to False.
            **kwargs: the model fields to update.

        Note: when doing multiple updates, it is recommended to call update() after all updates are made.
        """
        await self._update(persist=persist, **kwargs)

    async def create(self,
                     api_handler,
                     record_id: str,
                     driver_id: str = None,
                     vehicle_id: str = None) -> 'Policy':
        """
        Create a policy.

        Note: it is best to create a policy on the desired object (eg. vehicle, driver)

        Args:
            api (APIHandler): api handler
            record_id (str): record id, to place policy on
            group (PolicyGroup): policy group
            policy (Policy, optional): policy to create. This can be left None and a new policy will be created using the org defaults. Defaults to None.
            driver_id (str, optional): driver id, required for some fleet policies. Defaults to None.
            vehicle_id (str, optional): vehicle id, required for some fleet policies. Defaults to None.

        For policy groups:

        - d (driver): record ID is the driver ID
        - rv (vehicle): record ID is the vehicle ID
        - drv (driver): record ID is the driver vehicle ID
        - fd (fleet driver): record ID is the fleet ID, and driver_id is the driver ID
        - frv (fleet vehicle): record ID is the fleet ID, and vehicle_id is the vehicle ID
        - fdrv (fleet driver vehicle): record ID is the fleet ID, and driver_id and vehicle_id are the driver and vehicle IDs

        Returns:
            Policy: created policy
        """
        params = {}

        if self.policy_group == PolicyGroup.D:
            # * D
            if driver_id is not None:
                # just in case the driver id is not the same as the record id
                record_id = driver_id if record_id != driver_id else record_id
        elif self.policy_group == PolicyGroup.DRV:
            # * DRV
            # record id is all that is needed
            pass
        elif self.policy_group == PolicyGroup.RV:
            # * RV
            pass
        elif self.policy_group == PolicyGroup.FD:
            # * FD
            if driver_id is None:
                raise ValueError("driver_id must be supplied for FD policies")
            params["driverId"] = driver_id

            if record_id == driver_id:
                raise ValueError(
                    "record_id (fleet id) must not be the same as driver_id for FD policies")
        elif self.policy_group == PolicyGroup.FDRV:
            # * FDRV
            if driver_id is None:
                raise ValueError(
                    "driver_id must be supplied for FDRV policies")
            if vehicle_id is None:
                raise ValueError(
                    "vehicle_id must be supplied for FDRV policies")
            params["driverId"] = driver_id
            params["vehicleId"] = vehicle_id

            if record_id == driver_id or record_id == vehicle_id:
                raise ValueError(
                    "record_id (fleet id) must not be the same as driver_id or vehicle_id for FDRV policies")
        elif self.policy_group == PolicyGroup.FRV:
            # * FRV
            if vehicle_id is None:
                raise ValueError(
                    "vehicle_id must be supplied for FRV policies")

            if record_id == vehicle_id:
                raise ValueError(
                    "record_id (fleet id) must not be the same as vehicle_id for FRV policies")

            params["vehicleId"] = vehicle_id

        res = await api_handler.request("POST",
                                        f"policy/{record_id}",
                                        params=params,
                                        data=self.dict(
                                            by_alias=True,
                                            exclude_unset=True
                                        ))
        # reset with the new policy created by the API
        self.__init__(api=api_handler, **res)
        return self
