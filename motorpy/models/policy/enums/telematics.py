import enum


class PolicyTelematicsProcess(str, enum.Enum):
    NONE = "none"
    INDEFINITE = "indefinite"
    MIN_KM = "min_km"
    DAYS = "days"
