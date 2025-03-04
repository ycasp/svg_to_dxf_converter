import unittest

from src.shapes.line import Line
from src.svg_shapes import SvgLine
from src.utilities import change_svg_to_dxf_coordinate
from unittest.mock import Mock


class TestLine(unittest.TestCase):
    def setUp(self):
        self.svg_height = 100

        element_basic_line = {'x1': 10, 'y1': 20, 'x2': 30, 'y2': 40}
        self.basic_line = SvgLine(element_basic_line, self.svg_height)

        element_zero_length_line = {'x1': 50, 'y1': 50, 'x2': 50, 'y2': 50}
        self.zero_length_line = SvgLine(element_zero_length_line, self.svg_height)

        element_large_line = {'x1': 1e6, 'y1': 1e6, 'x2': -1e6, 'y2': -1e6}
        self.large_line = SvgLine(element_large_line, self.svg_height)

        element_negative_line = {'x1': -10, 'y1': -20, 'x2': -30, 'y2': -40}
        self.negative_line = SvgLine(element_negative_line, self.svg_height)


    def test_initialization(self):
        """Test that the Line object initializes correctly."""
        line = Line(self.basic_line)
        self.assertEqual(line.start, (10.0, change_svg_to_dxf_coordinate(20.0, self.svg_height)))
        self.assertEqual(line.end, (30.0, change_svg_to_dxf_coordinate(40.0, self.svg_height)))

    def test_zero_length_line(self):
        """Test a line where start and end points are the same."""
        line = Line(self.zero_length_line)
        self.assertEqual(line.start, line.end)

    def test_negative_coordinates(self):
        """Test that negative coordinates are handled correctly."""
        line = Line(self.negative_line)
        self.assertEqual(line.start, (-10.0, change_svg_to_dxf_coordinate(-20.0, self.svg_height)))
        self.assertEqual(line.end, (-30.0, change_svg_to_dxf_coordinate(-40.0, self.svg_height)))

    def test_large_coordinates(self):
        """Test with very large coordinate values."""
        line = Line(self.large_line)
        self.assertEqual(line.start, (1e6, change_svg_to_dxf_coordinate(1e6, self.svg_height)))
        self.assertEqual(line.end, (-1e6, change_svg_to_dxf_coordinate(-1e6, self.svg_height)))

    def test_draw_dxf_line(self):
        """Test that draw_dxf_line calls add_line with correct parameters."""
        line = Line(self.basic_line)

        # Mock the DXF modelspace object
        mock_msp = Mock()
        line.draw_dxf_line(mock_msp)

        # Assert that add_line was called with correct coordinates
        mock_msp.add_line.assert_called_once_with(line.start, line.end)


if __name__ == "__main__":
    unittest.main()