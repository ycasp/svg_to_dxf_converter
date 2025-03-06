import unittest

from src.svg_shapes.transform_messages import export_transformations


class TestTransformMessages(unittest.TestCase):

    def test_export_transformations(self):
        transform = None
        self.assertEqual(export_transformations(transform), None)

        translation = "translate(30,40)"
        transform_list = export_transformations(translation)
        self.assertEqual(transform_list[0], ('translate', [30, 40]))
        self.assertEqual(len(transform_list), 1)

        rotation = "rotate(45,50,50)"
        transform_list = export_transformations(rotation)
        self.assertEqual(transform_list[0], ('rotate', [45, 50, 50]))
        self.assertEqual(len(transform_list), 1)

        rotation_around_origin = "rotate(45)"
        transform_list = export_transformations(rotation_around_origin)
        self.assertEqual(transform_list[0], ('rotate', [45]))
        self.assertEqual(len(transform_list), 1)

        scaling = "scale(1.5,3.1415962)"
        transform_list = export_transformations(scaling)
        self.assertEqual(transform_list[0], ('scale', [1.5, 3.1415962]))
        self.assertEqual(len(transform_list), 1)

        multiple_transform = "translate(20,30) rotate(30,30,30) scale(2,2)"
        transform_list = export_transformations(multiple_transform)
        self.assertEqual(len(transform_list), 3)
        self.assertEqual(transform_list[0], ('translate', [20, 30]))
        self.assertEqual(transform_list[1], ('rotate', [30, 30, 30]))
        self.assertEqual(transform_list[2], ('scale', [2, 2]))

        skew_transform = "skewX(25) skewY(15)"
        transform_list = export_transformations(skew_transform)
        self.assertEqual(len(transform_list), 2)
        self.assertEqual(transform_list[0], ('skewX', [25]))
        self.assertEqual(transform_list[1], ('skewY', [15]))

        matrix_transform="matrix(1, 0.5, -0.5, 1, 20, 40)"
        transform_list = export_transformations(matrix_transform)
        self.assertEqual(len(transform_list), 1)
        self.assertEqual(transform_list[0], ('matrix', [1, 0.5, -0.5, 1, 20, 40]))

        crazy_transform="translate(10,20) rotate(90,30,30) scale(1.2,0.8) skewX(10) skewY(5) matrix(1, 0, 0, 1, 5, 5)"
        transform_list = export_transformations(crazy_transform)
        self.assertEqual(len(transform_list), 6)
