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

    # Helper recursion function
    def _exhaust_pathways(
            current_intersection,
            visited=[],
            prev_matches = set()
    ):
        """
        Helper recursion function for longest_road_path. Global in class
        to make it testable. Given a starting coordinate, _exhaust_pathways
        will iterate through all of the roads that are connected to it. It
        does this by finding the edges that are connected to it and determining
        whether a road which this player owns is on that edge. If it is, then
        the algorithm will find the intersection that the road leads to. If the
        intersection is not in the set of intersection that the last iteration
        visited, and the intersection has not been visited before, the it will
        add this intersection to its list of matches. If the algorithm finds
        no matches, this means that it has reached the end of a road.
        Algorithm does not need an intersection_plot because the plot
        can be reconstructed with just one intersection. Every intersection
        stores its surroundings, which store their surroundings, which
        store their surroundings, etc. However, the algorithm does not
        need to reconstruct the entire board. At any given time, it only
        needs information about its past iterations and the current
        intersection. Therefore, it can be called with just a single
        intersection at the beginning, since it has no stack.
        If current_intersection has a structure on it that is not
        owned by the player, then _exhaust_pathways will terminate.
        """

        local_visited = copy.copy(visited)
        local_visited.append(current_intersection)

        if current_intersection.owner is not self:
            yield local_visited

        matches = set()

        for edge in current_intersection.surroundings['edges']:
            if edge.occupant is self:
                connecting_intersection = None
                for intersection in edge.intersections:
                    if intersection is not current_intersection:
                        connecting_intersection = intersection
                if connecting_intersection not in visited:
                    if connecting_intersection not in prev_matches:
                        matches.add(connecting_intersection)

        if not matches:
            yield local_visited
        else:
            for match in matches:
                _exhaust_pathways(match, local_visited, matches)

    def all_paths(self) -> list:
        """
        Returns a list of all of the ordered lists
        that _exhaust_pathways would return for every
        intersection with only one road connected to
        it. Starting a cycle of recursion with two or
        more roads attached to an intersection would
        be redundant. It would not find the length
        of a road from beginning to end, but from
        the center to one end instead.
        """
        # Collection of the coordinates intersections
        # which have one or more of this player's roads connected to them
        intersection_set = set()
        for intersection in self.board.intersection_plot.values():
            for edge in intersection.surroundings['edges']:
                if edge.occupant is self:
                    intersection_set.add(intersection)

        all_paths = []
        for intersection in instersection_set:
            for item in list(self._exhaust_pathways(intersection)):
                all_paths.append(item)

        return all_paths

    def longest_road_path(self):
        all_paths = self.all_paths()
        for path in all_paths:
            visited_intersections = set()
            visited_roads = set()
            for intersection in path:
                  


    def longest_road_len(self) -> int:
        """
        If the road is a loop, the length will be the
        length of the intersection list returned by
        self.longest_road_path(). If the length of
        the pathway is 2, then the the length will
        be one. If it has a distict end and beginning
        and has a length greater than 2, it will return
        one less than the length of the intersection list
        returned by self.longest_road_path().
        """

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

