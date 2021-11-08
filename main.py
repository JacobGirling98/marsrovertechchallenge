from src.controller import Controller
from src.reader import Reader


def mars_rover_challenge():
    reader = Reader("input.txt")
    controller = Controller(reader)
    controller.control_rovers()
    [print(res) for res in controller.format_output()]


if __name__ == '__main__':
    mars_rover_challenge()
