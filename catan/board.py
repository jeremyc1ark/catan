from decorate_all_methods import decorate_all_methods

from .board_checker import BoardChecker
from .board_components import Edge, Harbor, Intersection, Tile


class Board:
    @decorate_all_methods(staticmethod)
    class board_helpers:
        def check_overlap(tile_list):
            assert isinstance(tile_list, list) or isinstance(tile_list, tuple), \
                'Argument <tile_list> must be of type list or tuple'
            off_limit_coords = []
            tile_coords = []
            for tile in tile_list:
                assert isinstance(tile, Tile), \
                    '<tile_list> contains one or more elements that are not of type Tile'
                tile_coords.append(tile.coords)

                x, y = tile.coords[0], tile.coords[1]
                off_limit_coords.append((x + 1, y))
                off_limit_coords.append((x - 1, y))
                off_limit_coords.append((x, y - 1))

            assert len(set(tile_coords)) == len(tile_coords), \
                'Argument <tile_list> has two tiles with the same coordinates'

            for coord in tile_coords:
                assert coord not in off_limit_coords, \
                    f'Tile at {coord} is overlapping with another tile'

        def make_feature_plot(tile_list):

            intersection_coord_set = set()
            edge_coord_set = set()
            for tile in tile_list:
                for coord in tile.intersection_coords():
                    intersection_coord_set.add(coord)
                for coord in tile.edge_coords():
                    edge_coord_set.add(coord)

            intersection_plot = {
                coord: Intersection(coord)
                for coord in intersection_coord_set
            }
            # Passing intersection_plot into edge creates the intersection list for that edge
            # upon instantiation
            edge_plot = {
                coord: Edge(coord, intersection_plot)
                for coord in edge_coord_set
            }
            return {'intersections': intersection_plot, 'edges': edge_plot}

        def give_intersections_tiles(tile_list, feature_plot):
            intersection_plot = feature_plot['intersections']
            for k, v in intersection_plot.items():
                for tile in tile_list:
                    if k in tile.intersection_coords():
                        v.surroundings['tiles'].append(tile)

        def give_intersections_intersections(feature_plot):
            intersection_plot = feature_plot['intersections']
            edge_plot = feature_plot['edges']
            for k, v in intersection_plot.items():
                x, y = k[0], k[1]
                pathways = {
                    (x + 0.5, y): (x + 1, y),
                    (x - 0.5, y): (x - 1, y),
                    (x, y + 0.5): (x, y + 1),
                    (x, y - 0.5): (x, y - 1)
                }
                for pathway, end in pathways.items():
                    if pathway in edge_plot.keys():
                        v.surroundings['intersections'].append(
                            intersection_plot[pathways[pathway]])

        def give_intersections_edges(feature_plot):
            edge_plot = feature_plot['edges']

            for edge in edge_plot.values():
                for intersection in edge.intersections:
                    intersection.surroundings['edges'].append(edge)

        def give_intersections_harbors(feature_plot, harbor_list):
            intersection_plot = feature_plot['intersections']
            for harbor in harbor_list:
                assert harbor.coords in list(intersection_plot.keys()), \
                    f'The coordinates for harbor at ({harbor.coords[0]}, {harbor.coords[1]})' \
                    ' are not on the board'
                intersection_plot[harbor.coords].build_harbor(harbor)

    @decorate_all_methods(staticmethod)
    class LocalChecker:
        def is_tile_list(passed_value):
            assert isinstance(passed_value, list) or isinstance(passed_value, tuple), \
                f'{passed_value} must be of types list or tuple'

            for tile in passed_value:
                assert isinstance(tile, Tile), \
                    f'{passed_value} contains an element which is not an instance of Tile'

        def is_harbor_list(passed_value):
            assert isinstance(passed_value, list) or isinstance(passed_value, tuple), \
                f'{passed_value} must be of types list or tuple'

            for harbor in passed_value:
                assert isinstance(harbor, Harbor), \
                    f'{passed_value} contains an element which is not an instance of Harbor'

        def is_intersection_plot(passed_value):
            assert isinstance(passed_value, dict), \
                f'{passed_value} must be of type dict'

            for k, v in passed_value:
                assert BoardChecker.is_intersection_coord(k), \
                    f'{k} is not a valid key for an intersection'
                assert isinstance(v, Intersection), \
                    f'Value with key {k} is not an instance of the Intersection class'

        def is_edge_plot(passed_value):
            assert isinstance(passed_value, dict), \
                f'{passed_value} must be of type dict'

            for k, v in passed_value:
                assert BoardChecker.is_edge_coord(k), \
                    f'{k} is not a valid key for an edge'
                assert isinstance(v, Edge), \
                    f'Value with key {k} is not an instance of the Edge class'

        def is_feature_plot(passed_value):
            assert isinstance(passed_value, dict), \
                f'{passed_value} must be of type dict'

            assert len(passed_value) == 2, \
                f'{passed_value} must be of length 2'

            dict_keys = list(passed_value.keys())

            assert 'intersections' in dict_keys, \
                '<feature_plot> is missing key: \'intersections\''
            assert 'edges' in dict_keys, \
                '<feature_plot> is missing key \'edges\''

            self.is_intersection_plot(passed_value['intersections'])
            self.is_edge_plot(passed_value['edges'])

    def __init__(self, tile_list, harbor_list):

        self.LocalChecker.is_harbor_list(harbor_list)
        self.LocalChecker.is_tile_list(tile_list)

        self.board_helpers.check_overlap(tile_list)
        feature_plot = self.board_helpers.make_feature_plot(tile_list)
        self.board_helpers.give_intersections_tiles(tile_list, feature_plot)
        self.board_helpers.give_intersections_intersections(feature_plot)
        self.board_helpers.give_intersections_edges(feature_plot)

        self.feature_plot = feature_plot
        self.intersection_plot = feature_plot['intersections']
        self.edge_plot = feature_plot['edges']
        self.tile_list = tile_list
        self.harbor_list = harbor_list
