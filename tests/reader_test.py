from _pytest.fixtures import fixture

from src.dataclasses.processed_input import ProcessedInput
from src.dataclasses.rover_instructions import RoverInstructions
from src.reader import Reader


@fixture
def reader() -> Reader:
    return Reader("input.txt")


def test_read_input(reader):
    data: list[str] = reader._read_input()

    assert data[0] == "5 5"
    assert data[1] == "1 2 N"
    assert data[2] == "LMLMLMLMM"
    assert data[3] == "3 3 E"
    assert data[4] == "MMRMMRMRRM"


def test_get_top_grid(reader):
    top_grid: list[int] = reader._top_grid(["5 5"])

    assert top_grid == [5, 5]


def test_get_position(reader):
    position: list[int and str] = reader._get_position("1 2 N")

    assert position == [1, 2, "N"]


def test_get_instructions(reader, mocker):
    mocker.patch.object(reader, "_get_position")
    reader._get_position.return_value = [1, 1, "A"]

    instructions: list[RoverInstructions] = reader._get_instructions(
        ["5 5", "1 2 N", "LMLMLMLMM", "3 3 E", "MMRMMRMRRM"])

    assert instructions[0] == RoverInstructions([1, 1, "A"], ["L", "M", "L", "M", "L", "M", "L", "M", "M"])
    assert instructions[1] == RoverInstructions([1, 1, "A"], ["M", "M", "R", "M", "M", "R", "M", "R", "R", "M"])


def test_process_input(reader, mocker):
    mocker.patch.object(reader, "_top_grid")
    reader._top_grid.return_value = [5, 6]
    mocker.patch.object(reader, "_get_instructions")
    reader._get_instructions.return_value = \
        [RoverInstructions([1, 1, "A"], ["L", "M", "L", "M", "L", "M", "L", "M", "M"])]

    actual: ProcessedInput = reader.process_input()

    assert actual.grid_size == [5, 6]
    assert actual.rover_details == [RoverInstructions([1, 1, "A"], ["L", "M", "L", "M", "L", "M", "L", "M", "M"])]
