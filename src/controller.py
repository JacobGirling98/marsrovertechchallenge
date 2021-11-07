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
        self.reader: Reader = reader

    def setup(self) -> None:
        processed_details: ProcessedInput = self.reader.process_input()
        self._instantiate_grid(processed_details.grid_size)
        self._instantiate_rovers([x.rover_setup for x in processed_details.rover_details])
        self._add_rovers_to_grid(self.rovers)
        self.commands: list[list[str]] = [x.commands for x in processed_details.rover_details]

    def _instantiate_grid(self, dimensions: Coordinates) -> None:
        x: list[int] = [0 for _ in range(dimensions.x + 1)]
        self.grid = [deepcopy(x) for _ in range(dimensions.y + 1)]
        self.dims = Coordinates(dimensions.x + 1, dimensions.y + 1)

    def _instantiate_rovers(self, rover_setup: list[RoverSetup]) -> None:
        for i, details in enumerate(rover_setup):
            self.rovers[i] = Rover(details, i)

    def _add_rovers_to_grid(self, rovers: dict[int, Rover]) -> None:
        for r in rovers.values():
            self.grid[self._transform_coords(r.position().y)][r.position().x] = r

    def process_rovers(self) -> None:
        for i in range(len(self.rovers)):
            self._control_rover(i, self.commands[i])

    def _control_rover(self, _id: int, instructions: list[str]) -> Rover:
        for command in instructions:
            if command == "L" or command == "R":
                self.rovers[_id].change_direction(command)
            elif command == "M":
                self.rovers[_id].move()
                self._update_grid(_id)
        return self.rovers[_id]

    def _update_grid(self, _id: int) -> None:
        rover: Rover = self.rovers[_id]
        old_pos: Coordinates = self._find_rover(_id)
        new_pos: Coordinates = rover.position()

        self.grid[self._transform_coords(old_pos.y)][old_pos.x] = 0
        self.grid[self._transform_coords(new_pos.y)][new_pos.x] = rover

    def _find_rover(self, _id: int) -> Coordinates:
        rover: Rover = self.rovers[_id]
        x: int
        y: int
        x, y = rover.position().x, rover.position().y
        if y + 1 < self.dims.y and isinstance(self.grid[self._transform_coords(y + 1)][x], Rover) and \
                self.grid[self._transform_coords(y + 1)][x].rover_id == _id:
            return Coordinates(x, y + 1)
        elif y - 1 >= 0 and isinstance(self.grid[self._transform_coords(y - 1)][x], Rover) and \
                self.grid[self._transform_coords(y - 1)][x].rover_id == _id:
            return Coordinates(x, y - 1)
        elif x + 1 < self.dims.x and isinstance(self.grid[self._transform_coords(y)][x + 1], Rover) and \
                self.grid[self._transform_coords(y)][x + 1].rover_id == _id:
            return Coordinates(x + 1, y)
        elif x - 1 >= 0 and isinstance(self.grid[self._transform_coords(y)][x - 1], Rover) and \
                self.grid[self._transform_coords(y)][x - 1].rover_id == _id:
            return Coordinates(x - 1, y)

    def _transform_coords(self, y: int) -> int:
        return self.dims.y - 1 - y

    def format_output(self) -> list[str]:
        return [f"{r.position().x} {r.position().y} {r.bearing()}" for r in self.rovers.values()]
