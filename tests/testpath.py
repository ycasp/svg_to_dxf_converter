import math
import unittest
from src.shapes.path import Path, draw_circular_arc, draw_rotated_elliptic_arc
from unittest.mock import Mock

from src.utilities import change_svg_to_dxf_coordinate


class TestPath(unittest.TestCase):
    def setUp(self):
        self.msp_mock = Mock()

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

        self.msp_mock.add_ellipse.assert_called_once_with(center = center, mayor_axis = (0, 120), ratio = 0.75,
                                                          start_param = -4.552741283791109, end_param = -3.0174462409750467)
        self.msp_mock.reset_mock()

        # 45 1 0
        center = (202.4933858267454, change_svg_to_dxf_coordinate(97.506614173254576, height))

        draw_rotated_elliptic_arc(center=center, rx=rx, ry=ry, theta=141.7830767038384, delta=-103.5661534076767,
                                  rotation=45, sweep=False, msp=self.msp_mock)

        self.msp_mock.add_ellipse.assert_called_once_with(center=center, mayor_axis=(84.85281, 84.85281), ratio=0.75,
                                                          start_param=-4.045377838884546, end_param=-2.237807468295042)
        self.msp_mock.reset_mock()

        # 0 1 1
        center = (188.85550154096586,  change_svg_to_dxf_coordinate(80.92355281606069, height))

        draw_rotated_elliptic_arc(center=center, rx=rx, ry=ry, theta=170.8528607762027, delta=-87.965926260717367,
                                  rotation=0, sweep=True, msp=self.msp_mock)

        self.msp_mock.add_ellipse.assert_called_once_with(center=center, mayor_axis=(0, 120), ratio=0.75,
                                                          start_param=-3.0174462409750467, end_param=-4.552741283791109)
        self.msp_mock.reset_mock()

        # 136 0 1
        center = (200.7225476499036, change_svg_to_dxf_coordinate(97.882028678524563, height))

        draw_rotated_elliptic_arc(center=center, rx=rx, ry=ry, theta=34.775926232869779, delta=-72.218308575467063,
            rotation=136, sweep=True, msp=self.msp_mock)

        self.msp_mock.add_ellipse.assert_called_once_with(center=center, mayor_axis=(83.35900, -86.32078), ratio=0.75,
                                                          start_param=-0.9173034751259864, end_param=-2.1777507399891425)
        self.msp_mock.reset_mock()



