from pydantic import BaseModel, Field, conint
from ..update import Mutable

# * extras - repairs


class PolicyExtrasRepairsBase(BaseModel, Mutable):
    extras_repairs_enforce_approved_suppliers: bool = Field(
        default=False,
        alias="enforceApprovedSuppliers",
        title="Extras repairs enforce approved suppliers",
        description="""If true, then the policy will be cancelled if the supplier is not approved."""
    )
    extras_repairs_courtesy_vehicle: bool = Field(
        default=False,
        alias="courtesyVehicle",
        title="Extras repairs courtesy vehicle",
        description="""If true, then the policy will be cancelled if the vehicle is not in courtesy."""
    )


class PolicyExtrasRepairs(PolicyExtrasRepairsBase):
    pass

    class Config:
        allow_population_by_field_name = True

# * extras - alarm


class PolicyExtrasAlarmBase(BaseModel, Mutable):
    extras_alarm_enforce: bool = Field(
        default=False,
        alias="enforce",
        title="Extras alarm enforce",
        description="""If true, then the policy will be cancelled if the alarm is not working."""
    )


class PolicyExtrasAlarm(PolicyExtrasAlarmBase):
    pass

    class Config:
        allow_population_by_field_name = True

# * extras - breakdown


class PolicyExtrasBreakdownBase(BaseModel, Mutable):
    extras_breakdown_cover: bool = Field(
        default=False,
        alias="cover",
        title="Extras breakdown cover",
        description="""If true, then the policy will be cancelled if the vehicle is broken down."""
    )
    extras_breakdown_cover_limit: conint(ge=0) = Field(
        default=0,
        alias="coverLimit",
        title="Extras breakdown cover limit",
        description="""How many times the policy can be cancelled if the vehicle is broken down."""
    )
    extras_breakdown_cost: conint(ge=0) = Field(
        default=0,
        alias="cost",
        title="Extras breakdown cost",
        description="""Additional cost added to the policy."""
    )


class PolicyExtrasBreakdown(PolicyExtrasBreakdownBase):
    pass

    class Config:
        allow_population_by_field_name = True

# * extras - rescue


class PolicyExtrasRescueBase(BaseModel, Mutable):
    extras_rescue_cover: bool = Field(
        default=False,
        alias="cover",
        title="Extras rescue cover",
        description="""If true, then rescue is added to the policy."""
    )
    extras_rescue_cover_limit: conint(ge=0) = Field(
        default=0,
        alias="coverLimit",
        title="Extras rescue cover limit",
        description="""How many times the policy can be cancelled if the vehicle is in a rescue."""
    )
    extras_rescue_cost: conint(ge=0) = Field(
        default=0,
        alias="cost",
        title="Extras rescue cost",
        description="""Additional cost added to the policy."""
    )


class PolicyExtrasRescue(PolicyExtrasRescueBase):
    pass

    class Config:
        allow_population_by_field_name = True

# * extras - theft


class PolicyExtrasTheftBase(BaseModel, Mutable):
    extras_theft_cover: bool = Field(
        default=False,
        alias="cover",
        title="Extras theft cover",
        description="""If true, then theft cover is added to the policy."""
    )
    extras_theft_cover_limit: conint(ge=0) = Field(
        default=0,
        alias="coverLimit",
        title="Extras theft cover limit",
        description="""How many times the policy can be cancelled if the vehicle is stolen."""
    )
    extras_theft_cost: conint(ge=0) = Field(
        default=0,
        alias="cost",
        title="Extras theft cost",
        description="""Additional cost added to the policy."""
    )


class PolicyExtrasTheft(PolicyExtrasTheftBase):
    pass

    class Config:
        allow_population_by_field_name = True

# * extras - key_recovery


class PolicyExtrasKeyRecoveryBase(BaseModel, Mutable):
    extras_key_cover: bool = Field(
        default=False,
        alias="cover",
        title="Extras key cover",
        description="""If true, then key recovery cover is added to the policy."""
    )
    extras_key_cover_limit: conint(ge=0) = Field(
        default=0,
        alias="coverLimit",
        title="Extras key cover limit",
        description="""How many times the policy can be cancelled if the amount of recoveries exceed this amount."""
    )
    extras_key_cost: conint(ge=0) = Field(
        default=0,
        alias="cost",
        title="Extras key cost",
        description="""Additional cost added to the policy."""
    )


class PolicyExtrasKeyRecovery(PolicyExtrasKeyRecoveryBase):
    pass

    class Config:
        allow_population_by_field_name = True

# * extras - windscreen


class PolicyExtrasWindscreenBase(BaseModel, Mutable):
    extras_windscreen_cover: bool = Field(
        default=False,
        alias="cover",
        title="Extras windscreen cover",
        description="""If true, then windscreen cover is added to the policy."""
    )
    extras_windscreen_cost: conint(ge=0) = Field(
        default=0,
        alias="cost",
        title="Extras windscreen cost",
        description="""Additional cost added to the policy."""
    )


class PolicyExtrasWindscreen(PolicyExtrasWindscreenBase):
    pass

    class Config:
        allow_population_by_field_name = True
