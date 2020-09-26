import pytest
from .context.catan.core.board_components import Tile, Edge, Intersection, Edge, Harbor

def test_valid_tile_kind():
    valid_tile_kind_data = {
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
    for elem in valid_tile_kind_data['assert_raises']:
        with pytest.raises(AssertionError):
            Tile.LocalChecker.valid_tile_kind(elem)

    for elem in valid_tile_kind_data['pass']:
        Tile.LocalChecker.valid_tile_kind(elem)

def test_valid_tile_token():
    valid_tile_token_data = {
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
    for elem in valid_tile_token_data['assert_raises']:
        with pytest.raises(AssertionError):
            Tile.LocalChecker.valid_tile_token(elem)

    for elem in valid_tile_token_data['pass']:
        Tile.LocalChecker.valid_tile_token(elem)

def test_tile_init():
    tile_init_data = {
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
    for elem in tile_init_data['assert_raises']:
        with pytest.raises(AssertionError):
            x = Tile(elem[0], elem[1], elem[2])

    for elem in tile_init_data['pass']:
            x = Tile(elem[0], elem[1], elem[2])
            assert x.coords == elem[0]
            assert x.kind == elem[1]
            assert x.token == elem[2]

def test_intersection_coords():
    intersection_coords_data =(
                (((5,9), 'wood', 9),((5,9), (6,9), (6,8), (5,8), (4,8), (4,9))),
                (((7,3), 'ore', 3),((7,3), (8,3), (8,2), (7,2), (6,2), (6,3))),
                (((2,5), 'desert', None),((2,5), (3,5), (3,4), (2,4), (1,4), (1,5)))
            )
    for elem in intersection_coords_data:
        x = Tile(elem[0][0], elem[0][1], elem[0][2])
        assert len(x.intersection_coords()) == len(elem[1])
        for coord in x.intersection_coords():
            assert coord in elem[1]

def test_edge_coords():
    edge_coords_data =(
                (((5,9), 'wood', 9),((5.5,9), (6,8.5), (5.5,8), (4.5,8), (4,8.5), (4.5,9))),
                (((7,3), 'ore', 3),((7.5,3), (8,2.5), (7.5,2), (6.5,2), (6,2.5), (6.5,3))),
                (((2,5), 'desert', None),((2.5,5), (3,4.5), (2.5,4), (1.5,4), (1,4.5), (1.5,5)))
            )
    for elem in edge_coords_data:
        x = Tile(elem[0][0], elem[0][1], elem[0][2])
        assert len(x.edge_coords()) == len(elem[1])
        for coord in x.edge_coords():
            assert coord in elem[1]

def test_tile_str():
    tile_str_data =(
                (((2,6), 'brick', 2),"Brick tile at (2, 6) with a token of 2"),
                (((4, 7), 'desert', None),"Desert tile at (4, 7) with a token of None")
                )
    for elem in tile_str_data:
        x = Tile(elem[0][0], elem[0][1], elem[0][2])
        assert str(x) == elem[1]

def test_harbor_init():
    harbor_init_data = {
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
    for elem in harbor_init_data['assert_raises']:
        with pytest.raises(AssertionError):
            x = Harbor(elem[0], elem[1])

    for elem in harbor_init_data['pass']:
        x = Harbor(elem[0], elem[1])

def test_harbor_str():
    harbor_str_data =(
                (((4,10), {'kind': 'wood', 'quantity': 2}),"Harbor at (4, 10) trading 2 wood for 1"),
                (((3,5), {'kind': None, 'quantity': 3}),"Harbor at (3, 5) trading 3 anything for 1")
            )
    for elem in harbor_str_data:
        x = Harbor(elem[0][0], elem[0][1])
        assert str(x) == elem[1]

