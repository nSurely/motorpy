"""
Convenience functions for creating policies.
"""
from .nested import Policy
from .enums import PolicyGroup
from motorpy.api import APIHandler


def create_policy(api: APIHandler,
                  record_id: str,
                  group: PolicyGroup,
                  policy: Policy = None,
                  driver_id: str = None,
                  vehicle_id: str = None) -> Policy:
    """
    Create a policy.

    Args:
        api (APIHandler): api handler
        record_id (str): record id, to place policy on
        group (PolicyGroup): policy group
        policy (Policy, optional): policy to create. This can be left None and a new policy will be created using the org defaults. Defaults to None.
        driver_id (str, optional): driver id, required for some fleet policies. Defaults to None.
        vehicle_id (str, optional): vehicle id, required for some fleet policies. Defaults to None.

    For policy groups:

    - d (driver): record ID is the driver ID
    - rv (vehicle): record ID is the vehicle ID
    - drv (driver): record ID is the driver vehicle ID
    - fd (fleet driver): record ID is the fleet ID, and driver_id is the driver ID
    - frv (fleet vehicle): record ID is the fleet ID, and vehicle_id is the vehicle ID
    - fdrv (fleet driver vehicle): record ID is the fleet ID, and driver_id and vehicle_id are the driver and vehicle IDs

    Returns:
        Policy: created policy
    """
    if not policy:
        policy = Policy(api=api)

    params = {}

    policy.policy_group = group

    if group == PolicyGroup.D:
        # * D
        if driver_id is not None:
            # just in case the driver id is not the same as the record id
            record_id = driver_id if record_id != driver_id else record_id
    elif group == PolicyGroup.DRV:
        # * DRV
        # record id is all that is needed
        pass
    elif group == PolicyGroup.RV:
        # * RV
        pass
    elif group == PolicyGroup.FD:
        # * FD
        if driver_id is None:
            raise ValueError("driver_id must be supplied for FD policies")
        params["driverId"] = driver_id

        if record_id == driver_id:
            raise ValueError(
                "record_id (fleet id) must not be the same as driver_id for FD policies")
    elif group == PolicyGroup.FDRV:
        # * FDRV
        if driver_id is None:
            raise ValueError("driver_id must be supplied for FDRV policies")
        if vehicle_id is None:
            raise ValueError("vehicle_id must be supplied for FDRV policies")
        params["driverId"] = driver_id
        params["vehicleId"] = vehicle_id

        if record_id == driver_id or record_id == vehicle_id:
            raise ValueError(
                "record_id (fleet id) must not be the same as driver_id or vehicle_id for FDRV policies")
    elif group == PolicyGroup.FRV:
        # * FRV
        if vehicle_id is None:
            raise ValueError("vehicle_id must be supplied for FRV policies")

        if record_id == vehicle_id:
            raise ValueError(
                "record_id (fleet id) must not be the same as vehicle_id for FRV policies")

        params["vehicleId"] = vehicle_id

    res = api.request("POST",
                      f"policy/{record_id}",
                      params=params,
                      data=policy.dict(
                          by_alias=True,
                          exclude_unset=True
                      ))

    return Policy(api=api, **res)
