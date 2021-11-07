from _pytest.fixtures import fixture

from src.controller import Controller
from src.dataclasses.coordinates import Coordinates
from src.dataclasses.processed_input import ProcessedInput
from src.dataclasses.rover_details import RoverDetails
from src.dataclasses.rover_setup import RoverSetup
from src.reader import Reader
from src.rover import Rover


@fixture
def reader():
    return Reader("input.txt")


@fixture
def controller(reader):
    controller = Controller(reader)
    rovers = [
        Rover(RoverSetup(Coordinates(1, 1), "N"), 0),
        Rover(RoverSetup(Coordinates(2, 2), "N"), 1),
        Rover(RoverSetup(Coordinates(3, 3), "N"), 2)
    ]
    controller.rovers = {i: rovers[i] for i in range(3)}
    controller.grid = [[0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, rovers[2], 0],
                       [0, 0, rovers[1], 0, 0],
                       [0, rovers[0], 0, 0, 0],
                       [0, 0, 0, 0, 0]]
    controller.dims = Coordinates(5, 6)
    controller.commands = [
        ["L", "M"],
        ["M"],
        ["R", 'M']
    ]
    return controller


def test_control_rover(controller):
    expected = Rover(RoverSetup(Coordinates(1, 2), "N"), 0)

    actual = controller.control_rover(0, ["L", "M", "L", "M", "L", "M", "L", "M", "M"])

    assert actual == expected


def test_process_rovers(controller):
    controller.process_rovers()

    expected: dict[int, Rover] = {
        0: Rover(RoverSetup(Coordinates(0, 1), "W"), 0),
        1: Rover(RoverSetup(Coordinates(2, 3), "N"), 1),
        2: Rover(RoverSetup(Coordinates(4, 3), "E"), 2)
    }

    assert controller.rovers == expected


def test_correct_output(controller):
    expected = ["1 3 N", "5 1 E"]
    rovers = [
        Rover(RoverSetup(Coordinates(1, 3), "N"), 0),
        Rover(RoverSetup(Coordinates(5, 1), "E"), 1)
    ]
    controller.rovers = {i: rovers[i] for i in range(len(rovers))}

    actual = controller.format_output()

    assert actual == expected


def test_instantiate_grid(controller):
    controller.instantiate_grid(Coordinates(5, 6))

    assert controller.grid == [[0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0]]


def test_instantiate_rovers(controller):
    rover_setups: list[RoverSetup] = [
        RoverSetup(Coordinates(1, 1), "N"),
        RoverSetup(Coordinates(2, 2), "N"),
        RoverSetup(Coordinates(3, 3), "N")
    ]
    expected_rovers = {i: Rover(rover_setups[i], i) for i in range(3)}

    controller.instantiate_rovers(rover_setups)

    assert controller.rovers == expected_rovers


def test_add_rovers_to_grid(controller):
    rover_a = Rover(RoverSetup(Coordinates(1, 1), "N"), 0)
    rover_b = Rover(RoverSetup(Coordinates(2, 2), "N"), 1)
    rover_c = Rover(RoverSetup(Coordinates(3, 3), "N"), 2)
    rovers = {0: rover_a, 1: rover_b, 2: rover_c}

    controller.add_rovers_to_grid(rovers)

    assert controller.grid == [[0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, rover_c, 0],
                               [0, 0, rover_b, 0, 0],
                               [0, rover_a, 0, 0, 0],
                               [0, 0, 0, 0, 0]]


def test_transform_coords(controller):
    controller.instantiate_grid(Coordinates(5, 6))

    assert controller.transform_coords(5) == 1
    assert controller.transform_coords(1) == 5
    assert controller.transform_coords(0) == 6


def test_find_rover(controller):
    rover_a = Rover(RoverSetup(Coordinates(1, 2), "N"), 0)
    rover_b = Rover(RoverSetup(Coordinates(1, 0), "N"), 1)
    rover_c = Rover(RoverSetup(Coordinates(4, 3), "N"), 2)
    rover_d = Rover(RoverSetup(Coordinates(3, 5), "N"), 3)
    controller.rovers = [rover_a, rover_b, rover_c, rover_d]
    controller.grid = [[0, 0, 0, 0, 0],
                       [0, 0, 0, rover_d, 0],
                       [0, 0, 0, rover_c, 0],
                       [0, 0, rover_a, 0, 0],
                       [0, rover_b, 0, 0, 0],
                       [0, 0, 0, 0, 0]]
    controller.dims = Coordinates(5, 6)

    assert controller.find_rover(0) == Coordinates(2, 2)
    assert controller.find_rover(1) == Coordinates(1, 1)
    assert controller.find_rover(2) == Coordinates(3, 3)
    assert controller.find_rover(3) == Coordinates(3, 4)


def test_update_grid(controller):
    rover_a = Rover(RoverSetup(Coordinates(1, 2), "N"), 0)
    rover_b = Rover(RoverSetup(Coordinates(1, 0), "N"), 1)
    rover_c = Rover(RoverSetup(Coordinates(4, 3), "N"), 2)
    rover_d = Rover(RoverSetup(Coordinates(3, 5), "N"), 3)
    controller.rovers = [rover_a, rover_b, rover_c, rover_d]
    controller.grid = [[0, 0, 0, 0, 0],
                       [0, 0, 0, rover_d, 0],
                       [0, 0, 0, rover_c, 0],
                       [0, 0, rover_a, 0, 0],
                       [0, rover_b, 0, 0, 0],
                       [0, 0, 0, 0, 0]]

    controller.update_grid(0)
    controller.update_grid(1)
    controller.update_grid(2)
    controller.update_grid(3)

    assert controller.grid == [[0, 0, 0, rover_d, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, rover_c],
                               [0, rover_a, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, rover_b, 0, 0, 0]]


def test_setup(controller, reader, mocker):
    rover_details = [
        RoverDetails(RoverSetup(Coordinates(1, 1), "N"), ["L", "M"]),
        RoverDetails(RoverSetup(Coordinates(2, 2), "N"), ["M"]),
        RoverDetails(RoverSetup(Coordinates(3, 3), "N"), ["R", "M"]),
    ]
    mocked_input = ProcessedInput(Coordinates(5, 5), rover_details)
    mocker.patch.object(reader, "process_input")
    reader.process_input.return_value = mocked_input
    expected_rovers = {i: Rover(rover_details[i].rover_setup, i) for i in range(len(rover_details))}

    controller.setup()

    assert controller.rovers == expected_rovers
    assert controller.grid == [[0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, expected_rovers[2], 0, 0],
                               [0, 0, expected_rovers[1], 0, 0, 0],
                               [0, expected_rovers[0], 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0]]
    assert controller.commands == [
        ["L", "M"],
        ["M"],
        ["R", 'M']
    ]
