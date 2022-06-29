import pprint
import pytest
from ..nested import PolicyNestedCreate
from .const import FULL, ORG_CONF

pp = pprint.PrettyPrinter(indent=4)


class TestCreate:
    def test_create_basic(self):
        to_test = {
            "isActivePolicy": True,
            "sumInsured": 100.00,
            "canRenew": True,
            "cover": [
                "comprehensive"
            ],
            "maxPassengers": 1
        }
        p = PolicyNestedCreate(**to_test)

        assert p.is_active == True
        assert p.sum_insured == 100.00
        assert p.can_renew == True
        assert p.cover_type == {'comprehensive'}
        assert p.max_passengers == 1

        exp = p.get_insert("RV", True)
        print(exp)
        assert 'uid' in exp

    def test_create_nested(self):
        _ = PolicyNestedCreate(**FULL)

    def test_create_export(self):
        # the policy to apply defaults to
        p = PolicyNestedCreate(**FULL)
        exp = p.export('DRV',
            exclude_unset=True,
        )
        print(exp)
        assert isinstance(exp, dict)

    def test_create_export_defaults(self):
        # the policy to apply defaults to
        # copy the full policy and delete some fields to check if the defaults are applied
        f = FULL.copy()
        excl = ['rates', 'rewards', 'telematics', 'premium']
        for k in excl:
            del f[k]

        p = PolicyNestedCreate(**f)

        exp = p.export('DRV',
            exclude_unset=True,
            org_defaults=ORG_CONF,
            risk_multiplier=2.0
        )
        pp.pprint(exp)

        # assert len(exp) == len(p.export(exclude_unset=False))

        # check that there are keys that start with rates, rewards, telematics etc..
        # as the start of the keys start with this prefix
        for k in excl:
            assert any([k in x for x in exp.keys()])

    def test_create_sparse_model(self):
        # checks that the fields are set by config
        # does not check every field
        p = PolicyNestedCreate()
        # export the model before fields are set
        exp_sm = p.export('DRV', exclude_unset=True)

        # export and set fields
        exp = p.export('DRV',
            org_defaults=ORG_CONF,
            risk_multiplier=None
        )
        pp.pprint(exp)
        assert len(exp) > 50

        assert len(exp) > len(exp_sm)

        # no fields are set above
        assert len(exp) != 0

    # def test_create_risk_multiplier(self):
    #     p = PolicyNestedCreate(**FULL)
    #     pp.pprint(p.dict(exclude_unset=False))
    #     # check risk multiplier
    #     rm = 2.0
    #     exp = p.export(
    #         exclude_unset=True,
    #         org_defaults=ORG_CONF,
    #         risk_multiplier=rm
    #     )
    #     print(exp)
    #     # 1 * 2 = 2 (risk multiplier)
    #     assert exp['final_rates_value'] == FULL['final']['rates']['value'] * rm
    #     assert exp['final_rates_applied_risk_multiplier'] == rm
    #     assert exp['final_base_premium_value'] == FULL['final']['premium']['value'] * rm
    #     assert exp['final_base_premium_applied_risk_multiplier'] == rm

    # def test_create_risk_multiplier_org_defaults(self):
    #     f = FULL.copy()
    #     for k in ['rates', 'premium']:
    #         del f[k]
    #     p = PolicyNestedCreate(**f)
    #     # check risk multiplier
    #     rm = 2.0
    #     exp = p.export(
    #         exclude_unset=True,
    #         org_defaults=ORG_CONF,
    #         risk_multiplier=rm
    #     )
    #     pp.pprint(exp)
    #     # 1 * 2 = 2 (risk multiplier)
    #     assert exp['final_rates_value'] == FULL['rates']['value'] * rm
    #     assert exp['final_rates_applied_risk_multiplier'] == rm
    #     assert exp['final_base_premium_value'] == FULL['premium']['value'] * rm
    #     assert exp['final_base_premium_applied_risk_multiplier'] == rm

    # def test_create_risk_multiplier_max(self):
    #     p = PolicyNestedCreate(**FULL)
    #     # check risk multiplier
    #     rm = 4.0
    #     exp = p.export(
    #         exclude_unset=True,
    #         org_defaults=ORG_CONF,
    #         risk_multiplier=rm
    #     )
    #     # 1 * 4 = 4 (risk multiplier)
    #     # but max is 3
    #     assert exp['final_rates_value'] == 3.0
    #     assert exp['final_rates_applied_risk_multiplier'] == rm
