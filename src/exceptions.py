class PositionOutOfBoundsException(Exception):

    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        super().__init__(f"Tried to move to out of bounds position: x={self.x}, y={self.y}")
