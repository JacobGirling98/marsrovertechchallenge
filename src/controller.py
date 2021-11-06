from src.dataclasses.processed_input import ProcessedInput
from src.reader import Reader
from src.rover import Rover


class Controller:

    def __init__(self, file_loc: str):
        self.reader = Reader(file_loc)

    def control_rover(self, rover: Rover, instructions: list[str]) -> Rover:
        for command in instructions:
            if command == "L" or command == "R":
                rover.change_direction(command)
            elif command == "M":
                rover.move()
        return rover

    def process_rovers(self) -> list[Rover]:
        processed_details: ProcessedInput = self.reader.process_input()
        rovers: list[Rover] = []
        for rover_details in processed_details.rover_details:
            rover = Rover(rover_details.position, processed_details.grid_size)
            rover = self.control_rover(rover, rover_details.commands)
            rovers.append(rover)
        return rovers

    def format_output(self, rovers: list[Rover]) -> list[str]:
        return [f"{r.position()[0]} {r.position()[1]} {r.bearing()}" for r in rovers]
