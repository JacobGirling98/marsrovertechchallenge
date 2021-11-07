from dataclasses import dataclass

from src.dataclasses.coordinates import Coordinates
from src.dataclasses.rover_details import RoverDetails


@dataclass
class ProcessedInput:
    grid_size: Coordinates
    rover_details: list[RoverDetails]
