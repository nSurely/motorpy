import enum


class PolicyCoverType(str, enum.Enum):
    COMPREHENSIVE = "comprehensive"
    THIRD_PARTY = "third_party"
    FIRE_THEFT = "fire_theft"
    LIABILITY = "liability"
    MEDICAL = "medical"
    MEDICAL_THIRD_PARTY = "medical_third_party"
    THIRD_PARTY_UNINSURED = "third_party_uninsured"
    THIRD_PARTY_UNDERINSURED = "third_party_underinsured"
    COLLISION = "collision"
    PERSONAL_INJURY = "personal_injury"
