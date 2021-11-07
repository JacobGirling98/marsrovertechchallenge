from copy import deepcopy

from src.dataclasses.coordinates import Coordinates
from src.dataclasses.processed_input import ProcessedInput
from src.dataclasses.rover_setup import RoverSetup
from src.reader import Reader
from src.rover import Rover


class Controller:
    grid: list[list[int or Rover]] = None
    dims: Coordinates = None
    rovers: dict[int, Rover] = {}
    commands: list[list[str]] = []

    def __init__(self, reader: Reader):
        self.reader = reader

    def control_rover(self, _id: int, instructions: list[str]) -> Rover:
        for command in instructions:
            if command == "L" or command == "R":
                self.rovers[_id].change_direction(command)
            elif command == "M":
                self.rovers[_id].move()
                self.update_grid(_id)
        return self.rovers[_id]

    def process_rovers(self) -> None:
        for i in range(len(self.rovers)):
            self.control_rover(i, self.commands[i])

    def format_output(self) -> list[str]:
        return [f"{r.position().x} {r.position().y} {r.bearing()}" for r in self.rovers.values()]

    def instantiate_grid(self, dimensions: Coordinates) -> None:
        x = [0 for _ in range(dimensions.x + 1)]
        self.grid = [deepcopy(x) for _ in range(dimensions.y + 1)]
        self.dims = Coordinates(dimensions.x + 1, dimensions.y + 1)

    def instantiate_rovers(self, rover_setup: list[RoverSetup]) -> None:
        for i, details in enumerate(rover_setup):
            self.rovers[i] = Rover(details, i)

    def add_rovers_to_grid(self, rovers: dict[int, Rover]) -> None:
        for r in rovers.values():
            self.grid[self.transform_coords(r.position().y)][r.position().x] = r

    def transform_coords(self, y: int) -> int:
        return self.dims.y - 1 - y

    def find_rover(self, _id: int) -> Coordinates:
        rover = self.rovers[_id]
        x, y = rover.position().x, rover.position().y
        if y + 1 < self.dims.y and isinstance(self.grid[self.transform_coords(y + 1)][x], Rover) and \
                self.grid[self.transform_coords(y + 1)][x]._id == _id:
            return Coordinates(x, y + 1)
        elif y - 1 >= 0 and isinstance(self.grid[self.transform_coords(y - 1)][x], Rover) and \
                self.grid[self.transform_coords(y - 1)][x]._id == _id:
            return Coordinates(x, y - 1)
        elif x + 1 < self.dims.x and isinstance(self.grid[self.transform_coords(y)][x + 1], Rover) and \
                self.grid[self.transform_coords(y)][x + 1]._id == _id:
            return Coordinates(x + 1, y)
        elif x - 1 >= 0 and isinstance(self.grid[self.transform_coords(y)][x - 1], Rover) and \
                self.grid[self.transform_coords(y)][x - 1]._id == _id:
            return Coordinates(x - 1, y)

    def update_grid(self, _id: int) -> None:
        rover = self.rovers[_id]
        old_pos: Coordinates = self.find_rover(_id)
        new_pos: Coordinates = rover.position()

        self.grid[self.transform_coords(old_pos.y)][old_pos.x] = 0
        self.grid[self.transform_coords(new_pos.y)][new_pos.x] = rover

    def setup(self) -> None:
        processed_details: ProcessedInput = self.reader.process_input()
        self.instantiate_grid(processed_details.grid_size)
        a = [x.rover_setup for x in processed_details.rover_details]
        self.instantiate_rovers([x.rover_setup for x in processed_details.rover_details])
        self.add_rovers_to_grid(self.rovers)
        self.commands = [x.commands for x in processed_details.rover_details]
