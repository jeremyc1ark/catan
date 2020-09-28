import copy

class Player:

    def __init__(self, board, name):

        assert board.__class__.__name__ == 'Board'
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
            if edge.occupant is self:
                road_coord_set.add(edge.coords)

        road_lengths = set()

        def exhaust_pathways(current_coord, coord_set, counter=1, visited=set(), prev_matching_coords=set()):
            # Creating a local set so as to not mutate the global set
            local_visited = copy.copy(visited)

            local_visited.add(current_coord)

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
                    if coord not in local_visited:
                        if coord not in prev_matching_coords:
                            matching_coords.add(coord)

            if not matching_coords:
                road_lengths.add(counter)
            else:
                for coord in matching_coords:
                    exhaust_pathways(coord, coord_set, counter+1, local_visited, matching_coords)

        for coord in road_coord_set:
            exhaust_pathways(coord, road_coord_set)

        return max(road_lengths)
