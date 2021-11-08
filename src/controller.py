from src.dataclasses.coordinates import Coordinates
from src.dataclasses.processed_input import ProcessedInput
from src.dataclasses.rover_setup import RoverSetup
from src.exceptions.position_blocked_exception import PositionBlockedException
from src.exceptions.position_out_of_bounds_exception import PositionOutOfBoundsException
from src.reader import Reader
from src.rover import Rover


class Controller:
    rovers: dict[int, Rover] = {}

    def __init__(self, reader: Reader):
        self.reader: Reader = reader
        processed_details: ProcessedInput = self.reader.process_input()
        self.dims: Coordinates = processed_details.grid_size
        self._instantiate_rovers([x.rover_setup for x in processed_details.rover_details])
        self.commands: list[list[str]] = [x.commands for x in processed_details.rover_details]

    def _instantiate_rovers(self, rover_setup: list[RoverSetup]) -> None:
        for i, details in enumerate(rover_setup):
            self.rovers[i] = Rover(details, i)

    def control_rovers(self) -> None:
        for i in range(len(self.rovers)):
            self._control_rover(i, self.commands[i])

    def _control_rover(self, _id: int, instructions: list[str]) -> Rover:
        for command in instructions:
            if command == "L" or command == "R":
                self.rovers[_id].change_direction(command)
            elif command == "M":
                self._move_rover(_id)
        return self.rovers[_id]

    def _move_rover(self, _id: int):
        new_coords: Coordinates = self.rovers[_id].look_ahead()
        self._check_matching_positions(_id, new_coords)
        self._check_coords_in_grid(_id, new_coords)
        self.rovers[_id].move()

    def _check_matching_positions(self, _id: int, position: Coordinates) -> None:
        res: list[Rover] = list(filter(lambda x: x.rover_id != _id and x.position() == position, self.rovers.values()))
        if len(res) > 0:
            raise PositionBlockedException(_id, res[0].rover_id, position)

    def _check_coords_in_grid(self, _id: int, position: Coordinates) -> None:
        if 0 <= position.x <= self.dims.x and 0 <= position.y <= self.dims.y:
            return
        raise PositionOutOfBoundsException(_id, position)

    def format_output(self) -> list[str]:
        return [f"{r.position().x} {r.position().y} {r.bearing()}" for r in self.rovers.values()]
