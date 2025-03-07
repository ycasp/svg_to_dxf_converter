import unittest

from src.svg_shapes.svgRectangle import *

class TestSvgRectangle(unittest.TestCase):

    def setUp(self):
        self.height = 200
        self.normal_rect_element = {'x': 50, 'y': 100, 'width': 100, 'height': 50}
        self.normal_rect = SvgRectangle(self.normal_rect_element, self.height)

    def test_initialization(self):
        self.assertEqual(self.normal_rect.x, 50)
        self.assertEqual(self.normal_rect.y, 100)
        self.assertEqual(self.normal_rect.rect_width, (100, 0))
        self.assertEqual(self.normal_rect.rect_height, (0, -50))
        self.assertEqual(self.normal_rect.rx, (0, 0))
        self.assertEqual(self.normal_rect.ry, (0, 0))

        self.normal_rect_element['rx'] = 50
        self.normal_rect = SvgRectangle(self.normal_rect_element, self.height)
        self.assertEqual(self.normal_rect.rx, (50, 0))
        self.assertEqual(self.normal_rect.ry, (0,25))

        self.normal_rect_element['ry'] = 15
        self.normal_rect = SvgRectangle(self.normal_rect_element, self.height)
        self.assertEqual(self.normal_rect.rx, (50, 0))
        self.assertEqual(self.normal_rect.ry, (0, 15))

        self.normal_rect_element['rx'] = None
        self.normal_rect = SvgRectangle(self.normal_rect_element, self.height)
        self.assertEqual(self.normal_rect.rx, (15, 0))
        self.assertEqual(self.normal_rect.ry, (0, 15))

    def test_ensure_applicable_radius(self):
        width = 100
        applicable_r = 49
        self.assertEqual(ensure_applicable_radius(applicable_r, width), applicable_r)

        non_applicable_r = 75
        self.assertEqual(ensure_applicable_radius(non_applicable_r, width), width / 2)

    def test_get_name(self):
        self.assertEqual(self.normal_rect.get_name(), 'rectangle')

    def test_scale(self):
        self.normal_rect_element['rx'] = 25
        self.normal_rect_element['ry'] = 15
        self.normal_rect= SvgRectangle(self.normal_rect_element, self.height)

        scale = 2
        self.normal_rect.scale(scale, scale)

        self.assertEqual(self.normal_rect.x, 100)
        self.assertEqual(self.normal_rect.y, 200)
        self.assertEqual(self.normal_rect.rect_width, (200, 0))
        self.assertEqual(self.normal_rect.rect_height, (0, -100))
        self.assertEqual(self.normal_rect.rx, (50, 0))
        self.assertEqual(self.normal_rect.ry, (0, 30))

        self.normal_rect = SvgRectangle(self.normal_rect_element, self.height)
        scale_x = 0.5
        scale_y = 3
        self.normal_rect.scale(scale_x, scale_y)

        self.assertEqual(self.normal_rect.x, 25)
        self.assertEqual(self.normal_rect.y, 300)
        self.assertEqual(self.normal_rect.rect_width, (50, 0))
        self.assertEqual(self.normal_rect.rect_height, (0, -150))
        self.assertEqual(self.normal_rect.rx, (12.5, 0))
        self.assertEqual(self.normal_rect.ry, (0, 45))

    def test_transform(self):
        self.normal_rect_element['transform'] = 'translate(20)'
        translated_rect = SvgRectangle(self.normal_rect_element, self.height)
        self.assertEqual(translated_rect.x, 70)
        self.assertEqual(translated_rect.y, 100)
        self.assertEqual(translated_rect.rect_width, (100, 0))
        self.assertEqual(translated_rect.rect_height, (0,-50))
        self.assertEqual(translated_rect.rx, (0, 0))
        self.assertEqual(translated_rect.ry, (0, 0))

        self.normal_rect_element['transform'] = 'translate(-20, 60)'
        translated_rect = SvgRectangle(self.normal_rect_element, self.height)
        self.assertEqual(translated_rect.x, 30)
        self.assertEqual(translated_rect.y, 160)

        transformation_element = {'x':2, 'y':2, 'width':6, 'height':3, 'transform':'rotate(32)', 'rx':2, 'ry':1}
        transformation_height = 15
        rotated_rect = SvgRectangle(transformation_element, transformation_height)
        self.assertEqual(rotated_rect.x, 0.63626)
        self.assertEqual(rotated_rect.y, 12.24407)
        self.assertEqual(rotated_rect.rect_width, (5.08829, -3.17952))
        self.assertEqual(rotated_rect.rect_height, (-1.58976, -2.54414))
        self.assertEqual(rotated_rect.rx, (1.69610, -1.05984))
        self.assertEqual(rotated_rect.ry, (0.52992, 0.84805))


        transformation_element['transform'] = 'scale(0.5)'
        scaled_rect = SvgRectangle(transformation_element, transformation_height)
        self.assertEqual(scaled_rect.x, 1)
        self.assertEqual(scaled_rect.y, 14)
        self.assertEqual(scaled_rect.rect_width, (3, 0))
        self.assertEqual(scaled_rect.rect_height, (0, -1.5))
        self.assertEqual(scaled_rect.rx, (1, 0))
        self.assertEqual(scaled_rect.ry, (0, 0.5))

        transformation_element['transform'] = 'scale(2, 5)'
        scaled_rect = SvgRectangle(transformation_element, transformation_height)
        self.assertEqual(scaled_rect.x, 4)
        self.assertEqual(scaled_rect.y, 5)
        self.assertEqual(scaled_rect.rect_width, (12, 0))
        self.assertEqual(scaled_rect.rect_height, (0, -15))
        self.assertEqual(scaled_rect.rx, (4, 0))
        self.assertEqual(scaled_rect.ry, (0, 5))

        transformation_element['transform'] = "rotate(90) scale(0.5)"
        rot_scaled_rect = SvgRectangle(transformation_element, transformation_height)
        self.assertEqual(rot_scaled_rect.x, -1)
        self.assertEqual(rot_scaled_rect.y, 14)
        self.assertEqual(rot_scaled_rect.rect_width, (0, -3))
        self.assertEqual(rot_scaled_rect.rect_height, (-1.5, 0))
        self.assertEqual(rot_scaled_rect.rx, (0, -1))
        self.assertEqual(rot_scaled_rect.ry, (0.5, 0))

        transformation_element['transform'] = "skewX(34)"
        skew_x_rect = SvgRectangle(transformation_element, transformation_height)
        self.assertAlmostEqual(skew_x_rect.x, 3.34902, 5)
        self.assertEqual(skew_x_rect.y, 13)
        self.assertEqual(skew_x_rect.rect_width, (6, 0))
        self.assertAlmostEqual(skew_x_rect.rect_height[0], 2.02353, 5)
        self.assertEqual(skew_x_rect.rect_height[1], -3)
        """self.assertEqual(skew_x_rect.rx, (2,0))
        self.assertAlmostEqual(skew_x_rect.ry[0], 0.67451, 5)
        self.assertEqual(skew_x_rect.ry[1], 1)"""

        transformation_element['transform'] = "skewY(-26)"
        skew_y_rect = SvgRectangle(transformation_element, transformation_height)
        self.assertEqual(skew_y_rect.x, 2)
        self.assertAlmostEqual(skew_y_rect.y, 13.97547, 5)
        self.assertEqual(skew_y_rect.rect_width[0], 6)
        self.assertAlmostEqual(skew_y_rect.rect_width[1], 2.926396, 6)
        self.assertEqual(skew_y_rect.rect_height, (0, -3))
        """self.assertEqual(skew_y_rect.rx[0], 2)
        self.assertAlmostEqual(skew_y_rect.rx[1], -0.97547, 5)
        self.assertEqual(skew_y_rect.ry, (0, 1))"""

        matrix_trafo_element = {'x': 10, 'y': 10, 'width': 30, 'height': 20, 'transform':"matrix(3 1 -1 3 30 40)", 'rx':10, 'ry':5}
        matrix_trafo_rect = SvgRectangle(matrix_trafo_element, self.height)
        self.assertEqual(matrix_trafo_rect.x, 50)
        self.assertEqual(matrix_trafo_rect.y, 120)
        self.assertEqual(matrix_trafo_rect.rect_width, (90, -30))
        self.assertEqual(matrix_trafo_rect.rect_height, (-20, -60))
        """ self.assertEqual(matrix_trafo_rect.rx, (30, 10))
        self.assertEqual(matrix_trafo_rect.ry, (-5, 15))"""
