from src.reader import Reader
from src.rover import Rover


class Controller:

    reader = Reader("input.txt")

    def control_rover(self, rover, instructions):
        for command in instructions:
            if command == "L" or command == "R":
                rover.change_direction(command)
            elif command == "M":
                rover.move()
        return rover.position()

    def process_rovers(self):
        grid_size, instructions = self.reader.process_input()
        rovers = []
        for row in instructions:
            rover = Rover(row[0], grid_size)
            self.control_rover(rover, instructions[1])
            rovers.append(rover)
        return rovers


