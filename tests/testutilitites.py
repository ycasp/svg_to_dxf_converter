import unittest
from src.utilities import rotate_clockwise_around_svg_origin, export_rotation, change_svg_to_dxf_coordinate, \
    calculate_euclidean_norm, calculate_scalar_product, calculate_angle_between_vectors_in_rad
import math
from unittest.mock import Mock

class TestUtilities(unittest.TestCase):

    def test_clockwise_rotation_around_svg_origin(self):
        x = 1
        y = 0
        height = 0

        # rotation around origin (height = 0), clockwise
        rot_angle = 90
        self.assertEqual(rotate_clockwise_around_svg_origin(x, y, rot_angle, height), (0, -1))

        # rotation around origin (height = 0), counterclockwise
        rot_angle = -90
        self.assertEqual(rotate_clockwise_around_svg_origin(x, y, rot_angle, height), (0, 1))

        # no rotation
        rot_angle = 0
        self.assertEqual(rotate_clockwise_around_svg_origin(x, y, rot_angle, height), (1, 0))

        # "decimal rotation" (test rounding)
        x = 0.3
        y = 0.25
        rot_angle = 22
        self.assertEqual(rotate_clockwise_around_svg_origin(x, y, rot_angle, height), (0.37181, 0.11941))

    def test_export_rotation(self):
            normal_rotation = "rotate(42.699784)"
            self.assertEqual(export_rotation(normal_rotation), 42.699784)

            non_rotation = "translation(40)"
            self.assertEqual(export_rotation(non_rotation), 0)

    def test_euclidean_norm(self):
        x = (3, 4)
        self.assertEqual(calculate_euclidean_norm(x), 5)

        x = (-3, 4)
        self.assertEqual(calculate_euclidean_norm(x), 5)

        x = (3, -4)
        self.assertEqual(calculate_euclidean_norm(x), 5)

        x = (-3, -4)
        self.assertEqual(calculate_euclidean_norm(x), 5)

        x = (0, 0)
        self.assertEqual(calculate_euclidean_norm(x), 0)

    def test_scalar_product(self):
        x = (1, 0); y = (0, 1)
        self.assertEqual(calculate_scalar_product(x, y), 0)

        x = (2, 8); y = (-3, 4)
        self.assertEqual(calculate_scalar_product(x, y), 26)

        x = (-2, 8); y = (-3, 4)
        self.assertEqual(calculate_scalar_product(x, y), 38)

        x = (-2, -8); y = (-3, 4)
        self.assertEqual(calculate_scalar_product(x, y), -26)

        x = (-2, -8); y = (-3, -4)
        self.assertEqual(calculate_scalar_product(x, y), 38)

        x = (2, -8); y = (-3, 4)
        self.assertEqual(calculate_scalar_product(x, y), -38)

        x = (0, 0); y = (0, 0)
        self.assertEqual(calculate_scalar_product(x, y), 0)

    def test_angle_calculation(self):
        x = (1, 0)

        y = (math.sqrt(2) / 2, math.sqrt(2) / 2)
        large_angle = False

        self.assertEqual(calculate_angle_between_vectors_in_rad(x, y, large_angle), 1/4 * math.pi)

        large_angle = True

        self.assertEqual(calculate_angle_between_vectors_in_rad(x, y, large_angle), 7/4 * math.pi)

        y = (-1, 0)
        self.assertEqual(calculate_angle_between_vectors_in_rad(x, y, False),
                         calculate_angle_between_vectors_in_rad(x, y, True))