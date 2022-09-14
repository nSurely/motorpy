import time
from motorpy.api import APIHandler
from typing import List


class TripManager:
    """
    TripManager handles the batching and sending of telematics data. One trip manager should be used per trip.

    Args:
        api (APIHandler): API handler.
        source_id (str): source ID.
        org_id (str, optional): organization ID. Defaults to None.
        batch_window (float, optional): batch window in seconds. If 0.0, it will send every time a new value is added. Defaults to 20.0.
    """

    def __init__(self,
                 api: APIHandler,
                 source_id: str,
                 org_id: str = None,
                 batch_window: float = 20.0) -> None:

        self.batch_window = batch_window
        if self.batch_window < 0:
            raise ValueError("batch_window must be greater than 0")

        if self.batch_window > 60:
            raise ValueError("batch_window must be less than 60")

        self.api = api
        self.source_id = source_id
        self.org_id = org_id

        self.last_batch_time = time.time()

        self.gps: List[dict] = []
        self.accelerometer: List[dict] = []
        self.gyroscope: List[dict] = []
        self.alerts: List[dict] = []

    def clear(self) -> None:
        "Clear the trip data."
        self.gps = []
        self.accelerometer = []
        self.gyroscope = []
        self.alerts = []

    async def send_check(self) -> None:
        "Check if we need to send a batch. If so, send it and clear."
        if (not self.gps and
            not self.accelerometer and
            not self.gyroscope and
                not self.alerts):
            return

        if self.batch_window != 0.0:
            if time.time() - self.last_batch_time < self.batch_window:
                return

        body = {
            "sourceId": self.source_id,
            "orgId": self.org_id,
            "gps": self.gps,
            "acc": self.accelerometer,
            "gyro": self.gyroscope,
            "alerts": self.alerts
        }

        await self.api.telematics_request("POST", "/track", data=body)
        self.clear()

    async def add_gps(self,
                      lat: float,
                      lng: float,
                      gps_accuracy: float = None,
                      altitude: float = None,
                      acceleration: float = None,
                      speed: float = None,
                      bearing: float = None,
                      bearing_accuracy: float = None,
                      vertical_acceleration: float = None,
                      timestamp: int = None) -> None:
        """Add a GPS point to the trip.

        Args:
            lat (float): latitude.
            lng (float): longitude.
            gps_accuracy (float, optional): GPS accuracy in metres. Defaults to None.
            altitude (float, optional): Altitude in metres. Defaults to None.
            acceleration (float, optional): Acceleration in m/s2. Defaults to None.
            speed (float, optional): speed in m/s. Defaults to None.
            bearing (float, optional): bearing/heading in degrees from north. Defaults to None.
            bearing_accuracy (float, optional): bearing accuracy in degrees. Defaults to None.
            vertical_acceleration (float, optional): vertical acceleration in m/s2. Defaults to None.
            timestamp (int, optional): timestamp in milliseconds override, will use time.time() if not provided. Defaults to None.

        Raises:
            ValueError: invalid latitude or longitude.
        """
        if lat is None or lng is None:
            raise ValueError("lat and lng must be provided")

        # check if lat is valid
        if lat < -90 or lat > 90:
            raise ValueError("lat must be between -90 and 90")

        # check if lng is valid
        if lng < -180 or lng > 180:
            raise ValueError("lng must be between -180 and 180")

        if not timestamp:
            timestamp = int(time.time() * 1000)

        self.gps.append({
            "lat": lat,
            "lng": lng,
            "a": gps_accuracy,
            "alt": altitude,
            "acc": acceleration,
            "s": speed,
            "b": bearing,
            "bAcc": bearing_accuracy,
            "va": vertical_acceleration,
            "ts": timestamp
        })
        await self.send_check()

    async def add_accelerometer(self,
                                x: float,
                                y: float,
                                z: float,
                                timestamp: int = None) -> None:
        """Add an accelerometer point to the trip.

        Args:
            x (float): x acceleration in m/s2.
            y (float): y acceleration in m/s2.
            z (float): z acceleration in m/s2.
            timestamp (int, optional): timestamp in milliseconds override, will use time.time() if not provided. Defaults to None.

        Raises:
            ValueError: missing x, y or z.
        """
        if x is None or y is None or z is None:
            raise ValueError("x, y and z must be provided")

        if not timestamp:
            timestamp = int(time.time() * 1000)

        self.accelerometer.append({
            "x": x,
            "y": y,
            "z": z,
            "ts": timestamp
        })
        await self.send_check()

    async def add_gyroscope(self,
                            x: float,
                            y: float,
                            z: float,
                            timestamp: int = None) -> None:
        """Add a gyroscope point to the trip.

        Args:
            x (float): x gyroscope in rad/s.
            y (float): y gyroscope in rad/s.
            z (float): z gyroscope in rad/s.
            timestamp (int, optional): timestamp in milliseconds override, will use time.time() if not provided. Defaults to None.

        Raises:
            ValueError: missing x, y or z.
        """
        if x is None or y is None or z is None:
            raise ValueError("x, y and z must be provided")

        if not timestamp:
            timestamp = int(time.time() * 1000)

        self.gyroscope.append({
            "x": x,
            "y": y,
            "z": z,
            "ts": timestamp
        })
        await self.send_check()

    async def add_alert(self,
                        alert_code: str,
                        measurement_1: float = None,
                        measurement_2: float = None,
                        measurement_3: float = None,
                        on_device: bool = False,
                        shown: bool = False,
                        timestamp: int = None) -> None:
        """Add an alert to the trip.

        Args:
            alert_code (str): alert code.
            measurement_1 (float, optional): measurement 1. Defaults to None.
            measurement_2 (float, optional): measurement 2. Defaults to None.
            measurement_3 (float, optional): measurement 3. Defaults to None.
            on_device (bool, optional): alert is on device. Defaults to False.
            shown (bool, optional): alert is shown. Defaults to False.
            timestamp (int, optional): timestamp in milliseconds override, will use time.time() if not provided. Defaults to None.

            Raises:
                ValueError: missing alert code.
        """
        if alert_code is None:
            raise ValueError("alert_code must be provided")

        if not timestamp:
            timestamp = int(time.time() * 1000)

        self.alerts.append({
            "code": alert_code,
            "m1": measurement_1,
            "m2": measurement_2,
            "m3": measurement_3,
            "onDevice": on_device,
            "shown": shown,
            "ts": timestamp
        })
        await self.send_check()
