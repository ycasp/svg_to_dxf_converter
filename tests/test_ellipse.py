import unittest

from src.shapes.ellipse import Ellipse
from unittest.mock import Mock
from math import pi

from src.svg_shapes import SvgEllipse


class TestEllipse(unittest.TestCase):

    def setUp(self):
        self.height = 100
        self.msp_mock = Mock()

        element_basic_ellipse_mayor_x = {'cx':10, 'cy':10, 'rx':10, 'ry':5}
        self.svg_basic_ellipse_mayor_x = SvgEllipse(element_basic_ellipse_mayor_x, self.height)

        element_basic_ellipse_mayor_y = {'cx': 10, 'cy': 10, 'rx': 5, 'ry': 10}
        self.svg_basic_ellipse_mayor_y = SvgEllipse(element_basic_ellipse_mayor_y, self.height)

        element_rotated_ellipse_mayor_x = {'cx': "1", 'cy': "-1", 'rx': "1", 'ry': "0.5", 'transform': "rotate(90)"}
        self.svg_rotated_ellipse_mayor_x = SvgEllipse(element_rotated_ellipse_mayor_x, 0)

        element_ccw_rotated_ellipse_mayor_y = {'cx': "-1", 'cy': "1", 'rx': "0.5", 'ry': "2", 'transform': "rotate(-90)"}
        self.svg_ccw_rotated_ellipse_mayor_y = SvgEllipse(element_ccw_rotated_ellipse_mayor_y, 0)

    def test_initialization(self):
        # with x as mayor axis
        basic_ellipse_mayor_x = Ellipse(self.svg_basic_ellipse_mayor_x, 1/2 * pi, 3/2 * pi)

        self.assertEqual(basic_ellipse_mayor_x.center, (10, 90))
        self.assertEqual(basic_ellipse_mayor_x.mayor_axis, (10,0))
        self.assertEqual(basic_ellipse_mayor_x.ratio, 0.5)
        self.assertEqual(basic_ellipse_mayor_x.start_param, 1/2 * pi)
        self.assertEqual(basic_ellipse_mayor_x.end_param, 3/2 * pi)

        # with y as mayor axis
        basic_ellipse_mayor_y = Ellipse(self.svg_basic_ellipse_mayor_y, 0, 3/2 * pi)

        self.assertEqual(basic_ellipse_mayor_y.center, (10, 90))
        self.assertEqual(basic_ellipse_mayor_y.mayor_axis, (0, 10))
        self.assertEqual(basic_ellipse_mayor_y.ratio, 0.5)
        self.assertEqual(basic_ellipse_mayor_y.start_param, - 1/2 * pi)
        self.assertEqual(basic_ellipse_mayor_y.end_param, pi)

        # rotated ellipse with x as mayor axis
        rotated_ellipse_mayor_x = Ellipse(self.svg_rotated_ellipse_mayor_x)

        self.assertEqual(rotated_ellipse_mayor_x.center, (1,-1))
        self.assertEqual(rotated_ellipse_mayor_x.mayor_axis, (0,-1))
        self.assertEqual(rotated_ellipse_mayor_x.ratio, 0.5)
        self.assertEqual(rotated_ellipse_mayor_x.start_param, 0)
        self.assertEqual(rotated_ellipse_mayor_x.end_param, 2 * pi)

        # rotated ellipse with y as mayor axis
        # to do some more testing, changed cx, cy
        rotated_ellipse_mayor_y = Ellipse(self.svg_ccw_rotated_ellipse_mayor_y)

        self.assertEqual(rotated_ellipse_mayor_y.center, (1, -1))
        self.assertEqual(rotated_ellipse_mayor_y.mayor_axis, (-2,0))
        self.assertEqual(rotated_ellipse_mayor_y.ratio, 0.25)
        self.assertEqual(rotated_ellipse_mayor_y.start_param, -1/2 * pi)
        self.assertEqual(rotated_ellipse_mayor_y.end_param, 3/2 * pi)

    def test_draw_dxf_ellipse(self):
        # with x as mayor axis
        basic_ellipse_mayor_x = Ellipse(self.svg_basic_ellipse_mayor_x)
        basic_ellipse_mayor_x.draw_dxf_ellipse(self.msp_mock)

        self.msp_mock.add_ellipse.assert_called_once_with((10,90), (10,0), 0.5, 0, 2 * pi)
        self.msp_mock.reset_mock()

        # with y as mayor axis
        basic_ellipse_mayor_y = Ellipse(self.svg_basic_ellipse_mayor_y)
        basic_ellipse_mayor_y.draw_dxf_ellipse(self.msp_mock)

        self.msp_mock.add_ellipse.assert_called_once_with((10, 90), (0, 10), 0.5, -1/2 * pi, 3 / 2 * pi)
        self.msp_mock.reset_mock()

        # rotated ellipse with x as mayor axis
        rotated_ellipse_mayor_x = Ellipse(self.svg_rotated_ellipse_mayor_x, 6 / 5 * pi, 8 / 5 * pi)
        rotated_ellipse_mayor_x.draw_dxf_ellipse(self.msp_mock)

        self.msp_mock.add_ellipse.assert_called_once_with((1, -1), (0, -1), 0.5, 6 / 5 * pi, 8 / 5 * pi)
        self.msp_mock.reset_mock()

        # rotated ellipse with y as mayor axis
        rotated_ellipse_mayor_y = Ellipse(self.svg_ccw_rotated_ellipse_mayor_y, 6 / 5 * pi, 8 / 5 * pi)
        rotated_ellipse_mayor_y.draw_dxf_ellipse(self.msp_mock)

        self.msp_mock.add_ellipse.assert_called_once_with((1, -1), (-2, 0), 0.25,
                                                          6 / 5 * pi - 1 / 2 * pi, 8 / 5 * pi - 1 / 2 * pi)
        self.msp_mock.reset_mock()
