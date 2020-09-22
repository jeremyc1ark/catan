import json
testing = {
    "BoardChecker": {
        "value_handler": {
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
        },

        "is_coord": {
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
        },

        "is_edge_coord": {
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
        },

        "is_intersection_coord": {
            "assert_raises": (
                [1,2],
                {'foo': 8, 'bar': 2},
                (1,4,3,6,7,8),
                (1,'dog'),
                (0.33, 1),
                (1, 1.55),
                (1.0,2)
            ),
            "pass": (
                (5,7),
                (7897,23423),
                (32283,3)
            )
        }
    },

    "Tile": {
        "LocalChecker": {
            "valid_tile_kind": {
                "assert_raises": (
                    1,
                    2,
                    'dog',
                    'foo',
                    ('desert')
                ),
                "pass": (
                    'desert',
                    'wood',
                    'ore',
                    'sheep',
                    'brick',
                    'wheat'
                )
            },
            "valid_tile_token": {
                "assert_raises": (
                    1,
                    13,
                    2.5,
                    'hello',
                    2.0
                ),
                "pass": (
                    2,
                    12,
                    None
                )
            }
        },
        "init": {
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
        },
        "intersection_coords": (
            # Use this to generate data for Tile.intersections
            (((5,9), 'wood', 9),((5,9), (6,9), (6,8), (5,8), (4,8), (4,9))),
            (((7,3), 'ore', 3),((7,3), (8,3), (8,2), (7,2), (6,2), (6,3))),
            (((2,5), 'desert', None),((2,5), (3,5), (3,4), (2,4), (1,4), (1,5)))
        ),
        "edge_coords": (
            # Use this to generate data for Tile.edges
            (((5,9), 'wood', 9),((5.5,9), (6,8.5), (5.5,8), (4.5,8), (4,8.5), (4.5,9))),
            (((7,3), 'ore', 3),((7.5,3), (8,2.5), (7.5,2), (6.5,2), (6,2.5), (6.5,3))),
            (((2,5), 'desert', None),((2.5,5), (3,4.5), (2.5,4), (1.5,4), (1,4.5), (1.5,5)))
        ),
        "str": (
            (((2,6), 'brick', 2),"Brick tile at (2, 6) with a token of 2"),
            (((4, 7), 'desert', None),"Desert tile at (4, 7) with a token of None")
            )
    },
    "Harbor": {
        "str": (
            (((4,10), {'kind': 'wood', 'quantity': 2}),"Harbor at (4, 10) trading 2 wood for 1"),
            (((3,5), {'kind': None, 'quantity': 3}),"Harbor at (3, 5) trading 3 anything for 1")
        ),
        "assert_raises": (
            ((3.5,5), {'kind': None, 'quantity': 3}),
            ({3,5}, {'kind': None, 'quantity': 3}),
            ((3,5,2), {'quantity': 3}),
            ((3,5), {'kind': None, 'quantity': 3}),
            ((3,5), {'kind': None, 'quantity': 3.5}),
            ((3,5), {'kind': None, 'quantity': 'foo'}),
            ((3,5), {'kind': None}),
            ((3,5), {'kind': 'foo', 'quantity': 3}),
            ((3,5), {'bar': 5, 'kind': None, 'quantity': 3}),
            ((3,5), {'foo': None, 'bar': 3})
        )
    },
    "tile_lists": {
        "overlapping": (
            ((2,1), 'wood', 4),
            ((4,1), 'ore', 10),
            ((1,2), 'wheat', 5),
            ((3,2), 'sheep', 2),
            ((5,2), 'brick', 8),
            ((2,3), 'desert', None),
            ((4,2), 'sheep', 12) # This is the problem
        ),
        "valid": (
            ((2,1), 'wood', 4),
            ((4,1), 'ore', 10),
            ((1,2), 'wheat', 5),
            ((3,2), 'sheep', 2),
            ((5,2), 'brick', 8),
            ((2,3), 'desert', None),
            ((4,3), 'sheep', 12) # This is the problem
        )
    },
    "harbor_list": (
        ((1,3), {'kind': None, 'quantity': 3}),
        ((2,3), {'kind': None, 'quantity': 3}),
        ((5,3), {'kind': 'sheep', 'quantity': 2}),
        ((5,2), {'kind': 'sheep', 'quantity': 2}),
        ((4,0), {'kind': 'brick', 'quantity': 2}),
        ((3,0), {'kind': 'brick', 'quantity': 2}),
        ((1,0), {'kind': 'None', 'quantity': 3}),
        ((1,1), {'kind': 'None', 'quantity': 3})
    )
}

with open('board_data.json', 'w') as f:
    json.dump(testing, f)
