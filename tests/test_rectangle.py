import unittest
from unittest.mock import Mock

from src.shapes.rectangle import Rectangle
from src.svg_shapes import SvgRectangle


class TestRectangle(unittest.TestCase):

    def setUp(self):
        self.height = 100
        self.msp_mock = Mock()

        element_basic_rect = {'x': 10, 'y': 10, 'width': 100, 'height': 50}
        self.svg_basic_rect = SvgRectangle(element_basic_rect, self.height)

        element_rotated_rect = {'x': 0, 'y': 0, 'width': 100, 'height': 100, 'transform': "rotate(90)"}
        self.svg_rotated_rect = SvgRectangle(element_rotated_rect, self.height)

        element_rounded_rect = {'x': 10, 'y': 10, 'width': 100, 'height': 50, 'transform': "rotate(45)",
            'rx': 9, 'ry': 7}
        self.svg_rounded_rect = SvgRectangle(element_rounded_rect, self.height)

    def test_basic_initialization(self):
        basic_rect = Rectangle(self.svg_basic_rect)
        self.assertEqual(basic_rect.x, 10)
        self.assertEqual(basic_rect.y, 90)
        self.assertEqual(basic_rect.rect_width, (100, 0))
        self.assertEqual(basic_rect.rect_height, (0, (-1) * 50))
        self.assertEqual(basic_rect.rx, (0, 0))
        self.assertEqual(basic_rect.ry, (0, 0))

    def test_rotated_rectangle(self):
        rotated_rect = Rectangle(self.svg_rotated_rect)
        self.assertEqual(rotated_rect.x, 0)
        self.assertEqual(rotated_rect.y, 100)
        self.assertEqual(rotated_rect.rect_width, (0, -100))
        self.assertEqual(rotated_rect.rect_height, (-100, 0))
        self.assertEqual(rotated_rect.rx, (0, 0))
        self.assertEqual(rotated_rect.ry, (0, 0))

    def test_rounded_rectangle(self):
        rounded_rect = Rectangle(self.svg_rounded_rect)

        self.assertEqual(rounded_rect.rx, (6.36396, -6.36396))
        self.assertEqual(rounded_rect.ry, (4.94975, 4.94975))

    def test_draw_dxf_rect_basic(self):
        """Test drawing a rectangle without rounded corners"""
        rect = Rectangle(self.svg_basic_rect)
        rect.draw_dxf_rect(self.msp_mock, self.height)
        # Check if a polyline was added
        self.msp_mock.add_lwpolyline.assert_called_once_with([(10, 90), (110, 90), (110, 40), (10, 40)], close=True)

    def test_draw_dxf_rect_rotated(self):
        rect = Rectangle(self.svg_rotated_rect)
        rect.draw_dxf_rect(self.msp_mock, self.height)

        self.msp_mock.add_lwpolyline.assert_called_once_with([(0, 100), (0, 0), (-100, 0), (-100, 100)], close=True)

    def test_draw_rounded_rectangle(self):
        # rx == 0. ry == 0 --> line, ellipse not called
        edgy_rect = Rectangle(self.svg_basic_rect)
        edgy_rect.draw_dxf_rect(self.msp_mock, self.height)
        self.msp_mock.add_line.assert_not_called()

        # rx != 0, ry == 0
        element_rounded_rect = {'x': 10, 'y': 20, 'width': 70, 'height': 50, 'transform': None,
            'rx': 4, 'ry': 0}
        svg_rounded_rect_rx = SvgRectangle(element_rounded_rect, self.height)
        rx_rounded_rect = Rectangle(svg_rounded_rect_rx)
        rx_rounded_rect.draw_dxf_rect(self.msp_mock, self.height)
        self.msp_mock.add_lwpolyline_assert_not_called()
        self.assertTrue(self.msp_mock.add_line.call_count == 4)
        self.assertTrue(self.msp_mock.add_ellipse.call_count == 4)
        self.msp_mock.reset_mock()

        # rx == 0, ry != 0
        element_rounded_rect = {'x': 10, 'y': 20, 'width': 70, 'height': 50, 'transform': None,
            'rx': 0, 'ry': 4}
        svg_rounded_rect_ry = SvgRectangle(element_rounded_rect, self.height)
        ry_rounded_rect = Rectangle(svg_rounded_rect_ry)
        ry_rounded_rect.draw_dxf_rect(self.msp_mock, self.height)
        self.msp_mock.add_lwpolyline_assert_not_called()
        self.assertTrue(self.msp_mock.add_line.call_count == 4)
        self.assertTrue(self.msp_mock.add_ellipse.call_count == 4)
        self.msp_mock.reset_mock()

        # rx != 0, ry != 0
        element_rounded_rect = {'x': 10, 'y': 20, 'width': 70, 'height': 50, 'transform': None,
            'rx': 8, 'ry': 4}
        svg_rounded_rect = SvgRectangle(element_rounded_rect, self.height)
        rounded_rect = Rectangle(svg_rounded_rect)
        rounded_rect.draw_dxf_rect(self.msp_mock, self.height)
        self.msp_mock.add_lwpolyline_assert_not_called()
        self.assertTrue(self.msp_mock.add_line.call_count == 4)
        self.assertTrue(self.msp_mock.add_ellipse.call_count == 4)
        self.msp_mock.reset_mock()


if __name__ == "__main__":
    unittest.main()
