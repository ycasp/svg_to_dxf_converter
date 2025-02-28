import unittest

from src.shapes.ellipse import Ellipse
from unittest.mock import Mock
from math import pi

class TestEllipse(unittest.TestCase):

    def setUp(self):
        self.height = 100
        self.msp_mock = Mock()

    def test_initialization(self):
        cx = "10"; cy = "10"; rx = "10"; ry = "5"
        transformation = None

        # with x as mayor axis
        basic_ellipse_mayor_x = Ellipse(cx, cy, rx, ry, transformation, self.height, 0, 1/2 * pi, 3/2 * pi)

        self.assertEqual(basic_ellipse_mayor_x.center, (10, 90))
        self.assertEqual(basic_ellipse_mayor_x.mayor_axis, (10,0))
        self.assertEqual(basic_ellipse_mayor_x.ratio, 0.5)
        self.assertEqual(basic_ellipse_mayor_x.start_param, 1/2 * pi)
        self.assertEqual(basic_ellipse_mayor_x.end_param, 3/2 * pi)

        # with y as mayor axis
        basic_ellipse_mayor_y = Ellipse(cx, cy, ry, rx, transformation, self.height, 0, 0, 3/2 * pi)

        self.assertEqual(basic_ellipse_mayor_y.center, (10, 90))
        self.assertEqual(basic_ellipse_mayor_y.mayor_axis, (0, 10))
        self.assertEqual(basic_ellipse_mayor_y.ratio, 0.5)
        self.assertEqual(basic_ellipse_mayor_y.start_param, - 1/2 * pi)
        self.assertEqual(basic_ellipse_mayor_y.end_param, pi)

        # rotated ellipse with x as mayor axis
        cx = "1"; cy = "-1"; rx = "1"; ry = "0.5"
        transformation = "rotate(90)"

        rotated_ellipse_mayor_x = Ellipse(cx, cy, rx, ry, transformation, 0)

        self.assertEqual(rotated_ellipse_mayor_x.center, (1,-1))
        self.assertEqual(rotated_ellipse_mayor_x.mayor_axis, (0,-1))
        self.assertEqual(rotated_ellipse_mayor_x.ratio, 0.5)
        self.assertEqual(rotated_ellipse_mayor_x.start_param, 0)
        self.assertEqual(rotated_ellipse_mayor_x.end_param, 2 * pi)

        # rotated ellipse with y as mayor axis
        # to do some more testing, changed cx, cy
        transformation = "rotate(-90)"
        rotated_ellipse_mayor_y = Ellipse(cy, cx, ry, 2*float(rx), transformation, 0, 0)

        self.assertEqual(rotated_ellipse_mayor_y.center, (1, -1))
        self.assertEqual(rotated_ellipse_mayor_y.mayor_axis, (-2,0))
        self.assertEqual(rotated_ellipse_mayor_y.ratio, 0.25)
        self.assertEqual(rotated_ellipse_mayor_y.start_param, -1/2 * pi)
        self.assertEqual(rotated_ellipse_mayor_y.end_param, 3/2 * pi)

    def test_draw_dxf_ellipse(self):
        cx = "10"; cy = "10"; rx = "10"; ry = "5"
        transformation = None

        # with x as mayor axis
        basic_ellipse_mayor_x = Ellipse(cx, cy, rx, ry, transformation, self.height)
        basic_ellipse_mayor_x.draw_dxf_ellipse(self.msp_mock)

        self.msp_mock.add_ellipse.assert_called_once_with((10,90), (10,0), 0.5, 0, 2 * pi)
        self.msp_mock.reset_mock()

        # with y as mayor axis
        basic_ellipse_mayor_y = Ellipse(cx, cy, ry, rx, transformation, self.height, 0, 0, 2 * pi)
        basic_ellipse_mayor_y.draw_dxf_ellipse(self.msp_mock)

        self.msp_mock.add_ellipse.assert_called_once_with((10, 90), (0, 10), 0.5, -1/2 * pi, 3 / 2 * pi)
        self.msp_mock.reset_mock()

        # rotated ellipse with x as mayor axis
        cx = "1"; cy = "-1"; rx = "1"; ry = "0.5"
        transformation = "rotate(90)"

        rotated_ellipse_mayor_x = Ellipse(cx, cy, rx, ry, transformation, 0, 0, 6 / 5 * pi, 8 / 5 * pi)
        rotated_ellipse_mayor_x.draw_dxf_ellipse(self.msp_mock)

        self.msp_mock.add_ellipse.assert_called_once_with((1, -1), (0, -1), 0.5, 6 / 5 * pi, 8 / 5 * pi)
        self.msp_mock.reset_mock()

        # rotated ellipse with y as mayor axis
        # to do some more testing, changed cx, cy
        transformation = "rotate(-90)"
        rotated_ellipse_mayor_y = Ellipse(cy, cx, ry, 2 * float(rx), transformation,
                                          0, 0, 6 / 5 * pi, 8 / 5 * pi)
        rotated_ellipse_mayor_y.draw_dxf_ellipse(self.msp_mock)

        self.msp_mock.add_ellipse.assert_called_once_with((1, -1), (-2, 0), 0.25,
                                                          6 / 5 * pi - 1 / 2 * pi, 8 / 5 * pi - 1 / 2 * pi)
        self.msp_mock.reset_mock()
