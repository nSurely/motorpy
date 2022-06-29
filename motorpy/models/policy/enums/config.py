import enum


class PolicyConfigTemplate(str, enum.Enum):
    CUSTOM = "custom"
    UBI = "ubi"
    STANDARD = "standard"
    TEMPORARY = "temporary"
    TESTING_PERIOD = "testing_period"
