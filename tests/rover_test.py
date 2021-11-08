import numpy as np
from _pytest.fixtures import fixture

from src.dataclasses.coordinates import Coordinates
from src.dataclasses.rover_setup import RoverSetup
from src.rover import Rover


@fixture
def rover():
    position = Coordinates(1, 2)
    rover_setup = RoverSetup(position, "N")
    rover = Rover(rover_setup, 0)
    rover._position = np.array([1, 2])
    rover._direction = np.array([0, 1])
    return rover


def test_create_rover():
    position = Coordinates(2, 2)
    rover_setup = RoverSetup(position, "N")
    rover = Rover(rover_setup, 0)

    assert (rover._position == np.array([2, 2])).all()
    assert (rover._direction == np.array([0, 1])).all()
    assert rover.rover_id == 0


def test_set_initial_direction(rover):
    direction1: np.array = rover._set_initial_direction("N")
    direction2: np.array = rover._set_initial_direction("E")
    direction3: np.array = rover._set_initial_direction("S")
    direction4: np.array = rover._set_initial_direction("W")

    assert (direction1 == np.array([0, 1])).all()
    assert (direction2 == np.array([1, 0])).all()
    assert (direction3 == np.array([0, -1])).all()
    assert (direction4 == np.array([-1, 0])).all()


def test_rotation_matrix(rover):
    anticlockwise_matrix: np.array = rover._rotation_matrix(np.pi / 2)
    clockwise_matrix: np.array = rover._rotation_matrix(-np.pi / 2)

    assert (clockwise_matrix == np.array([[0, 1],
                                          [-1, 0]])).any()
    assert (anticlockwise_matrix == np.array([[0, -1],
                                              [1, 0]])).any()


def test_change_direction(rover):
    rover.change_direction("L")
    assert (rover._direction == np.array([-1, 0])).all()
    assert rover.direction() == Coordinates(-1, 0)

    rover.change_direction("L")
    assert (rover._direction == np.array([0, -1])).all()
    assert rover.direction() == Coordinates(0, -1)

    rover.change_direction("L")
    assert (rover._direction == np.array([1, 0])).all()
    assert rover.direction() == Coordinates(1, 0)

    rover.change_direction("L")
    assert (rover._direction == np.array([0, 1])).all()
    assert rover.direction() == Coordinates(0, 1)

    rover.change_direction("R")
    assert (rover._direction == np.array([1, 0])).all()
    assert rover.direction() == Coordinates(1, 0)

    rover.change_direction("R")
    assert (rover._direction == np.array([0, -1])).all()
    assert rover.direction() == Coordinates(0, -1)

    rover.change_direction("R")
    assert (rover._direction == np.array([-1, 0])).all()
    assert rover.direction() == Coordinates(-1, 0)

    rover.change_direction("R")
    assert (rover._direction == np.array([0, 1])).all()
    assert rover.direction() == Coordinates(0, 1)


def test_look_ahead(rover):
    rover.look_ahead()
    assert rover.look_ahead() == Coordinates(1, 3)
    assert (rover._next_position == np.array([1, 3])).all()

    rover._direction = np.array([1, 0])
    assert rover.look_ahead() == Coordinates(2, 2)
    assert (rover._next_position == np.array([2, 2])).all()

    rover._direction = np.array([0, -1])
    rover.look_ahead()
    assert rover.look_ahead() == Coordinates(1, 1)
    assert (rover._next_position == np.array([1, 1])).all()

    rover._direction = np.array([-1, 0])
    rover.look_ahead()
    assert rover.look_ahead() == Coordinates(0, 2)
    assert (rover._next_position == np.array([0, 2])).all()


def test_move(rover):
    rover._next_position = np.array([1, 2])

    rover.move()

    assert (rover._position == np.array([1, 2])).any()
    assert rover.position() == Coordinates(1, 2)


# def test_move_out_of_bounds(rover, mocker):
#     mocker.patch.object(rover, "_valid_position")
#     rover._valid_position.return_value = False
#
#     with pytest.raises(PositionOutOfBoundsException) as e:
#         assert rover.move()
#     assert str(e.value) == "Tried to move to out of bounds position: x=1, y=3"
#
#
# def test_valid_position(rover):
#     assert rover._valid_position(np.array([1, 1]))
#     assert rover._valid_position(np.array([0, 0]))
#     assert rover._valid_position(np.array([5, 6]))
#     assert not rover._valid_position(np.array([-1, 1]))
#     assert not rover._valid_position(np.array([1, -1]))
#     assert not rover._valid_position(np.array([-1, -1]))
#     assert not rover._valid_position(np.array([7, 1]))
#     assert not rover._valid_position(np.array([1, 7]))
#     assert not rover._valid_position(np.array([7, 7]))


def test_bearing(rover):
    rover.change_direction("L")
    assert rover.bearing() == "W"

    rover.change_direction("L")
    assert rover.bearing() == "S"

    rover.change_direction("L")
    assert rover.bearing() == "E"

    rover.change_direction("L")
    assert rover.bearing() == "N"
