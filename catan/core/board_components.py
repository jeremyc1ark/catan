from decorate_all_methods import decorate_all_methods
from board_checker import BoardChecker

class Tile:

    @decorate_all_methods(staticmethod)
    class LocalChecker:

        def valid_tile_kind(passed_value):
            # Asserts that Tile.kind is a valid string
            BoardChecker.value_handler(passed_value, ('desert', 'wood', 'ore', 'sheep', 'brick', 'wheat'))

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

    def road_is_buildable(self, road):
        if not isinstance(self, Road):
            return False
        if self.road != None:
            return False
        
        neighbors = [intersection.occupant for intersection in self.intersections]
        neighbors = list(filter(lambda x: x != None, neighbors))

        # Either neighbors is empty or does not have the road owner
        if road.owner not in neighbors:
            for intersection in self.intersections:
                if intersection.occupant == None:
                    for edge in intersection.surroundings['edges']:
                        if edge.occupant == road.owner:
                            return True
            # If this loop ends without updating self.road and self.owner,
            # the placement is not possible and an AssertionError will be thrown
            if self.occupant == None:
                return False
        # Argument <road> is directly connected to a building owned by road.owner
        else:
            self.road = road
            self.occupant = road.owner

    
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
