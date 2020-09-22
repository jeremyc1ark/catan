import pytest
from board import Tile, Harbor

@pytest.fixture
def value_handler_data():
    data = {
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
    return data

@pytest.fixture
def is_coord_data():
    data = {
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
    return data

@pytest.fixture
def is_edge_coord_data():
    data = {
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
    return data

@pytest.fixture
def is_intersection_coord_data():
    data = {
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
    return data

@pytest.fixture
def valid_tile_kind_data():
    data = {
            "assert_raises": (
                1,
                2,
                'dog',
                'foo',
                ()
            ),
            "pass": (
                'desert',
                'wood',
                'ore',
                'sheep',
                'brick',
                'wheat'
            )
        }
    return data

@pytest.fixture
def valid_tile_token_data():
    data = {
                "assert_raises": (
                    1,
                    13,
                    2.5,
                    'hello'
                ),
                "pass": (
                    2,
                    12,
                    None
                )
            }
    return data

@pytest.fixture
def tile_init_data():
    data = {
            "assert_raises": (
                ((1,2.5), 'wood', 4),
                ((1,4), 'foo', 3),
                ((5,2), 'wheat', 1),
                ((7,3), 'desert', 6),
                ((3,6), 'ore', 7),
                ((3,6), 'ore', None),
                ('foo', 3, 'bar')
            ),
            "pass": (
                ((4,5), 'wheat', 8),
                ((5,4), 'brick', 2),
                ((3,9), 'desert', None)
            )
        }
    return data

@pytest.fixture
def intersection_coords_data():
    data = (
            # Use this to generate data for Tile.intersections
            (((5,9), 'wood', 9),((5,9), (6,9), (6,8), (5,8), (4,8), (4,9))),
            (((7,3), 'ore', 3),((7,3), (8,3), (8,2), (7,2), (6,2), (6,3))),
            (((2,5), 'desert', None),((2,5), (3,5), (3,4), (2,4), (1,4), (1,5)))
        )
    return data

@pytest.fixture
def edge_coords_data():
    data = (
            # Use this to generate data for Tile.edges
            (((5,9), 'wood', 9),((5.5,9), (6,8.5), (5.5,8), (4.5,8), (4,8.5), (4.5,9))),
            (((7,3), 'ore', 3),((7.5,3), (8,2.5), (7.5,2), (6.5,2), (6,2.5), (6.5,3))),
            (((2,5), 'desert', None),((2.5,5), (3,4.5), (2.5,4), (1.5,4), (1,4.5), (1.5,5)))
        )
    return data


@pytest.fixture
def tile_str_data():
    data = (
            (((2,6), 'brick', 2),"Brick tile at (2, 6) with a token of 2"),
            (((4, 7), 'desert', None),"Desert tile at (4, 7) with a token of None")
            )
    return data


@pytest.fixture
def harbor_str_data():
    data = (
            (((4,10), {'kind': 'wood', 'quantity': 2}),"Harbor at (4, 10) trading 2 wood for 1"),
            (((3,5), {'kind': None, 'quantity': 3}),"Harbor at (3, 5) trading 3 anything for 1")
        )
    return data

@pytest.fixture
def harbor_init_data():
    data = {
        "assert_raises": (
            ((3.5,5), {'kind': None, 'quantity': 3}),
            ({3,5}, {'kind': None, 'quantity': 3}),
            ((3,5,2), {'quantity': 3}),
            ((3,5), {'kind': None, 'quantity': 3.5}),
            ((3,5), {'kind': None, 'quantity': 'foo'}),
            ((3,5), {'kind': None}),
            ((3,5), {'kind': 'foo', 'quantity': 3}),
            ((3,5), {'bar': 5, 'kind': None, 'quantity': 3}),
            ((3,5), {'foo': None, 'bar': 3})
        ),
        "pass": (
            ((3,5), {'kind': None, 'quantity': 3}),
            ((3,5), {'kind': 'sheep', 'quantity': 2})
        )
    }
    return data

@pytest.fixture
def intersection_coords_for_tile_list():
    data = (
        (5,3),
        (4,3),
        (3,3),
        (2,3),
        (1,3),
        (6,2),
        (5,2),
        (4,2),
        (3,2),
        (2,2),
        (1,2),
        (0,2),
        (6,1),
        (5,1),
        (4,1),
        (3,1),
        (2,1),
        (1,1),
        (0,1),
        (5,0),
        (4,0),
        (3,0),
        (2,0),
        (1,0)
    )
    return data

@pytest.fixture
def edge_coords_for_tile_list():
    data = (
        (1.5,0),
        (2.5,0),
        (3.5,0),
        (4.5,0),
        (0.5,1),
        (1.5,1),
        (2.5,1),
        (3.5,1),
        (4.5,1),
        (5.5,1),
        (0.5,2),
        (1.5,2),
        (2.5,2),
        (3.5,2),
        (4.5,2),
        (5.5,2),
        (1.5,3),
        (2.5,3),
        (3.5,3),
        (4.5,3),
        (1,0.5),
        (3,0.5),
        (5,0.5),
        (0,1.5),
        (2,1.5),
        (4,1.5),
        (6,1.5),
        (1,2.5),
        (3,2.5),
        (5,2.5)
    )
    return data
