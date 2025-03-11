import unittest

from src.svg_shapes.svgPolyline import *

class TestSvgPolyline(unittest.TestCase):
    def setUp(self):
        self.svg_height = 800
        self.polyline_element = {'points':"100,100 150,150 200,80 250,165 300,50"}

    def test_initialization(self):
        basic_polyline = SvgPolyline(self.polyline_element, self.svg_height)
        self.assertListEqual(basic_polyline.point_list, [(100, 700), (150, 650), (200, 720), (250, 635), (300, 750)])

    def test_getter(self):
        basic_polyline = SvgPolyline(self.polyline_element, self.svg_height)
        self.assertEqual(basic_polyline.get_name(), 'polyline')

    def test_scale(self):
        scale_x = 2
        scale_y = 0.5
        basic_polyline = SvgPolyline(self.polyline_element, self.svg_height)
        basic_polyline.scale(scale_x, scale_y)
        self.assertListEqual(basic_polyline.point_list, [(200, 350), (300, 325), (400, 360), (500, 317.5), (600, 375)])

    def test_transformation(self):
        self.polyline_element['transform'] = 'translate(-34)'
        x_translated_polyline = SvgPolyline(self.polyline_element, self.svg_height)
        self.assertListEqual(x_translated_polyline.point_list, [(66, 700), (116, 650), (166, 720), (216, 635), (266, 750)])

        self.polyline_element['transform'] = 'translate(28, 41)'
        translated_polyline = SvgPolyline(self.polyline_element, self.svg_height)
        self.assertListEqual(translated_polyline.point_list, [(128, 659), (178, 609), (228, 679), (278, 594), (328, 709)])

        self.polyline_element['transform'] = 'rotate(273)'
        rotated_polyline = SvgPolyline(self.polyline_element, self.svg_height)
        rotated_points = [(105.09655, self.svg_height + 94.62936), (157.64482, self.svg_height + 141.94404),
            (90.35755, self.svg_height + 195.53903), (177.85786, self.svg_height + 241.02195),
            (65.63226, self.svg_height + 296.97206)]
        for i in range (0, 3):
            self.assertAlmostEqual(rotated_polyline.point_list[i][0], rotated_points[i][0], 5)
            self.assertAlmostEqual(rotated_polyline.point_list[i][1], rotated_points[i][1], 5)

        self.polyline_element['transform'] = 'rotate(-32, 158, 56)'
        rotated_polyline = SvgPolyline(self.polyline_element, self.svg_height)
        rotated_points = [(132.12966, self.svg_height - 124.04943), (201.02803, self.svg_height - 139.95588),
            (206.33608, self.svg_height - 54.09655), (293.78162, self.svg_height - 99.68467),
            (275.24331, self.svg_height + 24.33682)]
        for i in range(0, 3):
            self.assertAlmostEqual(rotated_polyline.point_list[i][0], rotated_points[i][0], 5)
            self.assertAlmostEqual(rotated_polyline.point_list[i][1], rotated_points[i][1], 5)

        self.polyline_element['transform'] = 'scale(2)'
        scaled_polyline = SvgPolyline(self.polyline_element, self.svg_height)
        self.assertListEqual(scaled_polyline.point_list, [(200, 600), (300, 500), (400, 640), (500, 470), (600, 700)])

        self.polyline_element['transform'] = 'scale(0.3, 1.2)'
        scaled_polyline = SvgPolyline(self.polyline_element, self.svg_height)
        self.assertListEqual(scaled_polyline.point_list, [(30, 680), (45, 620), (60, 704), (75, 602), (90, 740)])

        self.polyline_element['transform'] = 'skewX(39)'
        skew_x_polyline = SvgPolyline(self.polyline_element, self.svg_height)
        skew_x_points = [(180.97840, 700), (271.46760, 650), (264.78272, 720), (383.61437, 635), (340.48920, 750)]
        for i in range(0, 3):
            self.assertAlmostEqual(skew_x_polyline.point_list[i][0], skew_x_points[i][0], 5)
            self.assertAlmostEqual(skew_x_polyline.point_list[i][1], skew_x_points[i][1], 5)

        self.polyline_element['transform'] = 'skewY(81)'
        skew_y_polyline = SvgPolyline(self.polyline_element, self.svg_height)
        skew_y_points = [(100, self.svg_height - 731.37515), (150, self.svg_height - 1097.062727),
            (200, self.svg_height - 1342.75030), (250, self.svg_height - 1743.43788),
            (300, self.svg_height - 1944.125454)]
        for i in range(0, 3):
            self.assertAlmostEqual(skew_y_polyline.point_list[i][0], skew_y_points[i][0], 5)
            self.assertAlmostEqual(skew_y_polyline.point_list[i][1], skew_y_points[i][1], 5)

        self.polyline_element['transform'] = 'matrix(5, 8, 0.1, 0.3, 85, 58)'
        mat_polyline = SvgPolyline(self.polyline_element, self.svg_height)
        mat_points = [(595, self.svg_height - 888), (850, self.svg_height - 1303), (1093, self.svg_height - 1682),
            (1351.5, self.svg_height - 2107.5), (1590, self.svg_height - 2473)]
        for i in range(0, 3):
            self.assertAlmostEqual(mat_polyline.point_list[i][0], mat_points[i][0], 5)
            self.assertAlmostEqual(mat_polyline.point_list[i][1], mat_points[i][1], 5)