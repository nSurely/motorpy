from pydantic import BaseModel, Field
from ..update import Mutable
from .components import *


class PolicyExtrasNested(BaseModel, Mutable):
    extras_repairs: PolicyExtrasRepairs = Field(
        default=PolicyExtrasRepairs(),
        alias="repairs",
    )
    extras_alarm: PolicyExtrasAlarm = Field(
        default=PolicyExtrasAlarm(),
        alias="alarm",
    )
    extras_breakdown: PolicyExtrasBreakdown = Field(
        default=PolicyExtrasBreakdown(),
        alias="breakdown",
    )
    extras_rescue: PolicyExtrasRescue = Field(
        default=PolicyExtrasRescue(),
        alias="rescue",
    )
    extras_theft: PolicyExtrasTheft = Field(
        default=PolicyExtrasTheft(),
        alias="theft",
    )
    extras_key_recovery: PolicyExtrasKeyRecovery = Field(
        default=PolicyExtrasKeyRecovery(),
        alias="keyReplacement",
    )
    extras_windscreen: PolicyExtrasWindscreen = Field(
        default=PolicyExtrasWindscreen(),
        alias="windscreen",
    )

    class Config:
        allow_population_by_field_name = True
