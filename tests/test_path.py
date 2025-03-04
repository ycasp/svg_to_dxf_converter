import math
import unittest
from unittest.mock import Mock, MagicMock, patch
from src.shapes.path import Path, draw_circular_arc, draw_rotated_elliptic_arc, approximate_cubic_bezier_curve, \
    approximate_quadratic_bezier_curve
from svgpathtools import parse_path

from src.svg_shapes import SvgPath
from src.utilities import change_svg_to_dxf_coordinate


class TestPath(unittest.TestCase):
    def setUp(self):
        self.svg_height = 500
        self.msp_mock = Mock()
        self.mock_from_vertices = MagicMock(return_value=MagicMock())

        element_path = {'d': "M 50,250 L 150,50 C 200,150 300,150 350,50 Q 400,0 450,50 A 50,25 45 1 1 400,150 "
                "L 300,250 C 250,350 150,350 100,250 Q 75,200 50,250 Z"}

        self.svg_test_path = SvgPath(element_path, 0)

        element_complicated_path = {'d': "M 50,250 L 150,50 C 200,150 300,150 350,50 Q 400,0 450,50 A 50,25 45 1 1 400,150 "
                "L 300,250 C 250,350 150,350 100,250 Q 75,200 50,250 A 50,50 0 1 1 150,250 Z"}
        self.svg_complicated_path = SvgPath(element_complicated_path, self.svg_height)

    def test_initialization(self):
        test_path = Path(self.svg_test_path)

        self.assertEqual(test_path.path, "M 50,250 L 150,50 C 200,150 300,150 350,50 Q 400,0 450,50 A 50,25 45 1 1 400,150 "
                "L 300,250 C 250,350 150,350 100,250 Q 75,200 50,250 Z")

    @patch("src.shapes.path.approximate_cubic_bezier_curve")
    @patch("src.shapes.path.approximate_quadratic_bezier_curve")
    @patch("src.shapes.path.draw_rotated_elliptic_arc")
    @patch("src.shapes.path.draw_circular_arc")
    def test_draw_svg_path(self, mock_circular_arc, mock_elliptic_arc, mock_approx_quadratic, mock_approx_cubic):

        test_path = Path(self.svg_complicated_path)

        test_path.draw_svg_path(self.msp_mock, self.svg_height)

        assert self.msp_mock.add_line.call_count == 3

        assert mock_approx_cubic.call_count == 2

        assert mock_approx_quadratic.call_count == 2

        assert mock_elliptic_arc.call_count == 1

        assert mock_circular_arc.call_count == 1



    def test_draw_circular_arc(self):
        center = (0, 0)
        radius = 1

        draw_circular_arc(center, start_point = (1,0), end_point = (-1,0),
                          radius = radius, sweep = False, msp = self.msp_mock)

        self.msp_mock.add_arc.assert_called_once_with(center = center, radius = radius,
                                                      start_angle = 0, end_angle = 180, is_counter_clockwise = True)
        self.msp_mock.reset_mock()

        draw_circular_arc(center, start_point=(math.sqrt(2) / 2, math.sqrt(2) / 2),
                          end_point=(-math.sqrt(2) / 2, -math.sqrt(2) / 2),
                          radius=radius, sweep=False, msp=self.msp_mock)

        self.msp_mock.add_arc.assert_called_once_with(center=center, radius=radius,
                                                      start_angle=45, end_angle=-135, is_counter_clockwise=True)
        self.msp_mock.reset_mock()

        draw_circular_arc(center, start_point=(math.sqrt(2) / 2, -math.sqrt(2) / 2),
                          end_point=(-math.sqrt(2) / 2, math.sqrt(2) / 2),
                          radius=radius, sweep=True, msp=self.msp_mock)

        self.msp_mock.add_arc.assert_called_once_with(center=center, radius=radius,
                                                      start_angle=-45, end_angle=135, is_counter_clockwise=False)
        self.msp_mock.reset_mock()

        draw_circular_arc(center, start_point=(math.sqrt(2) / 2, math.sqrt(2) / 2),
                          end_point=(-math.sqrt(2) / 2, math.sqrt(2) / 2),
                          radius=radius, sweep=False, msp=self.msp_mock)

        self.msp_mock.add_arc.assert_called_once_with(center=center, radius=radius,
                                                      start_angle=45, end_angle=135, is_counter_clockwise=True)
        self.msp_mock.reset_mock()

        draw_circular_arc(center, start_point=(-math.sqrt(2) / 2, -math.sqrt(2) / 2),
                          end_point=(math.sqrt(2) / 2, -math.sqrt(2) / 2),
                          radius=radius, sweep=False, msp=self.msp_mock)

        self.msp_mock.add_arc.assert_called_once_with(center=center, radius=radius,
                                                      start_angle=-135, end_angle=-45, is_counter_clockwise=True)
        self.msp_mock.reset_mock()

        draw_circular_arc(center, start_point=(math.sqrt(2) / 2, math.sqrt(2) / 2),
                          end_point=(math.sqrt(2) / 2, -math.sqrt(2) / 2),
                          radius=radius, sweep=False, msp=self.msp_mock)

        self.msp_mock.add_arc.assert_called_once_with(center=center, radius=radius,
                                                      start_angle=45, end_angle=-45, is_counter_clockwise=True)

        self.msp_mock.reset_mock()

        draw_circular_arc(center, start_point=(-math.sqrt(2) / 2, math.sqrt(2) / 2),
                          end_point=(-math.sqrt(2) / 2, -math.sqrt(2) / 2),
                          radius=radius, sweep=False, msp=self.msp_mock)

        self.msp_mock.add_arc.assert_called_once_with(center=center, radius=radius,
                                                      start_angle=135, end_angle=-135, is_counter_clockwise=True)

    def test_draw_elliptic_arc(self):
        height = 400
        rx = 90; ry = 120

        # 0 0 0
        center = (188.85550154096586,  change_svg_to_dxf_coordinate(80.92355281606069, height))

        draw_rotated_elliptic_arc(center = center, rx = rx, ry = ry, theta = 170.8528607762027, delta = -87.965926260717367,
                                  rotation = 0, sweep = False, msp = self.msp_mock)

        self.msp_mock.add_ellipse.assert_called_once_with(center = center, major_axis = (0, 120), ratio = 0.75,
                                                          start_param = -4.552741283791109, end_param = -3.0174462409750467)
        self.msp_mock.reset_mock()

        # 45 1 0
        center = (202.4933858267454, change_svg_to_dxf_coordinate(97.506614173254576, height))

        draw_rotated_elliptic_arc(center=center, rx=rx, ry=ry, theta=141.7830767038384, delta=-103.5661534076767,
                                  rotation=45, sweep=False, msp=self.msp_mock)

        self.msp_mock.add_ellipse.assert_called_once_with(center=center, major_axis=(84.85281, 84.85281), ratio=0.75,
                                                          start_param=-4.045377838884546, end_param=-2.237807468295042)
        self.msp_mock.reset_mock()

        # 0 1 1
        center = (188.85550154096586,  change_svg_to_dxf_coordinate(80.92355281606069, height))

        draw_rotated_elliptic_arc(center=center, rx=rx, ry=ry, theta=170.8528607762027, delta=-87.965926260717367,
                                  rotation=0, sweep=True, msp=self.msp_mock)

        self.msp_mock.add_ellipse.assert_called_once_with(center=center, major_axis=(0, 120), ratio=0.75,
                                                          start_param=-3.0174462409750467, end_param=-4.552741283791109)
        self.msp_mock.reset_mock()

        # 136 0 1
        center = (200.7225476499036, change_svg_to_dxf_coordinate(97.882028678524563, height))

        draw_rotated_elliptic_arc(center=center, rx=rx, ry=ry, theta=34.775926232869779, delta=-72.218308575467063,
            rotation=136, sweep=True, msp=self.msp_mock)

        self.msp_mock.add_ellipse.assert_called_once_with(center=center, major_axis=(83.35900, -86.32078), ratio=0.75,
                                                          start_param=-0.9173034751259864, end_param=-2.1777507399891425)
        self.msp_mock.reset_mock()

        # ellipse with rx as mayor axis, 154 1 1
        rx = 145; ry = 78

        center = (266.2064880898378, change_svg_to_dxf_coordinate(101.3975340144844, height))

        draw_rotated_elliptic_arc(center=center, rx=rx, ry=ry, theta=-49.231602624334684, delta=-82.137486587315081,
                                  rotation=154, sweep=True, msp=self.msp_mock)

        self.msp_mock.add_ellipse.assert_called_once_with(center=center, major_axis=(-130.32514, -63.56382), ratio=0.5379310344827586,
                                                          start_param=2.2928231420894503,
                                                          end_param=0.8592535618281213)
        self.msp_mock.reset_mock()

    @patch("src.shapes.path.render_splines_and_polylines")
    @patch("src.shapes.path.from_vertices")
    def test_approximation_of_cubic_bezier_curves(self, mock_from_vertices, mock_render):
        mock_dxf_path = MagicMock()
        mock_from_vertices.return_value = mock_dxf_path

        height = 400
        path = "M 150.0,50.0 C 200.0,150.0 300.0,150.0 350.0,50.0"
        cubic_bezier_curve = parse_path(path)[0]
        approximate_cubic_bezier_curve(cubic_bezier_curve, self.msp_mock, height)

        mock_from_vertices.assert_called_once_with([(0,0)])

        mock_dxf_path.move_to.assert_called_once_with((150.0,350.0))

        mock_dxf_path.curve4_to.assert_called_once_with((350, 350), (200, 250), (300, 250))

        mock_render.assert_called_once_with(self.msp_mock, [mock_dxf_path])


    @patch("src.shapes.path.render_splines_and_polylines")
    @patch("src.shapes.path.from_vertices")
    def test_approximation_of_quadratic_bezier_curves(self, mock_from_vertices, mock_render):
        mock_dxf_path = MagicMock()
        mock_from_vertices.return_value = mock_dxf_path

        height = 400
        path = "M 150.0,50.0 Q 200.0,150.0 350.0,50.0"
        quadratic_bezier_curve = parse_path(path)[0]
        approximate_quadratic_bezier_curve(quadratic_bezier_curve, self.msp_mock, height)

        mock_from_vertices.assert_called_once_with([(0,0)])

        mock_dxf_path.move_to.assert_called_once_with((150.0,350.0))

        mock_dxf_path.curve3_to.assert_called_once_with((350, 350), (200, 250))

        mock_render.assert_called_once_with(self.msp_mock, [mock_dxf_path])