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

    def longest_road_path(self) -> list:
        all_paths = []

        # Helper recursion function
        def exhaust_pathways(current_coord, coord_set, visited=[], prev_matches=set()):
            local_visited = copy.copy(visited)
            local_visited.append(current_coord)

            x, y = current_coord[0], current_coord[1]
            possible_matches = {(x+1,y), (x-1,y), (x,y+1), (x,y-1)}

            matches = set()
            for elem in possible_matches:
                if elem in coord_set:
                    if elem not in local_visited:
                        if elem not in prev_matches:
                            matches.add(elem)

            if not matches:
                all_paths.append(local_visited)
            else:
                for match in matches:
                    exhaust_pathways(match, coord_set, local_visited, matches)

        # Collection of the coordinates intersections
        # which have one or more of this player's roads connected to them
        intersection_coord_set = set()
        for intersection in self.board.intersection_plot.values():
            for edge in intersection.surroundings['edges']:
                if edge.occupant is self:
                    intersection_coord_set.add(intersection.coords)


        for coord in intersection_coord_set:
            exhaust_pathways(coord, intersection_coord_set)

        # Makes a dict where keys are the lengths of their
        # corresponding paths
        path_lens = {len(path):path for path in all_paths}

        # Returns the path with the highest length
        return path_lens[max(path_lens.keys())]

    def longest_road_len(self) -> int:
        # If the road is a loop, the length will be the
        # length of the intersection list returned by
        # self.longest_road_path(). If the length of
        # the pathway is 2, then the the length will
        # be one. If it has a distict end and beginning
        # and has a length greater than 2, it will return
        # one less than the length of the intersection list
        # returned by self.longest_road_path().

        pathway = self.longest_road_path()

        # These are the surrounding intersection coordinates
        # for the final coordinate in the pathway
        end_intersections = [intersection.coords for intersection in
        self.board.intersection_plot[pathway[-1]].surroundings['intersections']]

        if len(pathway) == 2:
            return 1
        elif pathway[0] in end_intersections:
            return len(pathway)
        else:
            return len(pathway) - 1

