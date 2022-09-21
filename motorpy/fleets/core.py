import motorpy.models as models
from motorpy.api import APIHandler
from typing import Generator


class Fleets:

    def __init__(self, api: APIHandler) -> None:
        self.api = api

    async def get_fleet(self,
                  fleet_id: str,
                  **query) -> models.Fleet:
        """Get a fleet record.

        Args:
            fleet_id (str): the UUID of the fleet.
            **query (dict): additional query parameters.

        Returns:
            models.Fleet: the Fleet model.
        """
        params = {
            **query
        }

        raw = await self.api.request(
            "GET", f"fleets/{fleet_id}", params=params
        )

        model: models.Fleet = models.Fleet(**raw)

        model.api = self.api

        return model

    async def list_fleets(self,
                    max_records: int = None) -> Generator[models.Fleet, None, None]:
        count = 0
        async for fleet in self.api.batch_fetch("fleets"):
            if max_records is not None:
                if count >= max_records:
                    break
            model: models.Fleet = models.Fleet(**fleet)
            model.api = self.api
            yield model
            count += 1
    
    async def create_fleet(self, fleet: models.Fleet) -> models.Fleet:
        """Create a new fleet.

        Args:
            fleet (models.Fleet): the fleet model.

        Returns:
            models.Fleet: the created fleet model.
        """
        raw = await self.api.request("POST", "fleets", json=fleet.dict(exclude_unset=True))

        model: models.Fleet = models.Fleet(**raw)

        model.api = self.api

        return model
