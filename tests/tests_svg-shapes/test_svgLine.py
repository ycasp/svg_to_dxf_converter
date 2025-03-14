import unittest

from src.svg_shapes.svgLine import *


class TestSvgLine(unittest.TestCase):
    def setUp(self):
        self.svg_height = 600
        self.line_element = {'x1': "50", 'y1': "50", 'x2': "150", 'y2': "30"}

    def test_initialisation(self):
        line = SvgLine(self.line_element, self.svg_height)
        self.assertEqual(line.x1, 50)
        self.assertEqual(line.y1, 550)
        self.assertEqual(line.x2, 150)
        self.assertEqual(line.y2, 570)

    def test_getters(self):
        line = SvgLine(self.line_element, self.svg_height)
        self.assertEqual(line.get_name(), 'line')

    def test_scale(self):
        scale_x = 2
        scale_y = 3
        line = SvgLine(self.line_element, self.svg_height)

        line.scale(scale_x, scale_y)

        self.assertEqual(line.x1, 100)
        self.assertEqual(line.y1, 1650)
        self.assertEqual(line.x2, 300)
        self.assertEqual(line.y2, 1710)

    def test_transformation(self):
        self.line_element['transform'] = "translate(30)"
        x_translated_line = SvgLine(self.line_element, self.svg_height)
        self.assertEqual(x_translated_line.x1, 80)
        self.assertEqual(x_translated_line.y1, 550)
        self.assertEqual(x_translated_line.x2, 180)
        self.assertEqual(x_translated_line.y2, 570)

        self.line_element['transform'] = "translate(-30, 60)"
        translated_line = SvgLine(self.line_element, self.svg_height)
        self.assertEqual(translated_line.x1, 20)
        self.assertEqual(translated_line.y1, 490)
        self.assertEqual(translated_line.x2, 120)
        self.assertEqual(translated_line.y2, 510)

        self.line_element['transform'] = "rotate(42)"
        rotated_line = SvgLine(self.line_element, self.svg_height)
        self.assertAlmostEqual(rotated_line.x1, 3.70071, 5)
        self.assertAlmostEqual(rotated_line.y1, 600 - 70.61377, 5)
        self.assertAlmostEqual(rotated_line.x2, 91.39781, 5)
        self.assertAlmostEqual(rotated_line.y2, 600 - 122.66394, 5)

        self.line_element['transform'] = "rotate(42, 100, 250)"
        rotated_line = SvgLine(self.line_element, self.svg_height)
        self.assertAlmostEqual(rotated_line.x1, 196.66888, 5)
        self.assertAlmostEqual(rotated_line.y1, 600 - 67.91450, 5)
        self.assertAlmostEqual(rotated_line.x2, 284.36597, 5)
        self.assertAlmostEqual(rotated_line.y2, 600 - 119.96467, 5)

        self.line_element['transform'] = "scale(0.2)"
        x_scaled_line = SvgLine(self.line_element, self.svg_height)
        self.assertEqual(x_scaled_line.x1, 10)
        self.assertEqual(x_scaled_line.y1, 590)
        self.assertEqual(x_scaled_line.x2, 30)
        self.assertEqual(x_scaled_line.y2, 594)

        self.line_element['transform'] = "scale(3,4)"
        scaled_line = SvgLine(self.line_element, self.svg_height)
        self.assertEqual(scaled_line.x1, 150)
        self.assertEqual(scaled_line.y1, 400)
        self.assertEqual(scaled_line.x2, 450)
        self.assertEqual(scaled_line.y2, 480)

        self.line_element['transform'] = "skewX(41)"
        skew_x_line = SvgLine(self.line_element, self.svg_height)
        self.assertAlmostEqual(skew_x_line.x1, 93.46434, 5)
        self.assertEqual(skew_x_line.y1, 550)
        self.assertAlmostEqual(skew_x_line.x2, 176.07860, 5)
        self.assertEqual(skew_x_line.y2, 570)

        self.line_element['transform'] = "skewY(27)"
        skew_y_line = SvgLine(self.line_element, self.svg_height)
        self.assertEqual(skew_y_line.x1, 50)
        self.assertAlmostEqual(skew_y_line.y1, 600 - 75.47627, 5)
        self.assertEqual(skew_y_line.x2, 150)
        self.assertAlmostEqual(skew_y_line.y2, 600 - 106.42882, 5)

        self.line_element['transform'] = 'matrix(3, 0.5, 0.7, 0.4, 30, 20)'
        matrix_line = SvgLine(self.line_element, self.svg_height)
        self.assertEqual(matrix_line.x1, 215)
        self.assertEqual(matrix_line.y1, 535)
        self.assertEqual(matrix_line.x2, 501)
        self.assertEqual(matrix_line.y2, 493)
