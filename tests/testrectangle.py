import unittest

from typing_extensions import override

from src.shapes.rectangle import (Rectangle, export_rotation, ensure_applicable_radius,
                                  rotate_clockwise_around_svg_origin)
from src.utilities import change_svg_to_dxf_coordinate
from unittest.mock import Mock

class TestRectangle(unittest.TestCase):

    def setUp(self):
        self.height = 100
        self.msp_mock = Mock()

    def test_basic_initialization(self):
        x = "10"; y = "10"; width = "100"; rect_height = "50"
        transformation = None; rx = None; ry = None; rot_angle = 0
        basic_rect = Rectangle(x, y, width, rect_height, transformation, rx, ry, self.height, rot_angle)
        self.assertEqual(basic_rect.x, float(x))
        self.assertEqual(basic_rect.y, change_svg_to_dxf_coordinate(float(y), self.height))
        self.assertEqual(basic_rect.width, float(width))
        self.assertEqual(basic_rect.rect_height, (-1) * float(rect_height))
        self.assertEqual(basic_rect.transformation, None)
        self.assertEqual(basic_rect.rx, 0)
        self.assertEqual(basic_rect.ry, 0)
        self.assertEqual(basic_rect.rot_angle, 0)

    def test_rotated_rectangle(self):
        width = "30.882156"
        rect_height = "32.285889"
        x = "140.85437"
        y = "53.877674"
        transform = "rotate(42.699784)"
        rx = None; ry = None

        rotated_rect = Rectangle(x, y, width, rect_height, transform, rx, ry, self.height)

        self.assertEqual(rotated_rect.rot_angle, 42.699784)

    def test_rounded_rectangle(self):
        width = "30.882156"
        rect_height = "32.285889"
        x = "140.85437"
        y = "53.877674"
        transform = None
        rx = "5"
        ry = "7"

        rounded_rect = Rectangle(x, y, width, rect_height, transform, rx, ry, self.height)

        self.assertEqual(rounded_rect.rx, float(rx))
        self.assertEqual(rounded_rect.ry, float(ry))

    def test_export_rotation(self):
        normal_rotation = "rotate(42.699784)"
        self.assertEqual(export_rotation(normal_rotation), 42.699784)

        non_rotation = "translation(40)"
        self.assertEqual(export_rotation(non_rotation), 0)

    def test_ensure_applicable_radius(self):
        width = 100
        applicable_r = 49
        self.assertEqual(ensure_applicable_radius(applicable_r, width), applicable_r)

        non_applicable_r = 75
        self.assertEqual(ensure_applicable_radius(non_applicable_r, width), width / 2)

    def test_clockwise_rotation_around_svg_origin(self):
        x = 1
        y = 0
        height = 0

        # rotation around origin (height = 0), clockwise
        rot_angle = 90
        self.assertEqual(rotate_clockwise_around_svg_origin(x, y, rot_angle, height), (0,-1))

        # rotation around origin (height = 0), counterclockwise
        rot_angle = -90
        self.assertEqual(rotate_clockwise_around_svg_origin(x, y, rot_angle, height), (0,1))

        # no rotation
        rot_angle = 0
        self.assertEqual(rotate_clockwise_around_svg_origin(x, y, rot_angle, height), (1, 0))

        # "decimal rotation" (test rounding)
        x = 0.3
        y = 0.25
        rot_angle = 22
        self.assertEqual(rotate_clockwise_around_svg_origin(x, y, rot_angle, height), (0.37181, 0.11941))

    def test_draw_dxf_rect_basic(self):
        """Test drawing a rectangle without rounded corners"""
        rect = Rectangle(10, 20, 50, 30, None, 0, 0, self.height)
        rect.draw_dxf_rect(self.msp_mock, self.height)

        # Check if a polyline was added
        self.msp_mock.add_lwpolyline.assert_called_once_with([(10,80), (60, 80), (60,50), (10, 50)], close = True)

    def test_draw_dxf_rect_rotated(self):
        rect = Rectangle(0,0, 100, 100, "rotate(90)", 0, 0, self.height)
        rect.draw_dxf_rect(self.msp_mock, self.height)

        self.msp_mock.add_lwpolyline.assert_called_once_with([(0, 100), (0,0), (-100, 0), (-100, 100)], close = True)

    def test_draw_rounded_rectangle(self):
        # rx == 0. ry == 0 --> line, ellipse not called
        edgy_rect = Rectangle(10, 20, 70, 50, None,
                                   rx = 0, ry = 0, height = self.height)
        edgy_rect.draw_dxf_rect(self.msp_mock, self.height)
        self.msp_mock.add_line.assert_not_called()

        # rx != 0, ry == 0
        rx_rounded_rect = Rectangle(10, 20, 70, 50, None,
                              rx=4, ry=0, height=self.height)
        rx_rounded_rect.draw_dxf_rect(self.msp_mock, self.height)
        self.msp_mock.add_lwpolyline_assert_not_called()
        self.assertTrue(self.msp_mock.add_line.call_count == 4)
        self.assertTrue(self.msp_mock.add_ellipse.call_count == 4)
        self.msp_mock.reset_mock()

        # rx == 0, ry != 0
        ry_rounded_rect = Rectangle(10, 20, 70, 50, None,
                                    rx=0, ry=4, height=self.height)
        ry_rounded_rect.draw_dxf_rect(self.msp_mock, self.height)
        self.msp_mock.add_lwpolyline_assert_not_called()
        self.assertTrue(self.msp_mock.add_line.call_count == 4)
        self.assertTrue(self.msp_mock.add_ellipse.call_count == 4)
        self.msp_mock.reset_mock()

        # rx != 0, ry != 0
        rounded_rect = Rectangle(10, 20, 70, 50, None,
                                    rx=4, ry=4, height=self.height)
        rounded_rect.draw_dxf_rect(self.msp_mock, self.height)
        self.msp_mock.add_lwpolyline_assert_not_called()
        self.assertTrue(self.msp_mock.add_line.call_count == 4)
        self.assertTrue(self.msp_mock.add_ellipse.call_count == 4)
        self.msp_mock.reset_mock()

if __name__ == "__main__":
    unittest.main()