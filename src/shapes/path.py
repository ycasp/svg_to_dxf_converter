import math

from ezdxf.path import from_vertices, render_splines_and_polylines
from svgpathtools.path import CubicBezier, QuadraticBezier, Arc
from svgpathtools.path import Line as svgLine

from src.logging_config import setup_logger
from src.utilities import rad_to_degree, rotate_clockwise_around_cartesian_origin

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

    def __init__(self, svg_path):
        """
        Initializes the path object.
        :param svg_path: SvgPath, path to be transformed into dxf, already transformed and changed coordinates to cartesian coordinates
        """
        # extract the parsed_path (Path of svgpathtools)
        self.parsed_path = svg_path.parsed_path

    def draw_svg_path(self, msp):
        """
        Adds the path to a dxf file.
        It splits the path into its parts and adds/converts the corresponding type to the dxf file.
        Bézier curves are approximated.

        :param msp: Modelspace of the dxf file, to add the entities.
        :return: -
        """

        # iterate over path segments and add it to the model space
        for segment in self.parsed_path:
            if isinstance(segment, svgLine):
                # add line for Line
                msp.add_line(start=(segment.start.real, segment.start.imag),
                             end=(segment.end.real, segment.end.imag))
            elif isinstance(segment, CubicBezier):
                # approximate (and add) cubic Bézier curve with polyline
                approximate_cubic_bezier_curve(segment, msp)
            elif isinstance(segment, QuadraticBezier):
                # approximate (and add) quadratic Bézier curve with polyline
                approximate_quadratic_bezier_curve(segment, msp)
            elif isinstance(segment, Arc):
                # add arc segment --> via arc or via ellipse

                # determine if elliptic or circular arc
                if segment.radius.real == segment.radius.imag:  # if radius_x = radius_y --> elliptic arc
                    # extract values from segment
                    center = (segment.center.real, segment.center.imag)
                    start_point = (segment.start.real, segment.start.imag)
                    end_point = (segment.end.real, segment.end.imag)
                    radius = segment.radius.real
                    sweep = segment.sweep

                    # add the arc to the modelspace
                    draw_circular_arc(center, start_point, end_point, radius, sweep, msp)
                else:  # radius_x != radius_y --> elliptic arc
                    # extract values form segment
                    center = (segment.center.real, segment.center.imag)
                    rx = segment.radius.real
                    ry = segment.radius.imag
                    # add to model space
                    draw_rotated_elliptic_arc(center, rx, ry, segment.theta, segment.delta,
                                              segment.rotation, segment.sweep, msp)

            else:
                # unsupported segment type
                path_logger.warning("unsupported path segment: {}".format(segment))


def approximate_cubic_bezier_curve(segment, msp):
    """
    Approximates a cubic Bézier curve and adds it to the modelspace of the dxf file.

    :param segment: path segment, describing the Bézier curve with two control points, start and endpoint.
    :param msp: modelspace, where the curve is added, i.e. the approximation of the curve
    :return: -
    """

    # create a new path, move it to start point of cubic Bézier curve
    dxf_path = from_vertices([(0, 0)])
    dxf_path.move_to((segment.start.real, segment.start.imag))

    # convert the Bézier curve to spline
    dxf_path.curve4_to((segment.end.real, segment.end.imag),
                       (segment.control1.real, segment.control1.imag),
                       (segment.control2.real, segment.control2.imag))

    # add the spline to the model space
    render_splines_and_polylines(msp, [dxf_path])


def approximate_quadratic_bezier_curve(segment, msp):
    """
    Approximates a quadratic Bézier curve and adds it to the modelspace of the dxf file.

    :param segment: path segment, describing the Bézier curve with one control points, start and endpoint.
    :param msp: modelspace, where the curve is added, i.e. the approximation of the curve
    :return: -
    """

    # create a new path, move it to start point of quadratic Bézier curve
    dxf_path = from_vertices([(0, 0)])
    dxf_path.move_to((segment.start.real, segment.start.imag))

    # convert the Bézier curve to spline
    dxf_path.curve3_to((segment.end.real, segment.end.imag),
                       (segment.control.real, segment.control.imag))

    # add the spline to the model space
    render_splines_and_polylines(msp, [dxf_path])


def draw_circular_arc(center, start_point, end_point, radius, sweep, msp):
    """
    Draws a circular arc (rx = ry in path) to the Modelspace.

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

    # circular default direction is ccw (is_counter_clockwise = True), svg works other way around, thus not sweep
    msp.add_arc(center=center, radius=radius, start_angle=start_angle, end_angle=end_angle,
                is_counter_clockwise=not sweep)


def draw_rotated_elliptic_arc(center, rx, ry, theta, delta, rotation, sweep, msp):
    # calculate radian start- and end-angle
    start_angle = math.radians((-1) * theta)
    end_angle = math.radians((-1) * theta + (-1) * delta)

    # if sweep = True (--> ccw), change the angles
    if sweep:
        start_angle, end_angle = end_angle, start_angle

    # rotate the radii by the given rotation in the arc path
    rotated_rx = rotate_clockwise_around_cartesian_origin(rx, 0, rotation)
    rotated_ry = rotate_clockwise_around_cartesian_origin(0, ry, rotation)

    # determine mayor axis and ratio
    if rx >= ry:
        mayor_axis = rotated_rx
        ratio = ry / rx
    else:
        mayor_axis = rotated_ry
        ratio = rx / ry
        # if y is mayor axis, adjust angles (0 is on y-axis, not on x-axis)
        start_angle = start_angle - math.pi / 2
        end_angle = end_angle - math.pi / 2

    # add elliptic arc to modelspace
    msp.add_ellipse(center=center, major_axis=mayor_axis, ratio=ratio, start_param=start_angle, end_param=end_angle)
