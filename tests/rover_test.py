import numpy as np
import pytest
from _pytest.fixtures import fixture

from src.exceptions import PositionOutOfBoundsException
from src.rover import Rover


@fixture
def rover():
    rover = Rover([1, 2, "N"], [5, 6])
    rover._position = np.array([1, 2])
    rover._direction = np.array([0, 1])
    rover._max_x = 5
    rover._max_y = 6
    return rover


def test_create_rover():
    rover = Rover([1, 2, "N"], [5, 6])
    assert (rover._position == np.array([1, 2])).all()
    assert (rover._direction == np.array([0, 1])).all()
    assert rover._max_x == 5
    assert rover._max_y == 6


def test_set_starting_direction(rover):
    direction1 = rover._set_initial_direction("N")
    direction2 = rover._set_initial_direction("E")
    direction3 = rover._set_initial_direction("S")
    direction4 = rover._set_initial_direction("W")

    assert (direction1 == np.array([0, 1])).all()
    assert (direction2 == np.array([1, 0])).all()
    assert (direction3 == np.array([0, -1])).all()
    assert (direction4 == np.array([-1, 0])).all()


def test_rotation_matrix(rover):
    anticlockwise_matrix = rover._rotation_matrix(np.pi / 2)
    clockwise_matrix = rover._rotation_matrix(-np.pi / 2)

    assert (clockwise_matrix == np.array([[0, 1],
                                          [-1, 0]])).any()
    assert (anticlockwise_matrix == np.array([[0, -1],
                                              [1, 0]])).any()


def test_change_direction(rover):
    rover.change_direction("L")
    assert (rover._direction == np.array([-1, 0])).all()

    rover.change_direction("L")
    assert (rover._direction == np.array([0, -1])).all()

    rover.change_direction("L")
    assert (rover._direction == np.array([1, 0])).all()

    rover.change_direction("L")
    assert (rover._direction == np.array([0, 1])).all()

    rover.change_direction("R")
    assert (rover._direction == np.array([1, 0])).all()

    rover.change_direction("R")
    assert (rover._direction == np.array([0, -1])).all()

    rover.change_direction("R")
    assert (rover._direction == np.array([-1, 0])).all()

    rover.change_direction("R")
    assert (rover._direction == np.array([0, 1])).all()


def test_move(rover):
    rover.move()
    assert (rover._position == np.array([1, 3])).all()

    rover._direction = np.array([1, 0])
    rover.move()
    assert (rover._position == np.array([2, 3])).all()

    rover._direction = np.array([0, -1])
    rover.move()
    assert (rover._position == np.array([2, 2])).all()

    rover._direction = np.array([-1, 0])
    rover.move()
    assert (rover._position == np.array([1, 2])).all()


def test_move_out_of_bounds(rover, mocker):
    mocker.patch.object(rover, "valid_position")
    rover.valid_position.return_value = False

    with pytest.raises(PositionOutOfBoundsException) as e:
        assert rover.move()
    assert str(e.value) == "Tried to move to out of bounds position: x=1, y=3"


def test_valid_position(rover):
    assert rover.valid_position(np.array([1, 1]))
    assert rover.valid_position(np.array([0, 0]))
    assert rover.valid_position(np.array([5, 6]))
    assert not rover.valid_position(np.array([-1, 1]))
    assert not rover.valid_position(np.array([1, -1]))
    assert not rover.valid_position(np.array([-1, -1]))
    assert not rover.valid_position(np.array([7, 1]))
    assert not rover.valid_position(np.array([1, 7]))
    assert not rover.valid_position(np.array([7, 7]))
