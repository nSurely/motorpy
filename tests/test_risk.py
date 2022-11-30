import motorpy


def test_common_risk_init():
    r = motorpy.models.risk.CommonRisk(**{
        "risk": {
            "dynamic": {
                "apply": True,
                "process": "para",
                "weighting": 1.1
            },
            "lookback": {
                "rates": {
                    "apply": True,
                    "inheritance": False
                },
                "value": 1.0,
                "weighting": 0.0,
                "premium": {
                    "apply": True,
                    "inheritance": False
                }
            },
            "ihr": {
                "rates": {
                    "apply": True,
                    "inheritance": False
                },
                "value": 2.0,
                "weighting": 0.0,
                "premium": {
                    "apply": True,
                    "inheritance": False
                }
            }
        }
    })

    assert r.risk.dynamic.apply is True
    assert r.risk.dynamic.process == "para"
    assert r.risk.dynamic.weighting == 1.1
    assert r.risk.lookback.rates.apply is True
    assert r.risk.lookback.rates.inheritance is False
    assert r.risk.lookback.value == 1.0
    assert r.risk.lookback.weighting == 0.0
    assert r.risk.lookback.premium.apply is True
    assert r.risk.lookback.premium.inheritance is False
    assert r.risk.ihr.rates.apply is True
    assert r.risk.ihr.rates.inheritance is False
    assert r.risk.ihr.value == 2.0
    assert r.risk.ihr.weighting == 0.0
    assert r.risk.ihr.premium.apply is True
    assert r.risk.ihr.premium.inheritance is False
