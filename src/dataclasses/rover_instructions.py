from dataclasses import dataclass


@dataclass
class RoverInstructions:
    position: list[int and str]
    commands: list[str]
