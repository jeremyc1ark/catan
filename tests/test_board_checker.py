from decorate_all_methods import decorate_all_methods
import pytest
from catan.core.board_checker import BoardChecker

def test_value_handler():
    value_handler_data = {
                "assert_raises": (
                    (1, (2,3,4,5)),
                    (5, (3, 6, 5.5, 'r')),
                    ('hello', ()),
                    ('foo', []),
                    ([1,2,3], [[1,2], (), 'foo', 'cat'])
                ),
                "pass": (
                    (1, (1,2,3,4)),
                    (5, (3,6,5,'r')),
                    ([1,2,3], [[1,2,3], (), 'foo', 'cat'])
                )
            }
    for elem in value_handler_data['assert_raises']:
        with pytest.raises(AssertionError):
            BoardChecker.value_handler(elem[0], elem[1])

    for elem in value_handler_data['pass']:
        BoardChecker.value_handler(elem[0], elem[1])

def test_is_coord():
    is_coord_data = {
                "assert_raises": (
                    [1,2],
                    {'foo': 8, 'bar': 2},
                    (1,4,3,6,7,8),
                    (1,'dog'),
                    (0.33, 1)
                ),
                "pass": (
                    (5,7),
                    (2.5,3),
                    (2,4.5),
                    (1,2)
                )
            }
    for elem in is_coord_data['assert_raises']:
        with pytest.raises(AssertionError):
            BoardChecker.is_coord(elem)

    for elem in is_coord_data['pass']:
        BoardChecker.is_coord(elem)

def test_is_edge_coord():
    is_edge_coord_data = {
                "assert_raises": (
                    [1,2],
                    {'foo': 8, 'bar': 2},
                    (1,4,3,6,7,8),
                    (1,'dog'),
                    (0.33, 1),
                    (1,2),
                    (1, 1.55)
                ),
                "pass": (
                    (1,2.5),
                    (3.5,4),
                    (87.5,5)
                )
            }
    for elem in is_edge_coord_data['assert_raises']:
        with pytest.raises(AssertionError):
            BoardChecker.is_edge_coord(elem)

    for elem in is_edge_coord_data['pass']:
        BoardChecker.is_edge_coord(elem)

def test_is_intersection_coord():
    is_intersection_coord_data = {
                "assert_raises": (
                    [1,2],
                    {'foo': 8, 'bar': 2},
                    (1,4,3,6,7,8),
                    (1,'dog'),
                    (0.33, 1),
                    (1, 1.55)
                ),
                "pass": (
                    (5,7),
                    (7897,23423),
                    (32283,3)
                )
            }
    for elem in is_intersection_coord_data['assert_raises']:
        with pytest.raises(AssertionError):
            BoardChecker.is_intersection_coord(elem)

    for elem in is_intersection_coord_data['pass']:
        BoardChecker.is_intersection_coord(elem)

