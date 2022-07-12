"""
Org Settings. 

This model is stored here and not in the models dir as it is read only and closely related to the API.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class Design(BaseModel):
    primary_hex: str = Field(..., alias='primaryHex')
    secondary_hex: str = Field(..., alias='secondaryHex')
    tertiary_hex: str = Field(..., alias='tertiaryHex')
    font_family_primary: str = Field(..., alias='fontFamilyPrimary')
    font_family_secondary: str = Field(..., alias='fontFamilySecondary')
    font_primary_hex: str = Field(..., alias='fontPrimaryHex')
    font_secondary_hex: str = Field(..., alias='fontSecondaryHex')
    primary_logo_url: str = Field(..., alias='primaryLogoUrl')
    secondary_logo_url: str = Field(..., alias='secondaryLogoUrl')
    primary_logo_url_small: str = Field(..., alias='primaryLogoUrlSmall')
    secondary_logo_url_small: str = Field(..., alias='secondaryLogoUrlSmall')


class Policy(BaseModel):
    policy_drv_on: bool = Field(..., alias='policyDrvOn')
    policy_rv_on: bool = Field(..., alias='policyRvOn')
    policy_driver_on: bool = Field(..., alias='policyDriverOn')
    policy_fleet_on: bool = Field(..., alias='policyFleetOn')


class Features(BaseModel):
    claims_on: bool = Field(..., alias='claimsOn')
    emergencies_on: bool = Field(..., alias='emergenciesOn')
    rewards_on: bool = Field(..., alias='rewardsOn')
    scoring_on: bool = Field(..., alias='scoringOn')
    scoring_leaderboard_on: bool = Field(..., alias='scoringLeaderboardOn')
    billing_on: bool = Field(..., alias='billingOn')
    fleet_on: bool = Field(..., alias='fleetOn')
    fleet_billing_on: bool = Field(..., alias='fleetBillingOn')


class App(BaseModel):
    auto_tracking_on: bool = Field(..., alias='autoTrackingOn')
    ui_layout: int = Field(..., alias='uiLayout')
    show_trips_on: bool = Field(..., alias='showTripsOn')
    signup_on: bool = Field(..., alias='signupOn')


class Telematics(BaseModel):
    auto_tracking: Dict[str, Any] = Field(..., alias='autoTracking')
    data_capture: Dict[str, Any] = Field(..., alias='dataCapture')


class Tos(BaseModel):
    contact_email: str = Field(..., alias='contactEmail')
    require_privacy_agreement: bool = Field(...,
                                            alias='requirePrivacyAgreement')
    privacy_policy_display: str = Field(..., alias='privacyPolicyDisplay')
    privacy_policy_url: str = Field(..., alias='privacyPolicyUrl')
    privacy_policy_html: str = Field(..., alias='privacyPolicyHtml')
    require_tos_agreement: bool = Field(..., alias='requireTosAgreement')
    tos_display: str = Field(..., alias='tosDisplay')
    tos_url: str = Field(..., alias='tosUrl')
    tos_html: str = Field(..., alias='tosHtml')
    dpo_email: str = Field(..., alias='DPOEmail')


class Config(BaseModel):
    default_lang: str = Field(..., alias='defaultLang')
    require_proof_of_address: bool = Field(..., alias='requireProofOfAddress')
    require_id: bool = Field(..., alias='requireId')
    require_selfie: bool = Field(..., alias='requireSelfie')
    require_vehicle_pic_full: bool = Field(..., alias='requireVehiclePicFull')
    require_vehicle_pic_single: bool = Field(...,
                                             alias='requireVehiclePicSingle')
    require_vehicle_proof_of_reg: bool = Field(
        ..., alias='requireVehicleProofOfReg')
    require_drivers_license: bool = Field(..., alias='requireDriversLicense')
    driver_approval: bool = Field(..., alias='driverApproval')
    vehicle_approval: bool = Field(..., alias='vehicleApproval')
    use_vehicle_registry: bool = Field(..., alias='useVehicleRegistry')


class OrgSettings(BaseModel):
    profile_type: Optional[str] = Field(None, alias='profileType')
    source_id_type: Optional[str] = Field(None, alias='sourceIdType')
    design: Optional[Design] = None
    policy: Optional[Policy] = None
    features: Optional[Features] = None
    app: Optional[App] = None
    telematics: Optional[Telematics] = None
    external_id: Optional[str] = Field(None, alias='externalId')
    display_name: Optional[str] = Field(None, alias='displayName')
    env: Optional[str] = None
    is_active: Optional[bool] = Field(None, alias='isActive')
    id: Optional[str] = None
    created_at: Optional[str] = Field(None, alias='createdAt')
    org_group_id: Optional[str] = Field(None, alias='orgGroupId')
    org_group_display_name: Optional[str] = Field(
        None, alias='orgGroupDisplayName')
    default_lang: Optional[str] = Field(None, alias='defaultLang')
    tos: Optional[Tos] = None
    config: Optional[Config] = None
