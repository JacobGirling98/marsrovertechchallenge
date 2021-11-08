from src.dataclasses.coordinates import Coordinates


class PositionOutOfBoundsException(Exception):

    def __init__(self, _id: int, coordinates: Coordinates):
        self._id: int = _id
        self.coordinates: Coordinates = coordinates
        super().__init__(f"Rover {self._id} tried to move to out of bounds position: x = {self.coordinates.x}, y = {self.coordinates.y}")
