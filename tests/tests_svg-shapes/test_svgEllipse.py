import unittest

from src.svg_shapes.svgEllipse import *

class TestSvgEllipse(unittest.TestCase):
    def setUp(self):
        self.svg_height = 700
        self.normal_ellipse = {'cx':"100", 'cy':"130", 'rx':"50", 'ry':"30"}


    def test_initialization(self):
        normal_ellipse = SvgEllipse(self.normal_ellipse, self.svg_height)
        self.assertEqual(normal_ellipse.center_x, 100)
        self.assertEqual(normal_ellipse.center_y, 570)
        self.assertEqual(normal_ellipse.radius_x, (50, 0))
        self.assertEqual(normal_ellipse.radius_y, (0, 30))
        self.assertEqual(normal_ellipse.name, 'ellipse')


    def test_getters(self):
        normal_ellipse = SvgEllipse(self.normal_ellipse, self.svg_height)
        self.assertEqual(normal_ellipse.get_name(), 'ellipse')


    def test_transform(self):
        self.normal_ellipse['transform'] = 'translate(20)'
        x_translated_ellipse = SvgEllipse(self.normal_ellipse, self.svg_height)
        self.assertEqual(x_translated_ellipse.center_x, 120)
        self.assertEqual(x_translated_ellipse.center_y, 570)
        self.assertEqual(x_translated_ellipse.radius_x, (50, 0))
        self.assertEqual(x_translated_ellipse.radius_y, (0, 30))

        self.normal_ellipse['transform'] = 'translate(-30, 50)'
        translated_ellipse = SvgEllipse(self.normal_ellipse, self.svg_height)
        self.assertEqual(translated_ellipse.center_x, 70)
        self.assertEqual(translated_ellipse.center_y, 520)
        self.assertEqual(translated_ellipse.radius_x, (50, 0))
        self.assertEqual(translated_ellipse.radius_y, (0, 30))

        self.normal_ellipse['transform'] = 'rotate(61)'
        rot_ellipse = SvgEllipse(self.normal_ellipse, self.svg_height)
        self.assertAlmostEqual(rot_ellipse.center_x, -65.2196, 4)
        self.assertAlmostEqual(rot_ellipse.center_y, self.svg_height - 150.4872, 4)
        self.assertAlmostEqual(rot_ellipse.radius_x[0], 24.2405, 4)
        self.assertAlmostEqual(rot_ellipse.radius_x[1], 43.7310, 4)
        self.assertAlmostEqual(rot_ellipse.radius_y[0], -26.2386, 4)
        self.assertAlmostEqual(rot_ellipse.radius_y[1], 14.5443, 4)

        self.normal_ellipse['transform'] = 'rotate(29, 120, 210)'
        rot_ellipse = SvgEllipse(self.normal_ellipse, self.svg_height)
        self.assertAlmostEqual(rot_ellipse.center_x, 141.2924, 4)
        self.assertAlmostEqual(rot_ellipse.center_y, self.svg_height - 130.3342, 4)
        self.assertAlmostEqual(rot_ellipse.radius_x[0], 43.7310, 4)
        self.assertAlmostEqual(rot_ellipse.radius_x[1], 24.2405, 4)
        self.assertAlmostEqual(rot_ellipse.radius_y[0], -14.5443, 4)
        self.assertAlmostEqual(rot_ellipse.radius_y[1], 26.2386, 4)

        self.normal_ellipse['transform'] = 'scale(0.6)'
        scaled_ellipse = SvgEllipse(self.normal_ellipse, self.svg_height)
        self.assertEqual(scaled_ellipse.center_x, 60)
        self.assertEqual(scaled_ellipse.center_y, 622)
        self.assertEqual(scaled_ellipse.radius_x, (30, 0))
        self.assertEqual(scaled_ellipse.radius_y, (0, 18))

        self.normal_ellipse['transform'] = 'scale(1.4, 2.6)'
        scaled_ellipse = SvgEllipse(self.normal_ellipse, self.svg_height)
        self.assertEqual(scaled_ellipse.center_x, 140)
        self.assertEqual(scaled_ellipse.center_y, 362)
        self.assertEqual(scaled_ellipse.radius_x, (70, 0))
        self.assertEqual(scaled_ellipse.radius_y, (0, 78))

        """self.normal_ellipse['transform'] = 'skewX(45)'
        ellipse = SvgEllipse(self.normal_ellipse, self.svg_height)

        self.normal_ellipse['transform'] = 'skewY(33)'
        ellipse = SvgEllipse(self.normal_ellipse, self.svg_height)

        self.normal_ellipse['transform'] = 'matrix()'
        ellipse = SvgEllipse(self.normal_ellipse, self.svg_height)"""