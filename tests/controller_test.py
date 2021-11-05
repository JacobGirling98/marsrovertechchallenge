from _pytest.fixtures import fixture
import numpy as np

from src.controller import Controller
from src.rover import Rover


@fixture
def controller():
    return Controller()


def test_control_rover(controller):
    rover = Rover([1, 2, "N"], [5, 6])
    final_position = controller.control_rover(rover, "LMLMLMLMM")
    assert (final_position == np.array([1, 3])).all()

def test_process_rovers(controller):
    final_rovers = [Rover([1, 3, "N"], [5, 6]), Rover([5, 1, "E"], [5, 6])]

    final_rovers = controller.process_rovers()

    assert final_rovers[0].position() == np.array([1, 3])
    assert final_rovers[0].direction() == np.array([0, 1])
    assert final_rovers[1].position() == np.array([4, 1])
    assert final_rovers[1].direction() == np.array([1, 0])