from dataclasses import dataclass

from src.dataclasses.coordinates import Coordinates


@dataclass
class RoverSetup:
    position: Coordinates
    direction: str
