import unittest

from src.shapes.circle import Circle
from src.utilities import change_svg_to_dxf_coordinate
from unittest.mock import Mock


class TestCircle(unittest.TestCase):

    def test_initialization(self):
        height = 300
        cx = "35.732212"
        cy = "36.116428"
        r = "20"
        circle = Circle(cx, cy, r, height)
        self.assertEqual(circle.center, (float(cx), change_svg_to_dxf_coordinate(float(cy), height)))
        self.assertEqual(circle.radius, float(r))

    def test_wrong_center_initialization(self):
        height = 300
        cx = "35.732212"
        cy = "36.116428"
        r = "20"
        circle_wrong_center = Circle(cy, cx, r, height)
        self.assertNotEqual(circle_wrong_center.center, (float(cx), change_svg_to_dxf_coordinate(float(cy), height)))
        self.assertEqual(circle_wrong_center.radius, float(r))

    def test_draw_dxf_circle(self):
        height = 300
        circle = Circle(35.732212, 36.116428, 20, height)

        mock_msp = Mock()

        circle.draw_dxf_circle(mock_msp)

        mock_msp.add_circle.assert_called_once_with(circle.center, circle.radius)


if __name__ == "__main__":
    unittest.main()