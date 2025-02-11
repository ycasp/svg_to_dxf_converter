from ezdxf.path import from_vertices, render_splines_and_polylines
from svgpathtools.path import Line as svgLine
from svgpathtools.path import CubicBezier, QuadraticBezier, Arc
from svgpathtools import parse_path

from src.utilities import change_svg_to_dxf_coordinate


class Path:
    """
    Represents a path of a svg file.

    Attributes
       path (string): The path of a svg file.
    """
    # maximal distance to the original Bézier curve
    MAX_DISTANCE = 0.1
    # minimal segments a Bézier curve is split into
    MIN_SEGMENTS = 3

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
                """ 
                bezier_points = [segment.start, segment.control1, segment.control2, segment.end]
                msp.add_lwpolyline([(p.real, change_svg_to_dxf_coordinate(p.imag, height)) for p in bezier_points], close=False)
                """
                self.approximate_cubic_bezier_curve(segment, msp, height)
            elif isinstance(segment, QuadraticBezier):
                # Approximate Quadratic Bézier curve with a polyline
                """
                bezier_points = [segment.start, segment.control, segment.end]
                msp.add_lwpolyline([(p.real, change_svg_to_dxf_coordinate(p.imag, height)) for p in bezier_points], close=False)
                """
                self.approximate_quadratic_bezier_curve(segment, msp, height)
            elif isinstance(segment, Arc):
                # Add an ARC for SVG Arc segment
                msp.add_arc(center=(segment.center.real, change_svg_to_dxf_coordinate(segment.center.imag, height)),
                            radius=segment.radius.real)
            else:
                print(f"Unsupported segment type: {type(segment)}")

    @staticmethod
    def approximate_cubic_bezier_curve(segment, msp, height):
        """
        Approximates a cubic Bézier curve and adds it to the modelspace of the dxf file.

        :param segment: path segment, describing the Bézier curve with two control points, start and endpoint.
        :param msp: modelspace, where the curve is added, i.e. the approximation of the curve
        :param height: height for transformation to cartesian coordinates
        :return: -
        """

        dxf_path = from_vertices([(0,0)])
        dxf_path.move_to((segment.start.real, change_svg_to_dxf_coordinate(segment.start.imag, height)))

        dxf_path.curve4_to((segment.end.real, change_svg_to_dxf_coordinate(segment.end.imag, height)),
                               (segment.control1.real, change_svg_to_dxf_coordinate(segment.control1.imag, height)),
                           (segment.control2.real, change_svg_to_dxf_coordinate(segment.control2.imag, height)))

        # render_lines(msp, [dxf_path], distance = Path.MAX_DISTANCE, segments = Path.MIN_SEGMENTS)

        render_splines_and_polylines(msp, [dxf_path])

    @staticmethod
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