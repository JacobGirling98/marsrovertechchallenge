from src.dataclasses.coordinates import Coordinates
from src.dataclasses.processed_input import ProcessedInput
from src.dataclasses.rover_details import RoverDetails
from src.dataclasses.rover_setup import RoverSetup


class Reader:

    def __init__(self, input_file_path):
        self.input_file_path = input_file_path

    def _read_input(self) -> list[str]:
        with open(self.input_file_path, "r") as file:
            data: list = file.read().splitlines()
        return data

    def _top_grid(self, received_data: list) -> Coordinates:
        grid_dims = received_data[0].split()
        return Coordinates(int(grid_dims[0]), int(grid_dims[1]))

    def _get_position(self, input_position: str) -> Coordinates:
        position: list = input_position.split()
        return Coordinates(int(position[0]), int(position[1]))

    def _get_direction(self, input_position: str) -> str:
        return input_position.split()[2]

    def _get_rover_details(self, received_data: list) -> list[RoverDetails]:
        instructions: list[RoverDetails] = []
        counter = 1
        while counter < len(received_data):
            position: Coordinates = self._get_position(received_data[counter])
            direction: str = self._get_direction(received_data[counter])
            rover_setup = RoverSetup(position, direction)
            counter += 1
            movement: list[str] = list(received_data[counter])
            counter += 1
            instructions.append(RoverDetails(rover_setup, movement))
        return instructions

    def process_input(self) -> ProcessedInput:
        data: list[str] = self._read_input()
        return ProcessedInput(self._top_grid(data), self._get_rover_details(data))
