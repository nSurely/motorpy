from pydantic import Field
from typing import Optional
from motorpy.models import PrivateAPIHandler
from datetime import date
from enum import Enum
from motorpy.models.risk import CommonRisk


class VehicleCategory(str, Enum):
    """
    The type of vehicle.
    """
    AUTOMOBILE = "automobile"
    MOTORCYCLE = "motorcycle"
    ATV = "atv"
    RAIL = "rail"
    TRANSPORT = "transport"
    AIRCRAFT = "aircraft"
    SEACRAFT = "seacraft"
    TOWED = "towed"
    TRACTOR = "tractor"
    COMMERCIAL = "commercial"
    MILITARY = "military"
    SPECIAL = "special"
    UNKNOWN = "unknown"
    MISC = "misc"


class VehicleType(PrivateAPIHandler, CommonRisk):
    id: str = Field(default=None)
    external_id: Optional[str] = Field(
        default=None,
        alias="externalId"
    )
    display: Optional[str] = Field(
        default=None,
        alias="display",
        title="Display",
        description="Text field for display purposes."
    )
    description: Optional[str] = Field(
        default=None,
        alias="description",
        title="Description",
        description="Extended text field for a description of the vehicle."
    )
    is_active: Optional[bool] = Field(
        default=True,
        alias="isActive",
        title="Is Active",
        description="If this vehicle is active. If not, it will not be returned from the API unless requested."
    )
    vehicle_type: Optional[VehicleCategory] = Field(
        default='unknown',
        alias="vehicleType",
        title="Vehicle Type",
        description="The vehicle type/category. For a list of all available types, see path: GET /variables/vehicle-types"
    )
    variant: Optional[str] = Field(
        default=None,
        alias="variant",
        title="Variant",
        description="A descriptive field for this variant of the make and model, eg. sedan, SUV."
    )
    code: Optional[str] = Field(
        default=None,
        alias="code",
        title="Code",
        description="An additional code tied to the vehicle for internal idenification. This could be a manufacturer's code or risk system."
    )
    base_msrp_new: Optional[float] = Field(
        default=None,
        alias="baseMsrpNew",
        title="MSRP New",
        description="The base manufacturer's suggested retail price (MSRP) when new."
    )
    base_msrp_current: Optional[float] = Field(
        default=None,
        alias="baseMsrpCurrent",
        title="MSRP Current",
        description="The base manufacturer's suggested retail price (MSRP) when not new (preowned)."
    )
    brand: Optional[str] = Field(
        default=None,
        alias="brand",
        title="Brand",
        description="""The vehicle brand. 
        This field is highly important when a driver is selecting their vehicle.
        Make sure all fields have the same case, ie. Audi vs. audi. Otherwise it will be seen as differing brands.
        """
    )
    model: Optional[str] = Field(
        default=None,
        alias="model",
        title="Model",
        description="""The vehicle brand model.
        This field is highly important when a driver is selecting their vehicle.
        Make sure all fields have the same case, ie. A4 vs. a4. Otherwise it will be seen as differing models."""
    )
    year_floor: Optional[int] = Field(
        default=None,
        alias="yearFloor",
        title="Manufacturing Year Floor (First)",
        description="""The first year of production for this vehicle."""
    )
    year_top: Optional[int] = Field(
        default=None,
        alias="yearTop",
        title="Manufacturing Year Top (Final)",
        description="""The final year of production for this vehicle."""
    )
    doors: Optional[int] = Field(
        default=None,
        alias="doors",
        title="Door Count",
        description="The number of doors on this vehicle."
    )
    wheels: Optional[int] = Field(
        default=None,
        alias="wheels",
        title="Wheel Count",
        description="The number of wheels on this vehicle."
    )
    seats: Optional[int] = Field(
        default=None,
        alias="seats",
        title="Seat Count",
        description="The number of seats in this vehicle."
    )
    cylinders: Optional[int] = Field(
        default=None,
        alias="cylinders",
        title="Cylinder Count",
        description="The number of cylinders in this vehicles engine."
    )
    valves: Optional[int] = Field(
        default=None,
        alias="valves",
        title="Valve Count",
        description="The number of valves in this vehicles engine."
    )
    valve_timing: Optional[str] = Field(
        default=None,
        alias="valveTiming",
        title="Valve Timing",
        description="Text field descriptor of valve timing."
    )
    cam_type: Optional[str] = Field(None, alias="camType")
    drive_type: Optional[str] = Field(None, alias="driveType")
    transmission: Optional[str] = Field(None, alias="transmission")
    gear_count: Optional[int] = Field(None, alias="gearCount")
    engine_size_ml: Optional[int] = Field(None, alias="engineSizeML")
    horse_power: Optional[int] = Field(None, alias="horsePower")
    torque_nm: Optional[float] = Field(None, alias="torqueNM")
    engine_type: Optional[str] = Field(None, alias="engineType")
    fuel_type: Optional[str] = Field(None, alias="fuelType")
    fuel_tank_capacity_ml: Optional[int] = Field(
        None, alias="fuelTankCapacityML")
    combined_kmpl: Optional[float] = Field(
        None, alias="combinedKMPL")
    city_kmpl: Optional[float] = Field(
        None, alias="cityKMPL")
    combined_kmple: Optional[float] = Field(
        None, alias="combinedKMPLE")
    city_kmple: Optional[float] = Field(
        None, alias="cityKMPLE")
    kwh_100_km: Optional[float] = Field(None, alias="kwh100KM")
    time_to_charge_240v_mins: Optional[float] = Field(
        None, alias="timeToCharge240vMins")
    electric_range_km: Optional[float] = Field(None, alias="electricRangeKM")
    warranty_basic_years: Optional[int] = Field(
        None, alias="warrantyBasicYears")
    warranty_basic_km: Optional[int] = Field(None, alias="warrantyBasicKM")
    warranty_basic_expiry: Optional[date] = Field(
        None, alias="warrantyBasicExpiry")
    warranty_drivetrain_years: Optional[int] = Field(
        None, alias="warrantyDrivetrainYears")
    warranty_drivetrain_km: Optional[int] = Field(
        None, alias="warrantyDrivetrainKM")
    warranty_drivetrain_expiry: Optional[date] = Field(
        None, alias="warrantyDrivetrainExpiry")
    warranty_roadside_years: Optional[int] = Field(
        None, alias="warrantyRoadsideYears")
    warranty_roadside_km: Optional[int] = Field(
        None, alias="warrantyRoadsideKM")
    warranty_roadside_expiry: Optional[date] = Field(
        None, alias="warrantyRoadsideExpiry")
    warranty_rust_years: Optional[int] = Field(
        None, alias="warrantyRustYears")
    warranty_rust_km: Optional[int] = Field(
        None, alias="warrantyRustKM")
    warranty_rust_expiry: Optional[date] = Field(
        None, alias="warrantyRustExpiry")
    warranty_free_maintenance_years: Optional[int] = Field(
        None, alias="warrantyFreeMaintenanceYears")
    warranty_free_maintenance_km: Optional[int] = Field(
        None, alias="warrantyFreeMaintenanceKM")
    warranty_free_maintenance_expiry: Optional[date] = Field(
        None, alias="warrantyFreeMaintenanceExpiry")
    warranty_hybrid_component_years: Optional[int] = Field(
        None, alias="warrantyHybridComponentYears")
    warranty_hybrid_component_km: Optional[int] = Field(
        None, alias="warrantyHybridComponentKM")
    warranty_hybrid_component_expiry: Optional[date] = Field(
        None, alias="warrantyHybridComponentExpiry")
    warranty_ev_battery_years: Optional[int] = Field(
        None, alias="warrantyEVBatteryYears")
    warranty_ev_battery_km: Optional[int] = Field(
        None, alias="warrantyEVBatteryKM")
    warranty_ev_battery_expiry: Optional[date] = Field(
        None, alias="warrantyEVBatteryExpiry")
    length_mm: Optional[int] = Field(None, alias="lengthMM")
    width_mm: Optional[int] = Field(None, alias="widthMM")
    height_mm: Optional[int] = Field(None, alias="heightMM")
    wheel_base_mm: Optional[int] = Field(None, alias="wheelBaseMM")
    front_track_mm: Optional[int] = Field(None, alias="frontTrackMM")
    rear_track_mm: Optional[int] = Field(None, alias="rearTrackMM")
    ground_clearance_mm: Optional[int] = Field(None, alias="groundClearanceMM")
    angle_of_approach_degrees: Optional[float] = Field(
        None, alias="angleOfApproachDegrees")
    angle_of_departure_degrees: Optional[float] = Field(
        None, alias="angleOfDepartureDegrees")
    turning_circle_m: Optional[float] = Field(None, alias="turningCircleM")
    drag_coefficient: Optional[float] = Field(None, alias="dragCoefficient")
    epa_interior_volume_m3: Optional[float] = Field(
        None, alias="epaInteriorVolumeM3")
    cargo_capacity_m3: Optional[float] = Field(None, alias="cargoCapacityM3")
    max_cargo_capacity_m3: Optional[float] = Field(
        None, alias="maxCargoCapacityM3")
    curb_weight_kg: Optional[float] = Field(None, alias="curbWeightKG")
    gross_weight_kg: Optional[float] = Field(None, alias="grossWeightKG")
    max_payload_kg: Optional[float] = Field(None, alias="maxPayloadKG")
    max_towing_capacity_kg: Optional[float] = Field(
        None, alias="maxTowingCapacityKG")

    class Config:
        allow_population_by_field_name = True
        anystr_strip_whitespace = True

    def _check_id(self) -> None:
        if not self.id:
            raise ValueError("id must be set.")

    def get_display(self) -> str:
        "A simple display string to identify the model to the user."
        return f"{self.brand} {self.model}"

    async def refresh(self) -> None:
        """
        Refresh the model from the API.
        """
        self._check_id()
        api = self.api
        self.__init__(
            **(await self.api.request("GET",
                                      f"/vehicles/{self.id}")),
            api=api
        )

    async def delete(self) -> None:
        """
        Delete this record via the API.
        """
        self._check_id()
        await self.api.request(
            "DELETE",
            f"/vehicles/{self.id}"
        )

    async def save(self, fields: dict = None) -> Optional[dict]:
        """
        Persist any changes in the API.

        Args:
            fields (dict, optional): the API formatted fields to update. If not supplied, any set fields in the model will be updated in the API. Defaults to None.
        """
        self._check_id()

        return await self._save(
            url=f"/vehicles/{self.id}",
            fields=fields,
            exclude=None
        )

    async def update(self, persist: bool = False, **kwargs) -> None:
        """
        Update a field on the model, call save or keyword persist to persist changes in the API.

        Args:
            persist (bool): whether to persist the changes to the API. Defaults to False.
            **kwargs: the model fields to update.

        Note: when doing multiple updates, it is recommended to call update() after all updates are made.
        """
        await self._update(persist=persist, **kwargs)
