from dataclasses import dataclass

from src.dataclasses.rover_instructions import RoverInstructions


@dataclass
class ProcessedInput:
    grid_size: list[int]
    rover_details: list[RoverInstructions]
