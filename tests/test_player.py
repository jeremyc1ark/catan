# from .context.catan.core.player import Player, Road
from .context import catan
from catan.board_components import Road
from catan.player import Player

import pytest

@pytest.mark.parametrize(
    "road_list,max_len",
    [
        (
            [(0, 2.5), (0.5, 3), (1, 3.5), (1.5, 4),
            (2.5, 4), (3, 3.5), (3.5, 3), (4, 2.5),
            (3.5, 4), (4.5, 4), (5.5, 1), (6.5, 1),
            (9, 3.5)],
            8
        ),
        (
            [(0,2.5)],
            1
        ),
        (
            [(3,3.5), (3.5,3), (4.5,3), (5,3.5),
             (3.5,4), (4.5,4)],
            6
        ),
        (
            [(3.5,2), (3.5,3), (3.5,4), (3.5,5),
             (2.5,2), (2.5,3), (2.5,4), (2.5,5),
             (2,4.5), (2,2.5), (4,4.5), (4,2.5),
             (3,3.5), (3,1.5), (2.5,1)],
            14
        )
    ]
)
def test_longest_road(starter_board_data, road_list, max_len):
    local_player = Player(starter_board_data, 'Jeff')
    # Not using the build_road or build_building methods
    # to reduce dependency on other functions

    for elem in road_list:
        edge = local_player.board.edge_plot[elem]
        edge.road = Road(local_player)
        edge.occupant = local_player
    assert local_player.longest_road_len() == max_len, \
        f'local_player.longest_road should return {max_len} but returns {local_player.longest_road_len()} instead'
