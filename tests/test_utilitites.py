import unittest
import math

from src.utilities import rotate_clockwise_around_svg_origin, export_rotation, change_svg_to_dxf_coordinate, \
    calculate_euclidean_norm, calculate_scalar_product, calculate_angle_between_vectors_in_rad, export_translation, \
    export_scale, export_skew_x, export_skew_y, export_matrix



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
            self.assertEqual(export_rotation(normal_rotation), (42.699784, 0, 0))

            non_rotation = "translation(40)"
            self.assertEqual(export_rotation(non_rotation), None)

            no_transformation = None
            self.assertEqual(export_rotation(no_transformation), None)

            rotation_around_point = "rotate(30, 200, 200)"
            self.assertEqual(export_rotation(rotation_around_point), (30, 200, 200))


    def test_export_translation(self):
        transform = "translate(50,50)"
        self.assertEqual(export_translation(transform), (50, 50))

        transform = "translate(-50,0.5)"
        self.assertEqual(export_translation(transform), (-50, 0.5))

        transform_wrong = "translation(80,80)"
        self.assertEqual(export_translation(transform_wrong), None)

    def test_export_scale(self):
        scale = "scale(2, 0.5)"
        self.assertEqual(export_scale(scale), (2, 0.5))

        sx = 1/math.pi
        scale_only_x = f"scale({sx})"
        self.assertEqual(export_scale(scale_only_x), (sx, sx))

        no_scale = "rotation(10)"
        self.assertEqual(export_scale(no_scale), None)

    def test_export_skew(self):
        angle = 8.135
        skew_x = f"skewX({angle})"
        self.assertEqual(export_skew_x(skew_x), angle)

        no_skew = "translate(nothing)"
        self.assertEqual(export_skew_x(no_skew), None)

        skew_y = f"skewY({angle})"
        self.assertEqual(export_skew_y(skew_y), angle)

        self.assertEqual(export_skew_y(no_skew), None)

        to_much_info = "skewX(20,3)"
        self.assertEqual(export_skew_x(to_much_info), None)

        to_much_info = "skewY(20,3)"
        self.assertEqual(export_skew_y(to_much_info), None)


    def test_export_matrix(self):
        classic_mat = "matrix(2, 3, 0.5,   8, 0.12,2)"
        self.assertEqual(export_matrix(classic_mat), (2, 3, 0.5, 8, 0.12, 2))

        no_mat = "translate(50)"
        self.assertEqual(export_matrix(no_mat), None)

        few_info = "matrix(1, 1, 1, 1, 1)"
        self.assertEqual(export_rotation(few_info), None)

        to_much_info = "matrix(1, 1, 1, 1, 1, 1, 1, 1)"
        self.assertEqual(export_matrix(to_much_info), None)


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

        self.assertNotEqual(calculate_angle_between_vectors_in_rad(x, y, large_angle), 7/4 * math.pi)

        y = (-1, 0)
        self.assertEqual(calculate_angle_between_vectors_in_rad(x, y, False),
                         calculate_angle_between_vectors_in_rad(x, y, True))