import unittest

from src.shapes.circle import Circle
from src.svg_shapes import SvgCircle
from src.utilities import change_svg_to_dxf_coordinate
from unittest.mock import Mock


class TestCircle(unittest.TestCase):
    def setUp(self):
        self.svg_height = 300
        circle = {'cx': "35.732212", 'cy': "36.116428", 'r': "20"}
        self.svg_circle = SvgCircle(circle, self.svg_height)

    def test_initialization(self):
        circle = Circle(self.svg_circle)
        self.assertEqual(circle.center, (35.732212, change_svg_to_dxf_coordinate(36.116428, self.svg_height)))
        self.assertEqual(circle.radius, 20)

    def test_draw_dxf_circle(self):
        circle = Circle(self.svg_circle)

        mock_msp = Mock()

        circle.draw_dxf_circle(mock_msp)

        mock_msp.add_circle.assert_called_once_with(circle.center, circle.radius)


if __name__ == "__main__":
    unittest.main()