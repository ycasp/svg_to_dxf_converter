import unittest


from src.shapes.polygon import Polygon
from src.utilities import change_svg_to_dxf_coordinate
from unittest.mock import Mock

class TestPolygon(unittest.TestCase):

    def test_initialization(self):
        height = 100
        points = "0,0 10,10 20,40 20,-40 10,-10, 0,0"

        manual_points = [(0, change_svg_to_dxf_coordinate(0, height)),
                         (10, change_svg_to_dxf_coordinate(10, height)),
                         (20, change_svg_to_dxf_coordinate(40, height)),
                         (20, change_svg_to_dxf_coordinate(-40, height)),
                         (10, change_svg_to_dxf_coordinate(-10, height)),
                         (0, change_svg_to_dxf_coordinate(0, height))]

        polygon = Polygon(points, height)

        self.assertEqual(polygon.points_list, manual_points)

    def test_empty_points(self):
        height = 100
        points = ""

        empty_polygon = Polygon(points, height)

        self.assertEqual(empty_polygon.points_list, [])


    def test_draw_dxf_polygon(self):
        height = 100
        points = "0,0 10,10 20,40 20,-40 10,-10, 0,0"
        polygon = Polygon(points, height)

        mock_msp = Mock()

        polygon.draw_dxf_polygon(mock_msp)

        mock_msp.add_lwpolyline.assert_called_once_with(polygon.points_list, close = True)


if __name__ == "__main__":
    unittest.main()