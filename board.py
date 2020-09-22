import math

class BoardChecker:
    
    @staticmethod
    def value_handler(passed_value, valid_args):
        # Assert that the value is in a certain list of valid values
        assert isinstance(valid_args, tuple) or isinstance(valid_args, list), \
            'Argument <valid_args> must be of type tuple or list'
        assert (passed_value in valid_args), \
            f'{str(passed_value)} is not a valid argument'

    @staticmethod
    def is_coord(passed_value):
        # Assert that the value is a coordinate

        assert isinstance(passed_value, tuple), \
            f'{str(passed_value)} must be of type <tuple> or <list>'

        assert (len(passed_value) == 2), \
            f'{str(passed_value)} must be of length 2'

        assert all(isinstance(val, int) or isinstance(val, float) for val in passed_value), \
            f'{str(passed_value)} must only contain types <int> or <float>'

        assert all((val - math.floor(val) in (0, 0.5)) for val in passed_value), \
            f'{str(passed_value)} can only contain integers or integers + 0.5'

    @classmethod
    def is_edge_coord(cls, passed_value):
        cls.is_coord(passed_value)
        x = passed_value[0] - math.floor(passed_value[0])
        y = passed_value[1] - math.floor(passed_value[1])
        assert bool(x == 0.5) != bool(y == 0.5), \
            f'{str(passed_value)} is not an edge coordinate'
        assert x + y == 0.5, \
            f'{str(passed_value)} is not an edge coordinate'

    @classmethod
    def is_intersection_coord(cls, passed_value):
        cls.is_coord(passed_value)
        x = passed_value[0] - math.floor(passed_value[0])
        y = passed_value[1] - math.floor(passed_value[1])
        assert x == 0 and y == 0, \
            f'{str(passed_value)} is not an intersection coordinate'

class Tile:

    class LocalChecker:

        @staticmethod
        def valid_tile_kind(passed_value):
            # Asserts that Tile.kind is a valid string
            BoardChecker.value_handler(passed_value, ('desert', 'wood', 'ore', 'sheep', 'brick', 'wheat'))

        @staticmethod
        def valid_tile_token(passed_value):
            # Asserts that Title.token is a valid integer
            BoardChecker.value_handler(passed_value, (2, 3, 4, 5, 6, 8, 9, 10, 11, 12, None))

    def __init__(self, coords, kind, token):

        BoardChecker.is_intersection_coord(coords)
        self.LocalChecker.valid_tile_kind(kind)
        self.LocalChecker.valid_tile_token(token)

        if kind == 'desert':
            assert token == None, \
                'Desert\'s token must be None'
        else:
            assert token != None, \
                'All non-desert tiles must have non-None tokens'
        self.coords = coords
        self.kind = kind
        self.token = token
        
    def __str__(self):
        return f'{self.kind.capitalize()} tile at ({self.coords[0]}, ' \
        f'{self.coords[1]}) with a token of {str(self.token)}'
    
    def intersection_coords(self) -> tuple:
        x, y = self.coords[0], self.coords[1]
        return (self.coords, (x+1,y), (x+1,y-1), (x,y-1), (x-1,y-1), (x-1,y))

    def edge_coords(self) -> tuple:
            x, y = self.coords[0], self.coords[1]
            return ((x+0.5,y), (x+1,y-0.5), (x+0.5,y-1), (x-0.5,y-1), (x-1,y-0.5), (x-0.5, y))
    

    def intersections(self, intersection_dict) -> tuple:
        isinstance(intersection_dict, dict)

        intersection_list = []
        for coord in self.intersection_coords:
            intersection_list.append(intersection_dict[coord])
        return tuple(intersection_list)

    def edges(self, edge_dict) -> tuple:
        isinstance(edge_dict, dict)

        edge_list = []
        for coord in self.edge_coords:
            edge_list.append(edge_dict[coord])
        return tuple(edge_list)


class Structure:
    # Parent class for Settlement, City, Harbor and Road
    pass

class Settlement(Structure):
    def __init__(self, owner):
        self.owner = owner

class City(Structure):
    def __init__(self, owner):
        self.owner = owner

class Harbor(Structure):
    def __init__(self, coords, trade):
        
        assert isinstance(trade, dict), \
            'Argument <trade> must be of type: dict'
        assert len(trade) == 2, \
            'Argument <trade> must be of length 2'
        assert 'kind' in list(trade.keys()), \
            'Argument <trade> is missing key: \'kind\''
        assert 'quantity' in list(trade.keys()), \
            'Argument <trade> is missing key: \'quantity\''
        BoardChecker.value_handler(trade['kind'], ('sheep', 'wheat', 'brick', 'ore', 'wood', None))
        assert isinstance(trade['quantity'], int), \
            'trade[\'quantity\'] must be of type: int'

        BoardChecker.is_intersection_coord(coords)

        self.coords = coords
        self.trade = trade

    def __str__(self):
        choice = self.trade['kind'] if isinstance(self.trade['kind'], str) else 'anything'
        string = f"Harbor at ({self.coords[0]}, {self.coords[1]}) trading {str(self.trade['quantity'])} {choice} for 1"
        return string

class Road(Structure):
    def __init__(self, owner):
        self.owner = owner

class Intersection:
    def __init__(self, coords):

        BoardChecker.is_intersection_coord(coords)

        self.coords = coords
        self.surroundings = {'tiles': [], 'edges': [], 'intersections': []}
        self.building = None
        self.harbor = None
        self.occupant = None

    def __str__(self):
        return 'Intersection at ({self.coords[0]}, {self.coords[1]})'

    def build_harbor(self, harbor):
        assert isinstance(harbor, Harbor), \
            'Argument <harbor> must be an instance of Harbor'
        
        assert self.harbor == None, \
            'Cannot build two harbors on one intersection'

        self.harbor = harbor

    def build_building(self, building):
        assert isinstance(building, Settlement) or isinstance(building, City), \
            f'Argument <building> must be an instance of either Settlement or City'

        # Gets occupants of adjacent, non-empty intersections
        neighbors = [intersection.occupant for intersection in self.surroundings['intersections']]
        neighbors = list(filter(lambda x: x != None, neighbors))
        # If there are no adjacent occupants
        assert not neighbors, \
            'Cannot build a building adjacent to other buildings'
        assert building.owner in [edge.occupant for edge in self.surroundings['edges']], \
            'Cannot build a building that is not connected to a road'

        if self.occupant == None:
            assert isinstance(building, Settlement), \
                'Must build a Settlement here before you can build a City'
            self.building = building
            self.occupant = building.owner
        else:
            assert self.occupant == building.owner, \
                'Cannot build on somebody else\'s property'
            assert isinstance(building, City) and isinstance(self.building, Settlement)
            self.building = building


class Edge:
    def __init__(self, coords, intersection_plot):
        BoardChecker.is_edge_coord(coords)

        self.coords = coords
        self.road = None
        self.occupant = None

        x, y = coords[0], coords[1]
        possible_intersections = ((x+0.5, y), (x-0.5, y), (x, y+0.5), (x, y-0.5))
        intersections = []
        for coord in possible_intersections:
            try:
                intersections.append(intersection_plot[coord])
            except KeyError:
                pass
        
        self.intersections = intersections

    def __str__(self):
        if self.road != None:
            road = f' with a road owned by {self.road.owner.name}'
        else:
            road = ''

        string = f'Edge at ({self.coords[0]}, {self.coords[1]}) {road}' 
        return string

    def build_road(self, road):
        assert isinstance(road, Road), \
            'Argument <road> must be of the Road class'
        assert self.road == None, \
            'Cannot build a road on another road'

        neighbors = [intersection.occupant for intersection in self.intersections]
        neighbors = list(filter(lambda x: x != None, neighbors))

        # Either neighbors is empty or does not have the road owner
        if road.owner not in neighbors:
            for intersection in self.intersections:
                if intersection.occupant == None:
                    for edge in intersection.surroundings['edges']:
                        if edge.occupant == road.owner:
                            self.road = road
                            self.occupant = road.owner
            # If this loop ends without updating self.road and self.owner,
            # the placement is not possible and an AssertionError will be thrown
            assert self.occupant != None, \
                'Argument <road> must be directly connected to another ' \
                'Road or building who is owned by road.owner'

        # Argument <road> is directly connected to a building owned by road.owner
        else:
            self.road = road
            self.occupant = road.owner

class Board:

    class board_helpers:

        @staticmethod
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
                off_limit_coords.append((x+1,y))
                off_limit_coords.append((x-1,y))
                off_limit_coords.append((x,y-1))

            assert len(set(tile_coords)) == len(tile_coords), \
                'Argument <tile_list> has two tiles with the same coordinates'

            for coord in tile_coords:
                assert coord not in off_limit_coords, \
                    f'Tile at {coord} is overlapping with another tile'

        @staticmethod
        def make_feature_plot(tile_list):

            intersection_coord_set = set()
            edge_coord_set = set()
            for tile in tile_list:
                for coord in tile.intersection_coords():
                    intersection_coord_set.add(coord)
                for coord in tile.edge_coords():
                    edge_coord_set.add(coord)

            intersection_plot = {coord:Intersection(coord) for coord in intersection_coord_set}
            # Passing intersection_plot into edge creates the intersection list for that edge
            # upon instantiation
            edge_plot = {coord:Edge(coord, intersection_plot) for coord in edge_coord_set}
            return {'intersections': intersection_plot, 'edges': edge_plot}

        @staticmethod
        def give_intersections_tiles(tile_list, feature_plot):
            intersection_plot = feature_plot['intersections']
            for k,v in intersection_plot.items():
                for tile in tile_list:
                    if k in tile.intersection_coords():
                        v.surroundings['tiles'].append(tile)

        @staticmethod
        def give_intersections_intersections(feature_plot):
            intersection_plot = feature_plot['intersections']
            edge_plot = feature_plot['edges']
            for k,v in intersection_plot.items():
                x, y = k[0], k[1]
                pathways = {
                    (x+0.5,y):(x+1,y),
                    (x-0.5,y):(x-1,y),
                    (x,y+0.5):(x,y+1),
                    (x,y-0.5):(x,y-1)
                }
                for pathway, end in pathways.items():
                    if pathway in edge_plot.keys():
                        v.surroundings['intersections'].append(
                            intersection_plot[pathways[pathway]]
                        )


        @staticmethod
        def give_intersections_edges(feature_plot):
            edge_plot = feature_plot['edges']

            for edge in edge_plot.values():
                for intersection in edge.intersections:
                    intersection.surroundings['edges'].append(edge)

        @staticmethod
        def give_intersections_harbors(feature_plot, harbor_list):
            intersection_plot = feature_plot['intersections']
            for harbor in harbor_list:
                assert harbor.coords in list(intersection_plot.keys()), \
                    f'The coordinates for harbor at ({harbor.coords[0]}, {harbor.coords[1]})' \
                    ' are not on the board'
                intersection_plot[harbor.coords].build_harbor(harbor)


    class LocalChecker:

        @staticmethod
        def is_tile_list(passed_value):
            assert isinstance(passed_value, list) or isinstance(passed_value, tuple), \
                f'{passed_value} must be of types list or tuple'

            for tile in passed_value:
                assert isinstance(tile, Tile), \
                    f'{passed_value} contains an element which is not an instance of Tile'

        @staticmethod
        def is_harbor_list(passed_value):
            assert isinstance(passed_value, list) or isinstance(passed_value, tuple), \
                f'{passed_value} must be of types list or tuple'

            for harbor in passed_value:
                assert isinstance(harbor, Harbor), \
                    f'{passed_value} contains an element which is not an instance of Harbor'

        @staticmethod
        def is_intersection_plot(passed_value):
            assert isinstance(passed_value, dict), \
                f'{passed_value} must be of type dict'

            for k,v in passed_value:
                assert BoardChecker.is_intersection_coord(k), \
                    f'{k} is not a valid key for an intersection'
                assert isinstance(v, Intersection), \
                    f'Value with key {k} is not an instance of the Intersection class'

        @staticmethod
        def is_edge_plot(passed_value):
            assert isinstance(passed_value, dict), \
                f'{passed_value} must be of type dict'

            for k,v in passed_value:
                assert BoardChecker.is_edge_coord(k), \
                    f'{k} is not a valid key for an edge'
                assert isinstance(v, Edge), \
                    f'Value with key {k} is not an instance of the Edge class'

        @staticmethod
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

class Player:

    def __init__(self, board, name):

        assert isinstance(board, Board)
        assert isinstance(name, str)

        self.data = {
            'num_settlements': 5,
            'num_cities': 4,
            'num_roads': 15,
            'victory_points': 0,
            'largest_army': False,
            'longest_road': False
        }
        self.board = board
        self.name = name

    def road_coords(self) -> tuple:
        road_coords_set = set()
        for edge in self.board.edge_plot.values():
            if edge.occupant.name == self.name:
                road_coords_set.add(edge.coords)
        
