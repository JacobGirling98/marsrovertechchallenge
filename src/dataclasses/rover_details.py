from dataclasses import dataclass

from src.dataclasses.rover_setup import RoverSetup


@dataclass
class RoverDetails:
    rover_setup: RoverSetup
    commands: list[str]
