from .base import *
from .generation import *
from .geofence import *
from .terms import *


# class PolicyConfigUpdate(PolicyConfigStandardUpdate):
#     generation: PolicyGenerationUpdate = Field(
#         default=PolicyGenerationUpdate(),
#         alias="generation",
#         description="""
# Policy generation settings.
# """
#     )
#     terms: PolicyTermsUpdate = Field(
#         default=PolicyTermsUpdate(),
#         alias="terms",
#         description="""
# Policy terms and conditions.
# """
#     )
# #     geofence: PolicyGeofenceUpdate = Field(
# #         default=PolicyGeofenceUpdate(),
# #         alias="geofence",
# #         description="""
# # Policy geofence.
# # """
# #     )


class PolicyConfig(PolicyConfigStandard):
    generation: PolicyGeneration = Field(
        default=PolicyGeneration(),
        alias="generation",
        description="""
Policy generation settings.
"""
    )
    terms: PolicyTerms = Field(
        default=PolicyTerms(),
        alias="terms",
        description="""
Policy terms and conditions.
"""
    )
#     geofence: PolicyGeofenceRead = Field(
#         default=PolicyGeofenceRead(),
#         alias="geofence",
#         description="""
# Policy geofence.
# """
#     )

    class Config:
        allow_population_by_field_name = True


# class PolicyConfigCreate(PolicyConfigStandardCreate):
#     generation: PolicyGenerationCreate = Field(
#         default=PolicyGenerationCreate(),
#         alias="generation",
#         description="""
# Policy generation settings.
# """
#     )
#     terms: PolicyTermsCreate = Field(
#         default=PolicyTermsCreate(),
#         alias="terms",
#         description="""
# Policy terms and conditions.
# """
#     )
# #     geofence: PolicyGeofenceCreate = Field(
# #         default=PolicyGeofenceCreate(),
# #         alias="geofence",
# #         description="""
# # Policy geofence.
# # """
# #     )

#     def apply_defaults(self, defaults: PolicyConfigRead):
#         if 'generation' not in self.generation.__fields_set__:
#             self.generation = defaults.generation
#         if 'terms' not in self.terms.__fields_set__:
#             self.terms = defaults.terms
#         # if 'geofence' not in self.geofence.__fields_set__:
#         #     self.geofence = defaults.geofence
