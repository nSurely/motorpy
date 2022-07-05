from ..org_config import PolicyOrgConfig
from datetime import datetime
from uuid import uuid4

FULL = {
    "id": "DRV-123",
    "createdAt": "2020-01-01T00:00:00.000Z",
    "isActivePolicy": True,
    "sumInsured": 100.00,
    "canRenew": True,
    "maxPassengers": 1,
    "cover": [
        "comprehensive"
    ],
    "approval": {
        "approvedAt": datetime.now(),
        "autoApproved": True,
        "approvedBy": str(uuid4())
    },
    "cancellation": {
        "cancelledAt": datetime.now(),
        "message": "test"
    },
    "config": {
        "display": "test",
        "description": "test",
        "currency": "EUR",
        "generation": {
            "maxPassengersInheritVehicle": True,
            "autoIssued": True
        },
        "terms": {
            "url": "https://www.google.com",
            "html": "<h1>test</h1>",
                    "attachments": [
                        "https://www.google.com"
                    ],
            "requiresDriverEsignature": True
        },
        "geofence": {
            "enabled": True,
            "polygons": [
                {
                    "type": "Polygon",
                    "coordinates": [
                            [
                                -122.4,
                                37.8
                            ],
                        [
                                -122.4,
                                37.9
                            ],
                        [
                                -122.3,
                                37.9
                            ],
                        [
                                -122.4,
                                37.8
                            ]
                    ]
                }
            ]
        }
    },
    "contribution": {
        "pc": 100.00,
        "details": {
            "test": "test"
        }
    },
    "driver": {
        "esignature": "path",
        "esignatureFingerprint": {
            "test": "test"
        },
        "agreedAt": datetime.now()
    },
    "duration": {
        "start": datetime.now(),
        "end": datetime.now(),
        "gracePeriodMins": 1
    },
    "excess": {
        "voluntary": 100,
        "compulsory": 100
    },
    "extras": {
        "repairs": {
            "enforceApprovedSuppliers": True,
            "courtesyVehicle": True
        },
        "alarm": {
            "enforce": True
        },
        "breakdown": {
            "cover": True,
            "coverLimit": 1,
            "cost": 100
        },
        "rescue": {
            "cover": True,
            "coverLimit": 1,
            "cost": 100
        },
        "theft": {
            "cover": True,
            "coverLimit": 1,
            "cost": 100
        },
        "keyReplacement": {
            "cover": True,
            "coverLimit": 1,
            "cost": 100
        },
        "windscreen": {
            "cover": True,
            "cost": 100
        }
    },
    "fees": {
        "cancellation": 0,
        "renewal": 0,
        "newBusiness": 0
    },
    "final": {
        "rates": {
            "value": 1,
            "max": 3,
            "min": 0,
            "appliedRiskMultiplier": 1.5
        },
        "premium": {
            "value": 100,
            "appliedRiskMultiplier": 1.5
        }
    },
    "issuer": {
        "id": str(uuid4()),
        "policyAgreedAt": datetime.now()
    },
    "noClaims": {
        "forgiveness": False,
        "discountPc": 10.0
    },
    "premium": {
        "enabled": True,
        "value": 100,
        "payableImmediate": True,
        "frequency": "bmf",
        "useFrequency": False,
        "nextPaymentDate": None,
        "variable": False
    },
    "rates": {
        "enabled": True,
        # "active": True,
        "value": 0.5,
        "max": 1.0,
        "min": 0.0,
        "chargeableDistanceKm": 100,
        "frequency": "bmf",
        "variable": False
    },
    "rewards": {
        "enabled": True,
        "maxMonthly": 100,
        "rates": {
            "enabled": True,
            "maxDiscountPc": 20.0
        },
        "premium": {
            "enabled": True,
            "maxDiscountPc": 20.0
        }
    },
    "telematics": {
        "process": "indefinite",
        "days": None,
        "minKm": None
    }
}

GRACE_MINS = 60*24*7

# creating an empty policy config to get attrs
ORG_ATTRS = PolicyOrgConfig(policy_group="drv")
# create with shared fields (not all fields are used in config)
ORG_CONF = PolicyOrgConfig(
    policy_group="drv",
    policy_config="custom",
    cover_type={"comprehensive"},
    assign_policy_on_create=True,
    requires_approval=False,
    valid_mins=GRACE_MINS,
    **{k: v for k, v in FULL.items() if k in ORG_ATTRS.__fields__}
)
