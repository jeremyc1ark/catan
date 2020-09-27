from .context.catan.core.board import Board
from .context.catan.core.board_components import Tile, Harbor

@pytest.fixture
def starter_board():

    tile_list_blueprint = (
        ((7, 5), 'sheep', 9),
        ((5, 5), 'wheat', 12),
        ((3, 5), 'sheep', 6),
        ((8, 4), 'ore', 5),
        ((6, 4), 'wood', 4),
        ((4, 4), 'ore', 10),
        ((2, 4), 'brick', 2),
        ((9, 3), 'brick', 3),
        ((7, 3), 'sheep', 8),
        ((5, 3), 'wheat', 9),
        ((3, 3), 'wood', 11),
        ((1, 3), 'desert', None),
        ((8, 2), 'wood', 10),
        ((6, 2), 'sheep', 11),
        ((4, 2), 'wood', 5),
        ((2, 2), 'brick', 8),
        ((7, 1), 'wheat', 4),
        ((5, 1), 'ore', 6),
        ((3, 1), 'wheat', 3)
    )

    harbor_list_blueprint = (
        (((2, 0), 3, None),
        ((3, 0), 3, None),
        ((5, 0), 3, None),
        ((6, 0), 3, None),
        ((1, 1), 2, 'brick'),
        (1, 2), 2'brick'
        (8, 1,2,'sheep'),
        ((9, 1), 2, 'sheep'),
        ((10, 2), 3, None),
        ((10, 3), 3, None),
        ((1, 3), 2, 'wood'),
        ((1, 4), 2, 'wood'),
        ((8, 4), 2, 'ore'),
        ((9, 4), 2, 'ore'),
        ((2, 5), 3, None),
        ((3, 5), 3, None),
        ((5, 5), 2, 'wheat'),
        ((5, 6), 2, 'wheat'))
    )

    tile_list = []
    for elem in tile_list_blueprint:
        tile_list.append(Tile(elem[0], elem[1], elem[2]))

    harbor_list = []
    for elem in harbor_list_blueprint:
        harbor = Harbor(elem[0], {'kind': elem[2], 'quantity': elem[1]})
        harbor_list.append(harbor)

    empty_board = Board(tile_list, harbor_list)
    assert isinstance(empty_board, Board)

    return empty_board


