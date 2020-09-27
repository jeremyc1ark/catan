from .context.catan.core.player import Player, Road

def test_longest_road(starter_board_data):
    local_player = Player(starter_board_data, 'Jeff')
    # Not using the build_road or build_building methods
    # to reduce dependency on other functions

    road_list = (
        (0, 2.5),
        (0.5, 3),
        (1, 3.5),
        (1.5, 4),
        (2.5, 4),
        (3, 3.5),
        (3.5, 3),
        (4, 2.5),
        (3.5, 4),
        (4.5, 4),
        (5.5, 1),
        (6.5, 1),
        (9, 3.5)
    )

    for elem in road_list:
        edge = local_player.board.edge_plot[elem]
        assert edge.isbuildable(Road(local_player))
        edge.road = Road(local_player)
        edge.occupant = local_player

    assert local_player.longest_road() == 8, \
        f'local_player.longest_road should return 8 but returns {local_player.longest_road()} instead'
