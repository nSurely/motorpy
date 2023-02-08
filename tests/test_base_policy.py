"Test the motorpy.Policy model"
import motorpy
import asyncio
import pytest
import pprint
from .helpers.compare import compare_dict_keys, flatten


class TestPolicy:
    "Testing methods on the Policy model"

    pp = pprint.PrettyPrinter(indent=4)

    # policies
    async def test_policy_list(self, driver: motorpy.Driver):
        policies = [p async for p in driver.list_policies()]
        if not policies:
            return
        assert all([isinstance(p, motorpy.Policy) for p in policies])
        assert isinstance(policies, list)

    async def test_policy_create(self, driver: motorpy.Driver):
        new_policy_id = None
        try:
            # create a policy
            new_policy = motorpy.Policy(
                sum_insured=1001
            )
            new_policy = await driver.create_policy(new_policy)
            assert isinstance(new_policy, motorpy.Policy)
            assert new_policy.id is not None
            assert new_policy.sum_insured == 1001
            new_policy_id = new_policy.id
        finally:
            # clean up
            if new_policy_id:
                policy = await driver.get_policy(new_policy_id)
                await policy.delete()
    