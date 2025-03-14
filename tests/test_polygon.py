import unittest
from unittest.mock import Mock

from src.shapes.polygon import Polygon
from src.svg_shapes import SvgPolygon
from src.utilities import change_svg_to_dxf_coordinate


class TestPolygon(unittest.TestCase):
    def setUp(self):
        self.svg_height = 100

        element_points = {'points': "0,0 10,10 20,40 20,-40 10,-10, 0,0"}
        self.svg_polygon = SvgPolygon(element_points, self.svg_height)

        element_empty_points = {'points': ""}
        self.svg_empty_polygon = SvgPolygon(element_empty_points, self.svg_height)

    def test_initialization(self):
        manual_points = [(0, change_svg_to_dxf_coordinate(0, self.svg_height)),
            (10, change_svg_to_dxf_coordinate(10, self.svg_height)),
            (20, change_svg_to_dxf_coordinate(40, self.svg_height)),
            (20, change_svg_to_dxf_coordinate(-40, self.svg_height)),
            (10, change_svg_to_dxf_coordinate(-10, self.svg_height)),
            (0, change_svg_to_dxf_coordinate(0, self.svg_height))]

        polygon = Polygon(self.svg_polygon)

        self.assertEqual(polygon.points_list, manual_points)

    def test_empty_points(self):
        empty_polygon = Polygon(self.svg_empty_polygon)

        self.assertEqual(empty_polygon.points_list, [])

    def test_draw_dxf_polygon(self):
        polygon = Polygon(self.svg_polygon)

        mock_msp = Mock()

        polygon.draw_dxf_polygon(mock_msp)

        mock_msp.add_lwpolyline.assert_called_once_with(polygon.points_list, close=True)


if __name__ == "__main__":
    unittest.main()
