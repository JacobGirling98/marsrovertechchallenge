import numpy as np

from src.exceptions.position_out_of_bounds_exception import PositionOutOfBoundsException


class Rover:

    def __init__(self, initial_position: list, grid_size: list):
        self._position = np.array([initial_position[0], initial_position[1]])
        self._direction = self._set_initial_direction(initial_position[2])
        self._max_x = grid_size[0]
        self._max_y = grid_size[1]

    def _set_initial_direction(self, direction: str) -> np.array:
        directions = {
            "N": np.array([0, 1]),
            "E": np.array([1, 0]),
            "S": np.array([0, -1]),
            "W": np.array([-1, 0])
        }
        return directions[direction]

    def _rotation_matrix(self, angle: float) -> np.array:
        return np.array([[np.cos(angle), -np.sin(angle)],
                         [np.sin(angle), np.cos(angle)]])

    def change_direction(self, direction: str) -> np.array:
        angle = np.pi / 2 if direction == "L" else -np.pi / 2
        self._direction = np.matmul(self._rotation_matrix(angle), self._direction).astype(int)

    def move(self) -> None:
        new_position = self._position + self._direction
        if not self._valid_position(new_position):
            raise PositionOutOfBoundsException(new_position)
        self._position = new_position

    def _valid_position(self, new_position: np.array) -> bool:
        return 0 <= new_position[0] <= self._max_x and 0 <= new_position[1] <= self._max_y

    def position(self):
        return self._position

    def direction(self):
        return self._direction

    def bearing(self):
        directions = {
            (0, 1): "N",
            (1, 0): "E",
            (0, -1): "S",
            (-1, 0): "W"
        }
        return directions[tuple(self.direction())]
