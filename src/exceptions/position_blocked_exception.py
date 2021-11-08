from src.dataclasses.coordinates import Coordinates


class PositionBlockedException(Exception):

    def __init__(self, rover_id: int, obstacle_id: int, coordinates: Coordinates):
        self.rover_id = rover_id
        self.obstacle_id = obstacle_id
        self.coordinates = coordinates
        super().__init__(f"Rover {self.rover_id} blocked from moving to"
                         f" [{self.coordinates.x}, {self.coordinates.y}] by Rover {self.obstacle_id}")
