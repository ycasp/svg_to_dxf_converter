import math

from ezdxf.path import from_vertices, render_splines_and_polylines
from svgpathtools import parse_path
from svgpathtools.path import CubicBezier, QuadraticBezier, Arc
from svgpathtools.path import Line as svgLine
from src.logging_config import setup_logger
from src.utilities import change_svg_to_dxf_coordinate, rad_to_degree, \
    rotate_clockwise_around_cartesian_origin

path_logger = setup_logger(__name__)

class Path:
    """
    Represents a path of a svg file.

    Attributes
       path (string): The path of a svg file.
    """
    # constants for polyline approximation of Bézier curves
    MAX_DISTANCE = 0.1  # maximal distance to the original Bézier curve
    MIN_SEGMENTS = 3  # minimal segments a Bézier curve is split into

    # constant for spline approx of Bézier curves
    G1_TOL = 1e-2

    def __init__(self, path):
        """
        Initializes the path object.
        :param path: string with the path attributes (points, path type)
        """
        self.path = path

    def draw_svg_path(self, msp, height):
        """
        Adds the path to a dxf file.
        It splits the path into its parts and adds/converts the corresponding type to the dxf file.
        Bézier curves are approximated.

        :param msp: Modelspace of the dxf file, to add the entities.
        :param height: Height of the svg file, to transform the svg coordinates to dxf coordinates
        :return: -
        """
        parsed_path = parse_path(self.path)

        for segment in parsed_path:
            if isinstance(segment, svgLine):
                # Add a LINE for SVG Line segment
                msp.add_line(start=(segment.start.real, change_svg_to_dxf_coordinate(segment.start.imag, height)),
                             end=(segment.end.real, change_svg_to_dxf_coordinate(segment.end.imag, height)))
            elif isinstance(segment, CubicBezier):
                # Approximate Cubic Bézier curve with a polyline
                approximate_cubic_bezier_curve(segment, msp, height)
            elif isinstance(segment, QuadraticBezier):
                # Approximate Quadratic Bézier curve with a polyline
                approximate_quadratic_bezier_curve(segment, msp, height)
            elif isinstance(segment, Arc):
                # Add an ARC for SVG Arc segment

                if segment.radius.real == segment.radius.imag:
                    center = (segment.center.real, change_svg_to_dxf_coordinate(segment.center.imag, height))
                    start_point = (segment.start.real, change_svg_to_dxf_coordinate(segment.start.imag, height))
                    end_point = (segment.end.real, change_svg_to_dxf_coordinate(segment.end.imag, height))
                    radius = segment.radius.real
                    sweep = segment.sweep
                    draw_circular_arc(center, start_point, end_point, radius, sweep, msp)
                else:
                    center = (segment.center.real, change_svg_to_dxf_coordinate(segment.center.imag, height))
                    rx = segment.radius.real
                    ry = segment.radius.imag
                    draw_rotated_elliptic_arc(center, rx, ry, segment.theta, segment.delta,
                                              segment.rotation, segment.sweep, msp)

            else:
                path_logger.warning("unsupported path segment: {}".format(segment))


def approximate_cubic_bezier_curve(segment, msp, height):
    """
    Approximates a cubic Bézier curve and adds it to the modelspace of the dxf file.

    :param segment: path segment, describing the Bézier curve with two control points, start and endpoint.
    :param msp: modelspace, where the curve is added, i.e. the approximation of the curve
    :param height: height for transformation to cartesian coordinates
    :return: -
    """

    dxf_path = from_vertices([(0, 0)])
    dxf_path.move_to((segment.start.real, change_svg_to_dxf_coordinate(segment.start.imag, height)))

    dxf_path.curve4_to((segment.end.real, change_svg_to_dxf_coordinate(segment.end.imag, height)),
                       (segment.control1.real, change_svg_to_dxf_coordinate(segment.control1.imag, height)),
                       (segment.control2.real, change_svg_to_dxf_coordinate(segment.control2.imag, height)))

    # render_lines(msp, [dxf_path], distance = Path.MAX_DISTANCE, segments = Path.MIN_SEGMENTS)

    render_splines_and_polylines(msp, [dxf_path])


def approximate_quadratic_bezier_curve(segment, msp, height):
    """
    Approximates a quadratic Bézier curve and adds it to the modelspace of the dxf file.

    :param segment: path segment, describing the Bézier curve with one control points, start and endpoint.
    :param msp: modelspace, where the curve is added, i.e. the approximation of the curve
    :param height: height for transformation to cartesian coordinates
    :return: -
    """
    dxf_path = from_vertices([(0, 0)])
    dxf_path.move_to((segment.start.real, change_svg_to_dxf_coordinate(segment.start.imag, height)))

    dxf_path.curve3_to((segment.end.real, change_svg_to_dxf_coordinate(segment.end.imag, height)),
                       (segment.control.real, change_svg_to_dxf_coordinate(segment.control.imag, height)))

    # render_lines(msp, [dxf_path], distance = Path.MAX_DISTANCE, segments = Path.MIN_SEGMENTS)

    render_splines_and_polylines(msp, [dxf_path])


def draw_circular_arc(center, start_point, end_point, radius, sweep, msp):
    """
    draws a circular arc (rx = ry in path) to the Modelspace.

    :param center: (cx, cy), center of the arc, already in cartesian coordinates
    :param start_point: (sx, sy), start point of the arc, already in cartesian coordinates
    :param end_point: (ex, ey), endpoint of the arc, already in cartesian coordinates
    :param radius: radius of the arc (rx = ry as circular arc)
    :param sweep: (boolean), gives orientation of the arc (counterclockwise: sweep = false, clockwise: sweep = false)
    :param msp: modelspace of dxf file the arc should be written to
    :return: -
    """
    # calculate the vectors from center to start/endpoint
    start_point_vec = (start_point[0] - center[0],
    start_point[1] - center[1])
    end_point_vec = (end_point[0] - center[0],
    end_point[1] - center[1])

    # calculate angle between x-axis and vec from center to start/endpoint
    start_angle_rad = math.atan2(start_point_vec[1], start_point_vec[0])
    end_angle_rad = math.atan2(end_point_vec[1], end_point_vec[0])
    # transform the angles to degree (add_arc takes degree not radian)
    start_angle = rad_to_degree(start_angle_rad)
    end_angle = rad_to_degree(end_angle_rad)

    # default is ccl == true, svg works otherwise (default ccl == false) --> thus not sweep
    msp.add_arc(center=center, radius=radius, start_angle=start_angle, end_angle=end_angle,
                is_counter_clockwise=not sweep)


def draw_rotated_elliptic_arc(center, rx, ry, theta, delta, rotation, sweep, msp):
    start_angle = math.radians((-1) * theta)
    end_angle = math.radians((-1) * theta + (-1) * delta)

    if sweep:
        start_angle, end_angle = end_angle, start_angle

    rotated_rx = rotate_clockwise_around_cartesian_origin(rx, 0, rotation)
    rotated_ry = rotate_clockwise_around_cartesian_origin(0, ry, rotation)

    if rx >= ry:
        mayor_axis = rotated_rx
        ratio = ry / rx
    else:
        mayor_axis = rotated_ry
        ratio = rx / ry
        start_angle = start_angle - math.pi / 2
        end_angle = end_angle - math.pi / 2

    msp.add_ellipse(center=center, major_axis=mayor_axis, ratio=ratio, start_param=start_angle, end_param=end_angle)
