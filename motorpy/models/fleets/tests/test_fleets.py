from motorpy.models.fleets import Fleet
import uuid


class TestFleets:
    fid = str(uuid.uuid4())
    test_data = {
        "id": fid,
        "external_id": "123",
        "display": "display",
        "description": "desc",
        "tags": "tag1,tag2,tag3",
        "is_active": True,
        "requires_driver_assignment": True,
        "base_premium_billing_proc": "123",
        "rates_billing_proc": "123",
        "parent_id": "123",
        "created_at": "123",
        "translations": {
                "display": {
                    "en": "english_display",
                    "fr": "french_display",
                },
            "description": {
                    "en": "english_desc",
                    "fr": "french_desc",
                    }
        },
        "risk": {
            "lookback": {
                "rates": {
                    "apply": True,
                    "inheritance": True,
                },
                "value": 0.0,
                "weighting": 0.0,
                "premium": {
                    "apply": True,
                    "inheritance": True,
                },
            },
            "dynamic": {
                "apply": True,
                "process": "std",
                "weighting": 0.0,
            },
            "ihr": {
                "rates": {
                    "apply": True,
                    "inheritance": True,
                },
                "value": 0.0,
                "weighting": 0.0,
                "premium": {
                    "apply": True,
                    "inheritance": True,
                },
            },
        },
    }

    def test_model_init(self):
        fleet = Fleet(**self.test_data)
        assert str(fleet.id) == str(self.fid)

    def test_translations(self):
        fleet = Fleet(**self.test_data)
        assert fleet.translations["display"]["en"] == "english_display"
        assert fleet.translations["display"]["fr"] == "french_display"
        assert fleet.translations["description"]["en"] == "english_desc"
        assert fleet.translations["description"]["fr"] == "french_desc"

        # check its retrieving the correct translations
        disp = fleet.get_display("en")
        assert disp == "english_display"
        disp = fleet.get_display("fr")
        assert disp == "french_display"
        desc = fleet.get_description("en")
        assert desc == "english_desc"
        desc = fleet.get_description("fr")
        assert desc == "french_desc"

        # check for fallback
        disp = fleet.get_display("es")
        assert disp == "display"
        desc = fleet.get_description("es")
        assert desc == "desc"

    def test_parent(self):
        fleet = Fleet(**self.test_data)
        assert fleet.parent_id == "123"
        assert fleet.has_parent() == True

    def test_update_field(self):
        fleet = Fleet(**self.test_data)
        # fleet.update("display", "new_display")
        fleet.display = "new_display"
        assert fleet.display == "new_display"

        assert 'display' in fleet.__fields_set__
