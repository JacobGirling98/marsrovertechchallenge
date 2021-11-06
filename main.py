from src.controller import Controller


def mars_rover_challenge():
    controller = Controller("input.txt")
    rovers = controller.process_rovers()
    [print(res) for res in controller.format_output(rovers)]


if __name__ == '__main__':
    mars_rover_challenge()
