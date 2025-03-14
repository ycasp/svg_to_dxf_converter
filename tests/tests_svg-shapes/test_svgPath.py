import unittest

from svgpathtools import Path

from src.svg_shapes.svgPath import *


class TestSvgPath(unittest.TestCase):
    def setUp(self):
        self.svg_height = 1000
        self.path_element = {'d': "M100 100 L200 100 Q250 50, 300 100 C350 150, 450 50, 500 100 A50 50 0 0 1 600 100"}

    def assertComplexAlmostEqual(self, a, b, places=4):
        self.assertAlmostEqual(a.real, b.real, places=places)
        self.assertAlmostEqual(a.imag, b.imag, places=places)

    def test_initialization(self):
        basic_path = SvgPath(self.path_element, self.svg_height)
        basic_parsed_path = Path(Line(complex(100, 900), complex(200, 900)),
                                 QuadraticBezier(complex(200, 900), complex(250, 950), complex(300, 900)),
                                 CubicBezier(complex(300, 900), complex(350, 850), complex(450, 950),
                                             complex(500, 900)),
                                 Arc(complex(500, 900), complex(50, 50), 0, False, True,
                                     complex(600, 900)))
        self.assertEqual(basic_path.parsed_path, basic_parsed_path)

    def test_getter(self):
        basic_path = SvgPath(self.path_element, self.svg_height)
        self.assertEqual(basic_path.get_name(), 'path')

    def test_scale(self):
        basic_path = SvgPath(self.path_element, self.svg_height)
        basic_path.scale(0.5, 0.5)
        scaled_parsed_path = Path(Line(complex(50, 450), complex(100, 450)),
                                  QuadraticBezier(complex(100, 450), complex(125, 475), complex(150, 450)),
                                  CubicBezier(complex(150, 450), complex(175, 425), complex(225, 475),
                                              complex(250, 450)),
                                  Arc(complex(250, 450), complex(25, 25), 0, False, True,
                                      complex(300, 450)))
        self.assertEqual(basic_path.parsed_path, scaled_parsed_path)

    def test_transform(self):
        self.path_element['transform'] = "translate(30)"
        x_translate_path = SvgPath(self.path_element, self.svg_height)
        x_translate_parsed_path = Path(Line(complex(100 + 30, 900), complex(200 + 30, 900)),
                                       QuadraticBezier(complex(200 + 30, 900), complex(250 + 30, 950),
                                                       complex(300 + 30, 900)),
                                       CubicBezier(complex(300 + 30, 900), complex(350 + 30, 850),
                                                   complex(450 + 30, 950),
                                                   complex(500 + 30, 900)),
                                       Arc(complex(500 + 30, 900), complex(50, 50), 0, False, True,
                                           complex(600 + 30, 900)))
        self.assertEqual(x_translate_path.parsed_path, x_translate_parsed_path)

        self.path_element['transform'] = "translate(-10, 90)"
        translated_path = SvgPath(self.path_element, self.svg_height)
        translated_parsed_path = Path(Line(complex(90, 810), complex(190, 810)),
                                      QuadraticBezier(complex(190, 810), complex(240, 860), complex(290, 810)),
                                      CubicBezier(complex(290, 810), complex(340, 760), complex(440, 860),
                                                  complex(490, 810)),
                                      Arc(complex(490, 810), complex(50, 50), 0, False, True,
                                          complex(590, 810)))
        self.assertEqual(translated_path.parsed_path, translated_parsed_path)

        self.path_element['transform'] = "rotate(19)"
        origin_rotated_path = SvgPath(self.path_element, self.svg_height)

        line = origin_rotated_path.parsed_path.__getitem__(0)
        self.assertComplexAlmostEqual(line.start, complex(61.9950, self.svg_height - 127.1087), 4)
        self.assertComplexAlmostEqual(line.end, complex(156.5469, self.svg_height - 159.6655), 4)

        quad_bez = origin_rotated_path.parsed_path.__getitem__(1)
        self.assertComplexAlmostEqual(quad_bez.start, complex(156.5469, self.svg_height - 159.6655), 4)
        self.assertComplexAlmostEqual(quad_bez.control, complex(220.1012, self.svg_height - 128.6680), 4)
        self.assertComplexAlmostEqual(quad_bez.end, complex(251.0988, self.svg_height - 192.2223), 4)

        cub_bez = origin_rotated_path.parsed_path.__getitem__(2)
        self.assertComplexAlmostEqual(cub_bez.start, complex(251.0988, self.svg_height - 192.2223), 4)
        self.assertComplexAlmostEqual(cub_bez.control1, complex(282.0963, self.svg_height - 255.7766), 4)
        self.assertComplexAlmostEqual(cub_bez.control2, complex(409.2050, self.svg_height - 193.7816), 4)
        self.assertComplexAlmostEqual(cub_bez.end, complex(440.2025, self.svg_height - 257.3359), 4)

        arc = origin_rotated_path.parsed_path.__getitem__(3)
        self.assertComplexAlmostEqual(arc.start, complex(440.2025, self.svg_height - 257.3359), 4)
        self.assertComplexAlmostEqual(arc.radius, complex(50, 50), 4)
        self.assertComplexAlmostEqual(arc.end, complex(534.7543, self.svg_height - 289.8928), 4)

        self.path_element['transform'] = "rotate(38, 375, 175)"
        rotated_path = SvgPath(self.path_element, self.svg_height)

        line = rotated_path.parsed_path.__getitem__(0)
        self.assertComplexAlmostEqual(line.start, complex(204.4717, self.svg_height + 53.4077), 4)
        self.assertComplexAlmostEqual(line.end, complex(283.2727, self.svg_height - 8.1584), 4)

        quad_bez = rotated_path.parsed_path.__getitem__(1)
        self.assertComplexAlmostEqual(quad_bez.start, complex(283.2727, self.svg_height - 8.1584), 4)
        self.assertComplexAlmostEqual(quad_bez.control, complex(353.4563, self.svg_height + 0.4590), 4)
        self.assertComplexAlmostEqual(quad_bez.end, complex(362.0738, self.svg_height - 69.7246), 4)

        cub_bez = rotated_path.parsed_path.__getitem__(2)
        self.assertComplexAlmostEqual(cub_bez.start, complex(362.0738, self.svg_height - 69.7246), 4)
        self.assertComplexAlmostEqual(cub_bez.control1, complex(370.6913, self.svg_height - 139.9082), 4)
        self.assertComplexAlmostEqual(cub_bez.control2, complex(511.0585, self.svg_height - 122.6733), 4)
        self.assertComplexAlmostEqual(cub_bez.end, complex(519.6760, self.svg_height - 192.8569), 4)

        arc = rotated_path.parsed_path.__getitem__(3)
        self.assertComplexAlmostEqual(arc.start, complex(519.6760, self.svg_height - 192.8569), 4)
        self.assertComplexAlmostEqual(arc.radius, complex(50, 50), 4)
        self.assertComplexAlmostEqual(arc.end, complex(598.4770, self.svg_height - 254.4230), 4)

        self.path_element['transform'] = "skewX(24)"
        skew_x_path = SvgPath(self.path_element, self.svg_height)

        line = skew_x_path.parsed_path.__getitem__(0)
        self.assertComplexAlmostEqual(line.start, complex(144.5229, 900), 4)
        self.assertComplexAlmostEqual(line.end, complex(244.5229, 900), 4)

        quad_bez = skew_x_path.parsed_path.__getitem__(1)
        self.assertComplexAlmostEqual(quad_bez.start, complex(244.5229, 900), 4)
        self.assertComplexAlmostEqual(quad_bez.control, complex(272.2614, 950), 4)
        self.assertComplexAlmostEqual(quad_bez.end, complex(344.5229, 900), 4)

        cub_bez = skew_x_path.parsed_path.__getitem__(2)
        self.assertComplexAlmostEqual(cub_bez.start, complex(344.5229, 900), 4)
        self.assertComplexAlmostEqual(cub_bez.control1, complex(416.7843, 850), 4)
        self.assertComplexAlmostEqual(cub_bez.control2, complex(472.2614, 950), 4)
        self.assertComplexAlmostEqual(cub_bez.end, complex(544.5229, 900), 4)

        arc = skew_x_path.parsed_path.__getitem__(3)
        self.assertComplexAlmostEqual(arc.start, complex(544.5229, 900), 4)
        self.assertComplexAlmostEqual(arc.radius, complex(62.3547, 40.0932), 4)
        self.assertComplexAlmostEqual(arc.end, complex(644.5229, 900), 4)

        self.path_element['transform'] = "skewY(24)"
        skew_y_path = SvgPath(self.path_element, self.svg_height)

        line = skew_y_path.parsed_path.__getitem__(0)
        self.assertComplexAlmostEqual(line.start, complex(100, self.svg_height - 144.5229), 4)
        self.assertComplexAlmostEqual(line.end, complex(200, self.svg_height - 189.0457), 4)

        quad_bez = skew_y_path.parsed_path.__getitem__(1)
        self.assertComplexAlmostEqual(quad_bez.start, complex(200, self.svg_height - 189.0457), 4)
        self.assertComplexAlmostEqual(quad_bez.control, complex(250, self.svg_height - 161.3072), 4)
        self.assertComplexAlmostEqual(quad_bez.end, complex(300, self.svg_height - 233.5686), 4)

        cub_bez = skew_y_path.parsed_path.__getitem__(2)
        self.assertComplexAlmostEqual(cub_bez.start, complex(300, self.svg_height - 233.5686), 4)
        self.assertComplexAlmostEqual(cub_bez.control1, complex(350, self.svg_height - 305.8300), 4)
        self.assertComplexAlmostEqual(cub_bez.control2, complex(450, self.svg_height - 250.3529), 4)
        self.assertComplexAlmostEqual(cub_bez.end, complex(500, self.svg_height - 322.6143), 4)

        arc = skew_y_path.parsed_path.__getitem__(3)
        self.assertComplexAlmostEqual(arc.start, complex(500, self.svg_height - 322.6143), 4)
        self.assertComplexAlmostEqual(arc.radius, complex(53.6847, 83.4927), 4)
        self.assertComplexAlmostEqual(arc.end, complex(600, self.svg_height - 367.1372), 4)

        self.path_element['transform'] = "scale(0.5)"
        scaled_path = SvgPath(self.path_element, self.svg_height)
        scaled_parsed_path = Path(Line(complex(50, 950), complex(100, 950)),
                                  QuadraticBezier(complex(100, 950), complex(125, 975), complex(150, 950)),
                                  CubicBezier(complex(150, 950), complex(175, 925), complex(225, 975),
                                              complex(250, 950)),
                                  Arc(complex(250, 950), complex(25, 25), 0, False, True,
                                      complex(300, 950)))
        self.assertEqual(scaled_path.parsed_path, scaled_parsed_path)

        self.path_element['transform'] = "matrix(2.5, 0.5, -0.5, 4, 100, 50)"
        mat_path = SvgPath(self.path_element, self.svg_height)
        mat_parsed_path = Path(Line(complex(300, 500), complex(550, 450)),
                               QuadraticBezier(complex(550, 450), complex(700, 625), complex(800, 400)),
                               CubicBezier(complex(800, 400), complex(900, 175), complex(1200, 525),
                                           complex(1300, 300)))
        arc = mat_path.parsed_path.__getitem__(3)
        mat_path.parsed_path.__delitem__(3)
        self.assertEqual(mat_path.parsed_path, mat_parsed_path)
        self.assertComplexAlmostEqual(arc.start, complex(1300, 300), 4)
        self.assertComplexAlmostEqual(arc.radius, complex(126.9118, 201.9118), 4)
        self.assertComplexAlmostEqual(arc.end, complex(1550, 250))
