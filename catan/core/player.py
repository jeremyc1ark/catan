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

    def longest_road(self) -> tuple:
        road_coord_set = set()
        for edge in self.board.edge_plot.values():
            if edge.occupant == self:
                road_coord_set.add(edge.coords)

        road_lengths = set()
        def exhaust_pathways(current_coord, coord_set, counter=1):
            x, y = current_coord[0], current_coord[1]
            possible_coords = (
                (x+0.5,y+0.5),
                (x+0.5,y-0.5),
                (x-0.5,y+0.5),
                (x-0.5,y-0.5),
                (x+1,y),
                (x-1,y)
            )
            matching_coords = set()
            for coord in possible_coords:
                if coord in coord_set:
                    matching_coords.add(coord)

            if not matching_coords:
                road_lengths.add(counter)
            else:
                coord_set.remove(current_coord)
                for coord in matching_coords:
                    exhaust_pathways(coord, coord_set, counter+1)

        for coord in road_coord_set:
            local_coord_set = road_coord_set
            local_coord_set.remove(coord)
            exhaust_pathways(coord, local_coord_set)

        return max(road_lengths)
