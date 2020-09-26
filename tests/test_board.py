import pytest
from .context.catan.core.board import Board
from decorate_all_methods import decorate_all_methods

stage_testing = {
    "make_feature_plot": None,
    "give_intersections_tiles": None,
    "give_intersections_intersections": None,
    "give_intersections_edges": None,
    "give_intersections_harbors": None
}

stage_testing['make_feature_plot'] = Board.board_helpers.make_feature_plot(
    (
        Tile((2,1), 'sheep', 6),
        Tile((4,1), 'ore', 11),
        Tile((1,2), 'desert', None),
        Tile((3,2), 'wood', 5),
        Tile((5,2), 'brick', 2),
        Tile((2,3), 'wheat', 4),
        Tile((4,3), 'ore', 9)
    )
)

stage_testing['give_intersections_tiles'] = Board.board_helpers.give_intersections_tiles(
    valid_tile_list, stage_testing['make_feature_plot']
)

stage_testing['give_intersections_intersections'] = Board.board_helpers.give_intersections_intersections(
    stage_testing['give_intersections_tiles']
)

stage_testing['give_intersections_edges'] = Board.board_helpers.give_intersections_edges(
    stage_testing['give_intersections_intersections']
)

stage_testing['give_intersections_harbors'] = Board.board_helpers.give_intersections_harbors(
    stage_testing['give_intersections_edges'], 
    (
        Harbor((1,3), {'kind': 'ore', 'quantity': 2}),
        Harbor((2,3), {'kind': 'ore', 'quantity': 2}),
        Harbor((5,3), {'kind': 'wheat', 'quantity': 2}),
        Harbor((5,2), {'kind': 'wheat', 'quantity': 2}),
        Harbor((0,2), {'kind': None, 'quantity': 3}),
        Harbor((0,1), {'kind': None, 'quantity': 3})
    )
)


def test_check_overlap():
    overlap_tile_list = (
        Tile((2,1), 'sheep', 6),
        Tile((4,1), 'ore', 11),
        Tile((1,2), 'desert', None),
        Tile((3,2), 'wood', 5),
        Tile((5,2), 'brick', 2),
        Tile((2,3), 'wheat', 4),
        Tile((4,2), 'ore', 9) # This overlaps
    )

    with pytest.raises(AssertionError):
        Board.board_helpers.check_overlap(overlap_tile_list)
    Board.board_helpers.check_overlap(valid_tile_list)


def test_make_feature_plot(intersection_coords_for_tile_list, edge_coords_for_tile_list):
    feature_plot = stage_testing('make_feature_plot')
    edge_plot = feature_plot['edges']
    intersection_plot = feature_plot['intersections']
    intersection_coords_for_tile_list = ((5,3), (4,3), (3,3), (2,3), (1,3), (6,2),
        (5,2), (4,2), (3,2), (2,2), (1,2), (0,2), (6,1), (5,1), (4,1), (3,1), (2,1),
        (1,1), (0,1), (5,0), (4,0), (3,0), (2,0), (1,0))
    edge_coords_for_tile_list = ((1.5,0), (2.5,0), (3.5,0), (4.5,0), (0.5,1), (1.5,1),
        (2.5,1), (3.5,1), (4.5,1), (5.5,1), (0.5,2), (1.5,2), (2.5,2), (3.5,2), (4.5,2),
        (5.5,2), (1.5,3), (2.5,3), (3.5,3), (4.5,3), (1,0.5), (3,0.5), (5,0.5), (0,1.5),
        (2,1.5), (4,1.5), (6,1.5), (1,2.5), (3,2.5), (5,2.5))
    assert len(edge_plot) == 30
    assert len(intersection_plot) == 24

    for intersection_coord in intersection_plot.keys():
        assert intersection_coord in intersection_coords_for_tile_list

    for edge_coord in edge_plot.keys():
        assert edge_coord in edge_coords_for_tile_list

    assert len(edge_plot[(4,1.5)].intersections) == 2
    assert intersection_plot[(4,2)] in edge_plot[(4,1.5)].intersections
    assert intersection_plot[(4,1)] in edge_plot[(4,1.5)].intersections

def test_give_intersections_tiles():
    intersection_plot = stage_testing('give_intersections_tiles')['intersections']
    test_dict = {
        (5,3):[((4,3), 'ore', 9)],
        (2,1):[((2,1), 'sheep', 6), ((3,2), 'wood', 5), ((1,2), 'desert', None)],
        (3,3):[((2,3), 'wheat', 4), ((4,3), 'ore', 9)]
    }
    for k,v in test_dict.items():
        surrounding_tiles = intersection_plot[k].surroundings['tiles']
        assert len(surrounding_tiles) == len(v)
        for tile in surrounding_tiles:
            assert (tile.coords, tile.kind, tile.token) in v

def test_give_intersections_intersections():
    intersection_plot = stage_testing('give_intersections_intersections')['intersections']
    test_dict = {
        (5,3):[(5,2), (4,3)],
        (4,1):[(3,1), (5,1), (4,2)],
        (3,0):[(2,0), (4,0), (3,1)],
        (1,2):[(0,2),(2,2),(1,3)]
    }
    for k,v in test_dict.items():
        surrounding_intersections = intersection_plot[k].surroundings['intersections']
        assert len(surrounding_intersections) == len(v)
        for intersection in surrounding_intersections:
            assert intersection.coords in v

def test_give_intersections_edges():
    intersection_plot = stage_testing('give_intersections_edges')['intersections']
    test_dict = {
        (6,1):[(6,1.5),(5.5,1)],
        (3,1):[(2.5,1),(3.5,1),(3,0.5)],
        (3,2):[(2.5,2),(3.5,2),(3,2.5)]
    }
    for k,v in test_dict.items():
        surrounding_edges = intersection_plot[k].surroundings['edges']
        assert len(surrounding_edges) == len(v)
        for edge in surrounding_edges:
            assert edge.coords in v

def test_give_intersections_harbors():
    intersection_plot = stage_testing('give_intersections_harbors')['intersections']
    real_harbor_list = [(harbor.coords, harbor.trade) for harbor in valid_harbor_list]
    observed_harbor_list = [(intersection.harbor.coords, intersection.harbor.trade)
                            for intersection in intersection_plot.values()
                            if intersection.harbor != None]
    assert len(real_harbor_list) == len(observed_harbor_list)
    for elem in real_harbor_list:
        assert elem in observed_harbor_list

def test_edge_surroundings():
    edge_plot = stage_testing('make_feature_plot')['edges']
    test_dict = {
        (3,0.5):[(3,0),(3,1)],
        (3.5,2):[(3,2),(4,2)],
        (6,1.5):[(6,1),(6,2)],
        (0.5,2):[(0,2),(1,2)]
    }
    for k,v in test_dict.items():
        surrounding_intersections = edge_plot[k].intersections
        assert len(surrounding_intersections) == 2
        for intersection in surrounding_intersections:
            assert intersection.coords in v

def test_build_building():
    test_board = Board(valid_tile_list, valid_harbor_list)
    intersection_plot = test_board.intersection_plot
    edge_plot = test_board.edge_plot
    
    def assertion_helper(owner, coords, kind):
        if kind == Settlement or kind == City:
            intersection_plot[coords].build_building(kind(owner))
            assert intersection_plot[coords].occupant == owner
            assert isinstance(intersection_plot[coords].building, kind)
            
        elif kind == Road:
            edge_plot[coords].build_road(kind(owner))
            assert edge_plot[coords].occupant == owner
            assert isinstance(edge_plot[coords].road, Road)

    intersection_plot[(4,2)].building = Settlement('sam')
    intersection_plot[(4,2)].occupant = 'sam'
    assert intersection_plot[(4,2)].occupant == 'sam'
    assert isinstance(intersection_plot[(4,2)].building, Settlement)

    intersection_plot[(1,1)].building = Settlement('bob')
    intersection_plot[(1,1)].occupant = 'bob'
    assert intersection_plot[(1,1)].occupant == 'bob'
    assert isinstance(intersection_plot[(1,1)].building, Settlement)
    
    placements = (
        ('sam', (4,1.5), Road),
        ('sam', (3.5,1), Road),
        ('sam', (4.5,1), Road),
        ('sam', (3,1), Settlement),
        ('sam', (2.5,1), Road),
        ('sam', (1.5,1), Road),
        ('bob', (1,0.5), Road),
        ('bob', (1.5,0), Road),
        ('bob', (2,0), Settlement),
        ('sam', (3,1), City)
    )
    for elem in placements:
        print(elem[1])
        assertion_helper(elem[0], elem[1], elem[2])

    def assertion_raiser(owner, coords, kind):
        with pytest.raises(AssertionError):
            if kind == Settlement or kind == City:
                intersection_plot[coords].build_building(kind(owner))
            elif kind == Road:
                edge_plot[coords].build_road(kind(owner))

    illegal_placements = (
        ('sam', (2,1), Settlement),
        ('sam', (5,1), City),
        ('sam', (0.5,1), Road),
        ('sam', (4.5,3), Road),
        ('sam', (2,3), Settlement),
        ('bob', (5,1), Settlement)
    )

    for elem in illegal_placements:
        assertion_raiser(elem[0], elem[1], elem[2])

