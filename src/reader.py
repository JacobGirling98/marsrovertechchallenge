from src.dataclasses.processed_input import ProcessedInput
from src.dataclasses.rover_instructions import RoverInstructions


class Reader:

    def __init__(self, input_file_path):
        self.input_file_path = input_file_path

    def _read_input(self) -> list:
        with open(self.input_file_path, "r") as file:
            data: list = file.read().splitlines()
        return data

    def _top_grid(self, received_data: list) -> list:
        return [int(x) for x in received_data[0].split()]

    def _get_position(self, input_position: str) -> list:
        position: list = input_position.split()
        position[0], position[1] = int(position[0]), int(position[1])
        return position

    def _get_instructions(self, received_data: list) -> list:
        instructions: list[RoverInstructions] = []
        counter = 1
        while counter < len(received_data):
            position: list = self._get_position(received_data[counter])
            counter += 1
            movement: list = list(received_data[counter])
            counter += 1
            instructions.append(RoverInstructions(position, movement))
        return instructions

    def process_input(self):
        data: list = self._read_input()
        return ProcessedInput(self._top_grid(data), self._get_instructions(data))
