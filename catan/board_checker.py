from decorate_all_methods import decorate_all_methods
import math

@decorate_all_methods(staticmethod, exclude=['is_edge_coord', 'is_intersection_coord'])
class BoardChecker:
    
    def value_handler(passed_value, valid_args):
        # Assert that the value is in a certain list of valid values
        assert isinstance(valid_args, tuple) or isinstance(valid_args, list), \
            'Argument <valid_args> must be of type tuple or list'
        assert (passed_value in valid_args), \
            f'{str(passed_value)} is not a valid argument'

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
