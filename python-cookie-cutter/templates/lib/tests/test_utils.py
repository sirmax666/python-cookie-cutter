import pytest
from .. import utils


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        ([1,2,3], 6),
        ([1,2,3,4], 10)
    ]
)
def test_addition(args, expected):
    """Test function for addition
    
    Testing multiple scenarios with parametrize andarguments given as
    parameters.
    """
    assert utils.addition(*args) == expected
