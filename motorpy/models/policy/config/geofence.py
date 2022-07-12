import enum
from pydantic import BaseModel, Field, validator
from typing import List, Tuple, Optional
from ..update import Mutable

# * geofence


class GeoType(str, enum.Enum):
    """GeoType enum."""
    POLYGON = "Polygon"


class GeofencePolygon(BaseModel):
    type: GeoType = Field(
        "Polygon",
        description="The type of the geometry object. The value must be `Polygon`.",
    )
    coordinates: List[Tuple[float, float]] = Field(
        ...,
        description="An array of coordinates that defines the perimeter of the polygon. The first and last coordinates in the array must be the same.",
    )

    @validator("coordinates")
    def validate_coordinates(cls, v: Optional[List[List[Tuple[float, float]]]]):
        if v is None:
            return v
        if len(v) < 3:
            raise ValueError(
                f"Polygon coordinates must have at least 3 points, got {len(v)}"
            )
        if v[0] != v[-1]:
            raise ValueError(
                f"Polygon coordinates must have the same first and last points, got {v[0]} and {v[-1]}"
            )
        return v


class PolicyGeofenceBase(BaseModel, Mutable):
    geofence_active: bool = Field(
        default=False,
        alias="enabled",
        description="""
If the policy is active in geofence.
"""
    )
    geofence_polygons: Optional[dict] = Field(
        default_factory=lambda: dict(),
        alias="polygons",
        description="""List of polygons for this policy to be valid within."""
    )


class PolicyGeofenceCreate(PolicyGeofenceBase):
    pass


class PolicyGeofenceUpdate(PolicyGeofenceBase):
    pass


class PolicyGeofenceRead(PolicyGeofenceBase):
    pass

    class Config:
        allow_population_by_field_name = True
