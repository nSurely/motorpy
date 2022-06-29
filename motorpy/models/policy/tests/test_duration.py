import pprint
import pytest
from datetime import datetime, timedelta
from ..nested import PolicyNestedCreate
from .const import FULL, ORG_CONF, GRACE_MINS

pp = pprint.PrettyPrinter(indent=4)


class TestPolicyDefaultsDuration:
    def test_sparse_model(self):
        p = PolicyNestedCreate()

        exp = p.export('DRV', exclude_unset=True)

        assert 'duration_start' not in exp
        assert 'duration_end' not in exp
        assert 'duration_grace_period_mins' not in exp

        p.apply_duration(ORG_CONF)

        assert p.duration.duration_start is not None
        assert p.duration.duration_end is not None
        assert p.duration.duration_grace_period_mins is not None

        utc_now = datetime.utcnow()

        assert p.duration.duration_start.replace(
            microsecond=0) == utc_now.replace(microsecond=0)
        assert p.duration.duration_end.replace(microsecond=0) == (
            utc_now + timedelta(minutes=GRACE_MINS)).replace(microsecond=0)

        exp = p.export('DRV', exclude_unset=True)
        assert 'duration_start' in exp
        assert 'duration_end' in exp
        assert 'duration_grace_period_mins' in exp
