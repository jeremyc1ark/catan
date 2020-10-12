"""
Checker functions for setup and usage of board.

These functions are for general use whenever you need to check
that a given function is recieving the proper arguments.

Functions:
    is_coord(val)
    is_edge_coord(val)
    is_intersection_coord(val)
    is_road(val)
    is_settlement(val)
    is_city(val)

Classes:
    _is_edge_coord_Helpers
"""

import math
from typing import Any, Tuple, Union

from decorate_all_methods import decorate_all_methods


def is_coord(val: Any) -> bool:
    """Returns whether val is a valid coordinate

    In this case, a valid coordinate is a tuple with two integers or floats.

    Args:
        val: The value which you want to confirm is a coordinate
    """

    is_tuple = isinstance(val, tuple)
    is_len_2 = len(val) == 2
    has_only_nums = all(
        isinstance(val, int) or isinstance(val, float) for val in val)

    # If it satisfies these conditions, then it is a coordinate
    return is_tuple and is_len_2 and has_only_nums


@decorate_all_methods(staticmethod)
class _is_edge_coord_Helpers():
    """Helper functions for this module.

    Methods:
        between_two_ints(num)
        one_int_and_float(coord)
        float_in_coord(coord)
    """
    def between_two_ints(num: Union[int, float]) -> bool:
        """Returns whether num is an integer plus 0.5

        Args:
            num: Number of interest
        """

        return num - math.floor(num) == 0.5

    def one_of_int_and_float(
            coord: Tuple[Union[int, float], Union[int, float]]) -> bool:
        """Returns whether a tuple has one of both an int and float

        Args:
            coord: Coordinate, which is a tuple of two numbers
        """

        # Bools of whether there are ints and floats in coord
        has_int = any(isinstance(x, int) for x in coord)
        has_float = any(isinstance(x, float) for x in coord)

        # Both must eval to True for function to return True
        return has_float and has_int

    def float_in_coord(
            coord: Tuple[Union[int, float], Union[int, float]]) -> float:
        """Returns the first float in a tuple that it encounters

        Args:
            coord: Coordinate, which is a tuple of two numbers
        """

        for num in coord:
            if isinstance(num, float):
                return num


def is_edge_coord(val: Any) -> bool:
    """Returns whether the val is an edge coordinate.

    An edge coordinate must satisfy all of the conditions of a coordinate.
    In addition, an edge coordinate must contain one integer and one float.
    The float must be an integer plus 0.5.

    Args:
        val: The value which you want to confirm is an edge coordinate

    Dependent on:
        is_coord(val)
        _is_edge_coord_Helpers.one_of_int_and_float(coord)
        _is_edge_coord_Helpers.between_two_ints(num)
        _is_edge_coord_Helpers.float_in_coord(coord)
    """

    helpers = _is_edge_coord_Helpers

    is_a_coordinate = is_coord(val)
    has_one_int_and_float = helpers.one_of_int_and_float(val)
    float_is_midway = helpers.between_two_ints(helpers.float_in_coord(val))

    return is_a_coordinate and has_one_int_and_float and float_is_midway


def is_intersection_coord(val: Any) -> bool:
    """Returns whether the val is an intersection coordinate

    An intersection coordinate must satisfy all of the conditions of a
    coordinate. In addition, an intersection coordinate must consist of
    only two integers.

    Args:
        val: The value which you want to confirm is an edge coordinate

    Dependent on:
        is_coord(val)
    """

    is_a_coordinate = is_coord(val)
    is_all_ints = all(isinstance(x, int) for x in val)

    return is_a_coordinate and is_all_ints


def is_harbor(val: Any) -> bool:
    """Returns whether val is a harbor

    A harbor looks like the following:
    {'kind': 'harbor',
     'trade': <type of trade>,
     'quantity': <int>
     'coord': <intersections_coord>}
    Where <type of trade> is a member of
    (None, 'wood', 'sheep', 'ore', 'brick', 'wheat')
    Where <coord> is a value that returns True when passed into
    is_intersection_coord

    Args:
        val: The value which you want to confirm is a harbor

    Dependent on:
        is_intersection_coord(val)
    """

    valid_trades = {None, 'wood', 'sheep', 'ore', 'brick', 'wheat'}

    try:
        has_valid_trade = val['trade'] in valid_trades
        has_valid_quantity = isinstance(val['quantity'], int)
        has_valid_kind = val['kind'] == 'harbor'
        has_valid_coord = is_intersection_coord(val['coord'])
    except (KeyError, TypeError):
        return False

    return has_valid_quantity and \
        has_valid_trade and \
        has_valid_coord and \
        has_valid_kind


def is_road(val: Any) -> bool:
    """Returns whether val is a road

    A road looks like the following:
    {'kind': 'road',
     'owner_name': <str>,
     'coord': <edge_coord>}
    Where <edge_coord> is a value that returns True when passed to
    is_edge_coord

    Args:
        val: The value which you want to confirm is a road

    Dependent on:
        is_edge_coord(val)
    """

    try:
        has_valid_owner_name = isinstance(val['owner_name'], str)
        has_valid_coord = is_edge_coord(val['coord'])
        has_valid_kind = val['kind'] == 'road'
    except (KeyError, TypeError):
        return False

    return has_valid_owner_name and has_valid_coord and has_valid_kind


def is_settlement(val: Any) -> bool:
    """Returns whether val is a settlement

    A settlement looks like the following:
    {'kind': 'settlement',
     'owner_name': <str>,
     'coord': <edge_coord>}
    Where <edge_coord> is a value that returns True when passed to
    is_edge_coord

    Args:
        val: The value which you want to confirm is a settlement

    Dependent on:
        is_intersection_coord(val)
    """

    try:
        has_valid_owner_name = isinstance(val['owner_name'], str)
        has_valid_coord = is_intersection_coord(val['coord'])
        has_valid_kind = val['kind'] == 'settlement'
    except (KeyError, TypeError):
        return False

    return has_valid_owner_name and has_valid_coord and has_valid_kind


def is_city(val: Any) -> bool:
    """Returns whether val is a city

    A city looks like the following:
    {'kind': 'city',
     'owner_name': <str>,
     'coord': <edge_coord>}
    Where <edge_coord> is a value that returns True when passed to
    is_edge_coord

    Args:
        val: The value which you want to confirm is a city

    Dependent on:
        is_intersection_coord(val)
    """

    try:
        has_valid_owner_name = isinstance(val['owner_name'], str)
        has_valid_coord = is_intersection_coord(val['coord'])
        has_valid_kind = val['kind'] == 'city'
    except (KeyError, TypeError):
        return False

    return has_valid_owner_name and has_valid_coord and has_valid_kind
