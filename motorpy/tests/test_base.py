from ..base import Motor
from ..auth import Auth

class TestMotor:

    def test_motor_init(self):
        """
        Test Motor initialization.
        """
        org_id = "org_id"
        auth = Auth(
            api_key="api_key",
            api_secret="api_secret",
        )
        region = 'eu-1'

        motor = Motor(org_id, auth, region)

        assert motor.org_id == org_id
        assert motor.auth == auth
        assert motor.region == region

        # assert inherited methods are present
        # for sanity check
        assert hasattr(motor, 'get_vehicle')
        assert hasattr(motor, 'list_vehicles')
        assert hasattr(motor, 'get_driver')
