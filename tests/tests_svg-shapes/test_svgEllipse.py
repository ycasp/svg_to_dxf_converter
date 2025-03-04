import unittest

from src.svg_shapes.svgEllipse import *

class TestSvgEllipse(unittest.TestCase):
    def setUp(self):
        self.normal_ellipse = {'cx':"70", 'cy':"50", 'rx':"60", 'ry':"40"}
        self.rotated_ellipse = {'cx':"70", 'cy':"50", 'rx':"60", 'ry':"40", 'transform': 'rotate(-90)'}
        self.svg_height = 100

    def test_initialization(self):
        normal_ellipse = SvgEllipse(self.normal_ellipse, self.svg_height)
        self.assertEqual(normal_ellipse.center_x, 70)
        self.assertEqual(normal_ellipse.center_y, 50)
        self.assertEqual(normal_ellipse.radius_x, (60, 0))
        self.assertEqual(normal_ellipse.radius_y, (0, 40))
        self.assertEqual(normal_ellipse.transform, None)
        self.assertEqual(normal_ellipse.name, 'ellipse')

        rot_ellipse = SvgEllipse(self.rotated_ellipse, self.svg_height)
        self.assertEqual(rot_ellipse.center_x, 50)
        self.assertEqual(rot_ellipse.center_y, 170)
        self.assertEqual(rot_ellipse.radius_x, (0, 60))
        self.assertEqual(rot_ellipse.radius_y, (-40, 0))
        self.assertEqual(rot_ellipse.transform, 'rotate(-90)')
        self.assertEqual(rot_ellipse.name, 'ellipse')

    def test_getters(self):
        normal_ellipse = SvgEllipse(self.normal_ellipse, self.svg_height)
        self.assertEqual(normal_ellipse.get_name(), 'ellipse')

        rot_ellipse = SvgEllipse(self.rotated_ellipse, self.svg_height)
        self.assertNotEqual(rot_ellipse.get_name(), 'circle')