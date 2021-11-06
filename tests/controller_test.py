import numpy as np
from _pytest.fixtures import fixture

from src.controller import Controller
from src.rover import Rover


@fixture
def controller():
    return Controller("input.txt")


def test_control_rover(controller):
    rover = Rover([1, 2, "N"], [5, 6])
    expected = Rover([1, 3, "N"], [5, 6])

    actual = controller.control_rover(rover, "LMLMLMLMM")

    assert (actual.position() == expected.position()).all()
    assert (actual.direction() == expected.direction()).all()


def test_process_rovers(controller):
    final_rovers = controller.process_rovers()

    assert (final_rovers[0].position() == np.array([1, 3])).any()
    assert (final_rovers[0].direction() == np.array([0, 1])).any()
    assert (final_rovers[1].position() == np.array([5, 1])).any()
    assert (final_rovers[1].direction() == np.array([1, 0])).any()


def test_correct_output(controller):
    expected = ["1 3 N", "5 1 E"]
    rovers = [
        Rover([1, 3, "N"], [5, 6]),
        Rover([5, 1, "E"], [5, 6])
    ]

    actual = controller.format_output(rovers)

    assert actual == expected
