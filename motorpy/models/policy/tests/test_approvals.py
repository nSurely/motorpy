import pprint
import pytest
from datetime import datetime
from ..nested import PolicyNestedCreate
from .const import ORG_CONF

pp = pprint.PrettyPrinter(indent=4)


class TestPolicyDefaultsApprovals:
    def test_sparse_model_no_approval(self):
        p = PolicyNestedCreate()

        p.apply_approvals(ORG_CONF)

        assert p.approval.approval_auto_approved is True
        assert p.approval.approval_approved_at.replace(
            microsecond=0) == datetime.utcnow().replace(microsecond=0)
        assert p.approval.approval_by is None

        exp = p.export('DRV', exclude_unset=True)

        assert 'approval_auto_approved' in exp
        assert 'approval_approved_at' in exp
        assert 'approval_by' in exp

    def test_sparse_model_approval(self):
        p = PolicyNestedCreate()

        tmp = ORG_CONF.copy()
        tmp.requires_approval = True
        p.apply_approvals(tmp)

        assert p.approval.approval_auto_approved is False
        assert p.approval.approval_approved_at is None

    def test_sparse_model_full(self):
        p = PolicyNestedCreate()

        p.apply_org_defaults(ORG_CONF)

        # pp.pprint(p.dict(exclude_unset=True))

        assert p.approval.approval_auto_approved is True
        # remove milliseconds as it may not be equal
        assert p.approval.approval_approved_at.replace(
            microsecond=0) == datetime.utcnow().replace(microsecond=0)
        assert p.approval.approval_by is None

        exp = p.export('DRV', exclude_unset=True)

        assert 'approval_auto_approved' in exp
        assert 'approval_approved_at' in exp
        assert 'approval_by' in exp
