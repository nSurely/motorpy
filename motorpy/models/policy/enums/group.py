import enum


class PolicyGroup(str, enum.Enum):
    D = "d"
    DRV = "drv"
    RV = "rv"
    FD = "fd"
    FDRV = "fdrv"
    FRV = "frv"
