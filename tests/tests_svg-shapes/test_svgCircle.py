import unittest

from ezdxf.render.forms import circle

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
        self.assertEqual(circle.transform, None)

        rot_circle = SvgCircle(self.rot_circle, self.svg_height)
        self.assertEqual(rot_circle.name, 'circle')
        self.assertEqual(rot_circle.center_x, -100)
        self.assertEqual(rot_circle.center_y, 200)
        self.assertEqual(rot_circle.radius, 50)
        self.assertNotEqual(rot_circle.transform, None)

    def test_getters(self):
        normal_circle = SvgCircle(self.normal_circle, self.svg_height)
        self.assertEqual(normal_circle.get_circle_name(), 'circle')

        rot_circle = SvgCircle(self.rot_circle, self.svg_height)
        self.assertEqual(rot_circle.get_circle_name(), 'circle')
