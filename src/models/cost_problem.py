from enum import Enum

from pydantic import BaseModel, PositiveInt

from config import settings
from src.models import Client, Facility


class CostType(Enum):
    """Available cost types for the cost problem"""

    PROXIMITY = "proximity"
    TRAVEL_DISTANCE = "distances"
    TRAVEL_DURATION = "durations"


class CostProblem(BaseModel):
    """Model representing the cost problem"""

    clients: list[Client]
    fixed_facilities: list[Facility]
    cost_type: CostType
    osrm_server_address: str = settings.OSRM_SERVER_ADDRESS
    osrm_batch_size: PositiveInt = settings.OSRM_BATCH_SIZE
