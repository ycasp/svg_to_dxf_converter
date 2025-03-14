import unittest

from src.svg_shapes.svgPolygon import *


class TestSvgPolygon(unittest.TestCase):
    def setUp(self):
        self.svg_height = 800
        self.polygon_element = {'points': "80,50 150,130 50,150"}

    def test_initialization(self):
        polygon = SvgPolygon(self.polygon_element, self.svg_height)
        self.assertListEqual(polygon.point_list, [(80, 750), (150, 670), (50, 650)])

    def test_getter(self):
        polygon = SvgPolygon(self.polygon_element, self.svg_height)
        self.assertEqual(polygon.get_name(), 'polygon')

    def test_scale(self):
        scale_x = 0.5
        scale_y = 2
        polygon = SvgPolygon(self.polygon_element, self.svg_height)
        polygon.scale(scale_x, scale_y)
        self.assertListEqual(polygon.point_list, [(40, 1500), (75, 1340), (25, 1300)])

    def test_transformation(self):
        self.polygon_element['transform'] = 'translate(-33)'
        x_translated_polygon = SvgPolygon(self.polygon_element, self.svg_height)
        self.assertListEqual(x_translated_polygon.point_list, [(47, 750), (117, 670), (17, 650)])

        self.polygon_element['transform'] = 'translate(12,48)'
        translated_polygon = SvgPolygon(self.polygon_element, self.svg_height)
        self.assertListEqual(translated_polygon.point_list, [(92, 702), (162, 622), (62, 602)])

        self.polygon_element['transform'] = 'rotate(193)'
        rotated_polygon = SvgPolygon(self.polygon_element, self.svg_height)
        rotated_points = [(-66.70205, self.svg_height + 66.71459), (-116.91187, self.svg_height + 160.41077),
            (-14.97585, self.svg_height + 157.40306)]
        for i in range(0, 3):
            self.assertAlmostEqual(rotated_polygon.point_list[i][0], rotated_points[i][0], 5)
            self.assertAlmostEqual(rotated_polygon.point_list[i][1], rotated_points[i][1], 5)

        self.polygon_element['transform'] = 'rotate(61, 263, 123)'
        rotated_polygon = SvgPolygon(self.polygon_element, self.svg_height)
        rotated_points = [(238.12708, self.svg_height + 72.44651), (202.09417, self.svg_height - 27.56164),
            (136.12082, self.svg_height + 50.20414)]
        for i in range(0, 3):
            self.assertAlmostEqual(rotated_polygon.point_list[i][0], rotated_points[i][0], 5)
            self.assertAlmostEqual(rotated_polygon.point_list[i][1], rotated_points[i][1], 5)

        self.polygon_element['transform'] = 'scale(0.2)'
        scaled_polygon = SvgPolygon(self.polygon_element, self.svg_height)
        self.assertListEqual(scaled_polygon.point_list, [(16, 790), (30, 774), (10, 770)])

        self.polygon_element['transform'] = 'scale(5, 2)'
        scaled_polygon = SvgPolygon(self.polygon_element, self.svg_height)
        self.assertListEqual(scaled_polygon.point_list, [(400, 700), (750, 540), (250, 500)])

        self.polygon_element['transform'] = 'skewX(-52)'
        skew_x_polygon = SvgPolygon(self.polygon_element, self.svg_height)
        skew_x_points = [(16.00292, 750), (-16.39241, 670), (-141.99124, 650)]
        for i in range(0, 3):
            self.assertAlmostEqual(skew_x_polygon.point_list[i][0], skew_x_points[i][0], 5)
            self.assertAlmostEqual(skew_x_polygon.point_list[i][1], skew_x_points[i][1], 5)

        self.polygon_element['transform'] = 'skewY(11)'
        skew_y_polygon = SvgPolygon(self.polygon_element, self.svg_height)
        skew_y_points = [(80, self.svg_height - 65.55042), (150, self.svg_height - 159.15705),
            (50, self.svg_height - 159.71902)]
        for i in range(0, 3):
            self.assertAlmostEqual(skew_y_polygon.point_list[i][0], skew_y_points[i][0], 5)
            self.assertAlmostEqual(skew_y_polygon.point_list[i][1], skew_y_points[i][1], 5)

        self.polygon_element['transform'] = 'matrix(2, 0.3, 2, 0.8, -32, 23)'
        mat_polygon = SvgPolygon(self.polygon_element, self.svg_height)
        mat_points = [(228, 713), (528, self.svg_height - 172), (368, self.svg_height - 158)]
        for i in range(0, 3):
            self.assertAlmostEqual(mat_polygon.point_list[i][0], mat_points[i][0], 5)
            self.assertAlmostEqual(mat_polygon.point_list[i][1], mat_points[i][1], 5)
