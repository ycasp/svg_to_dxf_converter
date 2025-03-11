import unittest

from src.svg_shapes.svgCircle import *

class TestSvgCircle(unittest.TestCase):

    def setUp(self):
        self.normal_circle = {'cx': '100', 'cy': '100', 'r': '50'}
        self.rot_circle = {'cx': '100', 'cy': '100', 'r': '50', 'transform': 'rotate(90)'}
        self.svg_height = 300


    def test_initialization(self):
        circle = SvgCircle(self.normal_circle, self.svg_height)
        self.assertEqual(circle.name, 'circle')
        self.assertEqual(circle.center_x, 100)
        self.assertEqual(circle.center_y, 200)
        self.assertEqual(circle.radius, 50)

        rot_circle = SvgCircle(self.rot_circle, self.svg_height)
        self.assertEqual(rot_circle.name, 'circle')
        self.assertEqual(rot_circle.center_x, -100)
        self.assertEqual(rot_circle.center_y, 200)
        self.assertEqual(rot_circle.radius, 50)
        self.assertNotEqual(rot_circle.transformation_list, ['rotate', [90]])

    def test_getters(self):
        normal_circle = SvgCircle(self.normal_circle, self.svg_height)
        self.assertEqual(normal_circle.get_name(), 'circle')

        rot_circle = SvgCircle(self.rot_circle, self.svg_height)
        self.assertEqual(rot_circle.get_name(), 'circle')

    def test_scale(self):
        scale = 3
        circle = SvgCircle(self.normal_circle, self.svg_height)
        circle.scale(scale, scale)
        self.assertEqual(circle.name, 'circle')
        self.assertEqual(circle.center_x, 300)
        self.assertEqual(circle.center_y, 600)
        self.assertEqual(circle.radius, 150)

        scale_x = 0.5
        scale_y = 0.25
        rot_circle = SvgCircle(self.rot_circle, self.svg_height)
        rot_circle.scale(scale_x, scale_y)
        self.assertEqual(rot_circle.name, 'circle')
        self.assertEqual(rot_circle.center_x, -50)
        self.assertEqual(rot_circle.center_y, 50)
        self.assertEqual(rot_circle.radius, 25)
        self.assertNotEqual(rot_circle.transformation_list, ['rotate', [90]])

    def test_transform(self):
        self.normal_circle['transform'] = 'translate(40)'
        x_trans_circle = SvgCircle(self.normal_circle, self.svg_height)
        self.assertEqual(x_trans_circle.center_x, 140)
        self.assertEqual(x_trans_circle.center_y, 200)
        self.assertEqual(x_trans_circle.radius, 50)

        self.normal_circle['transform'] = 'translate(40, 150)'
        trans_circle = SvgCircle(self.normal_circle, self.svg_height)
        self.assertEqual(trans_circle.center_x, 140)
        self.assertEqual(trans_circle.center_y, 50)
        self.assertEqual(trans_circle.radius, 50)

        self.normal_circle['transform'] = 'rotate(90)'
        rot_circle = SvgCircle(self.normal_circle, self.svg_height)
        self.assertEqual(rot_circle.center_x, -100)
        self.assertEqual(rot_circle.center_y, 200)
        self.assertEqual(rot_circle.radius, 50)

        self.normal_circle['transform'] = 'rotate(-90, 100, 100)'
        rot_circle = SvgCircle(self.normal_circle, self.svg_height)
        self.assertEqual(rot_circle.center_x, 100)
        self.assertEqual(rot_circle.center_y, 200)
        self.assertEqual(rot_circle.radius, 50)

        self.normal_circle['transform'] = 'scale(0.5)'
        scaled_circle = SvgCircle(self.normal_circle, self.svg_height)
        self.assertEqual(scaled_circle.center_x, 50)
        self.assertEqual(scaled_circle.center_y, 250)
        self.assertEqual(scaled_circle.radius, 25)
        self.assertEqual(scaled_circle.radius_y, 0)

        self.normal_circle['transform'] = 'scale(0.5, 3)'
        scaled_circle = SvgCircle(self.normal_circle, self.svg_height)
        self.assertEqual(scaled_circle.center_x, 50)
        self.assertEqual(scaled_circle.center_y, 0)
        self.assertEqual(scaled_circle.radius, 25)
        self.assertEqual(scaled_circle.radius_y, 150)

        self.normal_circle['transform'] = 'matrix(1, 0, 0, 1, 30, -30)'
        matrix_circle = SvgCircle(self.normal_circle, self.svg_height)
        self.assertEqual(matrix_circle.center_x, 130)
        self.assertEqual(matrix_circle.center_y, 230)
        self.assertEqual(matrix_circle.radius, 50)

        self.normal_circle['transform'] = 'matrix(0, 1, 1, 0)'
        matrix_circle = SvgCircle(self.normal_circle, self.svg_height)
        self.assertEqual(matrix_circle.center_x, 100)
        self.assertEqual(matrix_circle.center_y, 200)
        self.assertEqual(matrix_circle.radius, 50)

        crazy_trafo_element = {'cx': '0', 'cy': '0', 'r': '1',
            'transform': 'rotate(90, 1, 0) translate(3, -5) matrix(0, -1, -1, 0) matrix(1, 0, 0, 1, -4, -6) scale(3)'}
        crazy_circle = SvgCircle(crazy_trafo_element, 10)
        self.assertEqual(crazy_circle.center_x, 6)
        self.assertEqual(crazy_circle.center_y, 40)
        self.assertEqual(crazy_circle.radius, 3)