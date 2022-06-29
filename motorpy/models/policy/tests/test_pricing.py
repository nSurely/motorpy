import pprint
import pytest
from ..nested import PolicyNestedCreate
from .const import FULL, ORG_CONF

pp = pprint.PrettyPrinter(indent=4)


class TestPolicyPricing:
    def test_sparse_model_rates(self):
        p = PolicyNestedCreate()

        exp = p.export('DRV', exclude_unset=True)

        # check they are not set
        assert 'final_rates_value' not in exp
        assert 'final_rates_max' not in exp
        assert 'final_rates_min' not in exp
        assert 'final_rates_applied_risk_multiplier' not in exp
        assert 'final_base_premium_value' not in exp
        assert 'final_base_premium_applied_risk_multiplier' not in exp

        # set rates
        p.apply_rates(ORG_CONF)
        pp.pprint(FULL['rates'])

        # they should match the org config rates (not final values in that dict!!)
        assert p.final.final_rates.final_rates_value == FULL['rates']['value']
        assert p.final.final_rates.final_rates_min == FULL['rates']['min']
        assert p.final.final_rates.final_rates_max == FULL['rates']['max']

    def test_sparse_model_premium(self):
        # same process as above ^^
        p = PolicyNestedCreate()

        exp = p.export('DRV', exclude_unset=True)

        assert 'final_base_premium_value' not in exp
        assert 'final_base_premium_applied_risk_multiplier' not in exp

        p.apply_premium(ORG_CONF)

        pp.pprint(FULL['premium'])

        assert p.final.final_base_premium.final_base_premium_value == FULL['premium']['value']

    def test_sparse_model_risk_multiplier(self):
        p = PolicyNestedCreate()
        p.apply_premium(ORG_CONF)
        p.apply_rates(ORG_CONF)

        rm = 1.1

        p.apply_risk_multiplier(rm)

        assert p.final.final_rates.final_rates_value == FULL['rates']['value'] * rm
        assert p.final.final_base_premium.final_base_premium_value == FULL[
            'premium']['value'] * rm

        # rm should not effect the min/max
        assert p.final.final_rates.final_rates_min == FULL['rates']['min']
        assert p.final.final_rates.final_rates_max == FULL['rates']['max']

        assert p.final.final_rates.final_rates_applied_risk_multiplier == rm
        assert p.final.final_base_premium.final_base_premium_applied_risk_multiplier == rm

        # check that value error is raised as it will set value to too high for rates
        rm = 100.0
        with pytest.raises(ValueError):
            p.apply_risk_multiplier(rm)

    def test_sparse_model_pricing_full(self):
        p = PolicyNestedCreate()
        p.apply_org_defaults(ORG_CONF)

        rm = 1.1
        p.apply_risk_multiplier(rm)

        assert p.final.final_rates.final_rates_min == FULL['rates']['min']
        assert p.final.final_rates.final_rates_max == FULL['rates']['max']

        # check export contains final fields
        exp = p.export('DRV', exclude_unset=True)
        assert 'final_rates_value' in exp
        assert 'final_rates_min' in exp
        assert 'final_rates_max' in exp
        assert 'final_rates_applied_risk_multiplier' in exp
        assert 'final_base_premium_value' in exp
        assert 'final_base_premium_applied_risk_multiplier' in exp
