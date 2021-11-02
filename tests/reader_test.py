from _pytest.fixtures import fixture

from src.reader import Reader


@fixture
def reader():
    return Reader("input.txt")


def test_read_input(reader):
    data = reader.read_input()
    assert data[0] == "5 5"
    assert data[1] == "1 2 N"
    assert data[2] == "LMLMLMLMM"
    assert data[3] == "3 3 E"
    assert data[4] == "MMRMMRMRRM"


def test_get_top_grid(reader):
    top_grid = reader.top_grid(["5 5"])
    assert top_grid == [5, 5]


def test_get_position(reader):
    position = reader.get_position("1 2 N")
    assert position == [1, 2, "N"]


def test_get_instructions(reader, mocker):
    mocker.patch.object(reader, "get_position")
    reader.get_position.return_value = [1, 1, "A"]

    instructions = reader.get_instructions(["5 5", "1 2 N", "LMLMLMLMM", "3 3 E", "MMRMMRMRRM"])
    assert instructions[0] == [[1, 1, "A"], ["L", "M", "L", "M", "L", "M", "L", "M", "M"]]
    assert instructions[1] == [[1, 1, "A"], ["M", "M", "R", "M", "M", "R", "M", "R", "R", "M"]]
