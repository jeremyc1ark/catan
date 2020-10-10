"""

"""


def value_handler(passed_value, valid_args):
    """ Asserts that passed_value is in valid_args

    Args:
      passed_value: The value that you want to assert is in valid_args
      valid_args: A list of elements that passed_value must be a member of
    """

    assert isinstance(valid_args, tuple) or isinstance(valid_args, list), \
        'Argument <valid_args> must be of type tuple or list'
    assert (passed_value in valid_args), \
        f'{str(passed_value)} is not a valid argument'


def is_coord(passed_value):
    """ Asserts that passed_value is a valid coordinate


    """
    assert isinstance(passed_value, tuple), \
        f'{str(passed_value)} must be of type <tuple> or <list>'

    assert (len(passed_value) == 2), \
        f'{str(passed_value)} must be of length 2'

    assert all(
        isinstance(val, int) or
        isinstance(val, float)
        for val in passed_value
    ), \
        f'{str(passed_value)} must only contain types <int> or <float>'

    assert all((val - math.floor(val) in (0, 0.5)) for val in passed_value), \
        f'{str(passed_value)} can only contain integers or integers + 0.5'
