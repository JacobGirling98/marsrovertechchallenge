import numpy as np

from src.dataclasses.coordinates import Coordinates
from src.dataclasses.rover_setup import RoverSetup


class Rover:

    _next_position: np.array

    def __init__(self, initial_position: RoverSetup, _id: int):
        self._position: np.array = np.array([initial_position.position.x, initial_position.position.y])
        self._direction: np.array = self._set_initial_direction(initial_position.direction)
        self.rover_id: int = _id

    def _set_initial_direction(self, direction: str) -> np.array:
        directions = {
            "N": np.array([0, 1]),
            "E": np.array([1, 0]),
            "S": np.array([0, -1]),
            "W": np.array([-1, 0])
        }
        return directions[direction]

    def change_direction(self, direction: str) -> np.array:
        angle = np.pi / 2 if direction == "L" else -np.pi / 2
        self._direction = np.matmul(self._rotation_matrix(angle), self._direction).astype(int)

    def move(self) -> None:
        # if not self._valid_position(new_position):
        #     raise PositionOutOfBoundsException(new_position)
        self._position = self._next_position

    def look_ahead(self) -> Coordinates:
        self._next_position = self._position + self._direction
        return Coordinates(self._next_position[0], self._next_position[1])

    def _rotation_matrix(self, angle: float) -> np.array:
        return np.array([[np.cos(angle), -np.sin(angle)],
                         [np.sin(angle), np.cos(angle)]])

    # def _valid_position(self, new_position: np.array) -> bool:
    #     return 0 <= new_position[0] <= self._max_x and 0 <= new_position[1] <= self._max_y

    def position(self) -> Coordinates:
        return Coordinates(self._position[0], self._position[1])

    def direction(self) -> Coordinates:
        return Coordinates(self._direction[0], self._direction[1])

    def bearing(self):
        directions = {
            (0, 1): "N",
            (1, 0): "E",
            (0, -1): "S",
            (-1, 0): "W"
        }
        return directions[tuple(self._direction)]

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Rover):
            return (self._position == o._position).any() and (
                    self._direction == o._direction).any() and self.rover_id == o.rover_id
        return False
