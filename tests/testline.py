import unittest

from src.shapes.line import Line
from src.utilities import change_svg_to_dxf_coordinate
from unittest.mock import Mock


class TestLine(unittest.TestCase):

    def test_initialization(self):
        """Test that the Line object initializes correctly."""
        height = 100
        line = Line(10, 20, 30, 40, height)
        self.assertEqual(line.start, (10.0, change_svg_to_dxf_coordinate(20.0, height)))
        self.assertEqual(line.end, (30.0, change_svg_to_dxf_coordinate(40.0, height)))

    def test_zero_length_line(self):
        """Test a line where start and end points are the same."""
        height = 100
        line = Line(50, 50, 50, 50, height)
        self.assertEqual(line.start, line.end)

    def test_negative_coordinates(self):
        """Test that negative coordinates are handled correctly."""
        height = 100
        line = Line(-10, -20, -30, -40, height)
        self.assertEqual(line.start, (-10.0, change_svg_to_dxf_coordinate(-20.0, height)))
        self.assertEqual(line.end, (-30.0, change_svg_to_dxf_coordinate(-40.0, height)))

    def test_large_coordinates(self):
        """Test with very large coordinate values."""
        height = 100
        line = Line(1e6, 1e6, -1e6, -1e6, height)
        self.assertEqual(line.start, (1e6, change_svg_to_dxf_coordinate(1e6, height)))
        self.assertEqual(line.end, (-1e6, change_svg_to_dxf_coordinate(-1e6, height)))

    def test_draw_dxf_line(self):
        """Test that draw_dxf_line calls add_line with correct parameters."""
        height = 100
        line = Line(10, 20, 30, 40, height)

        # Mock the DXF modelspace object
        mock_msp = Mock()
        line.draw_dxf_line(mock_msp)

        # Assert that add_line was called with correct coordinates
        mock_msp.add_line.assert_called_once_with(line.start, line.end)


if __name__ == "__main__":
    unittest.main()