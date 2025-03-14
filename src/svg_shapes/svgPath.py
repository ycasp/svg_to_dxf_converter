from svgpathtools import parse_path, Line, CubicBezier, QuadraticBezier, Arc
from svgpathtools.parser import parse_transform
from svgpathtools.path import transform

from src.logging_config import setup_logger
from src.svg_shapes import export_transformations
from src.utilities import change_svg_to_dxf_coordinate

svg_path_logger = setup_logger(__name__)


class SvgPath:
    """"
    Represents a svg path, transforms it according to the transform message of svg and changes the coordinates into cartesian system.

    Attributes:
        name: string, 'path'
        parsed_path: svgpathtools path, with all segments
        transformation_list: list, with all transformations and its values
    """

    def __init__(self, element, svg_height):
        """
        Initializes svg path.
        :param element: dictionary, svg path element
        :param svg_height: float, height of svg file
        """
        self.name = 'path'
        # extract the path string / values and parse it
        path_string = element.get('d')
        self.parsed_path = parse_path(path_string)
        # extract the transformations and apply it to the path
        transform_message = element.get('transform')
        if transform_message is not None:
            self.transformation_list = export_transformations(transform_message)
            # for every transformation get the transformation matrices
            transform_mat = parse_transform(transform_message)
            # apply it to the path
            self.parsed_path = transform(self.parsed_path, transform_mat)

        # change the coordinates to cartesian format (not svg)
        self.change_path_svg_to_dxf_coordinate(svg_height)

    def get_name(self):
        """
        Getter for name.
        :return: 'path'
        """
        return self.name

    def scale(self, scale_x, scale_y):
        """
        Scales the path.
        :param scale_x: float, scaling parameter in x-direction
        :param scale_y: float, scaling parameter in y-direction
        :return: -
        """

        def _scale(z):
            """
            Scale a complex number.
            :param z: complex number, to be scaled
            :return: complex number, scaled with scale_x, scale_y
            """
            return scale_x * z.real + 1j * scale_y * z.imag

        # Note: if we would do it via the matrix [[scale_x, 0, 0], [0, scale_y, 0], [0, 0, 1]] (which is the matrix transform of our step), the arc center would be adjusted to the actual coordinates, but we need the old center just scaled

        # iterate over path segments
        for segment in self.parsed_path:
            if isinstance(segment, Line):
                # scale start and end point of line
                segment.start = _scale(segment.start)
                segment.end = _scale(segment.end)
            elif isinstance(segment, QuadraticBezier):
                # scale start, end and control point of quadratic Bézier curve
                segment.start = _scale(segment.start)
                segment.end = _scale(segment.end)
                segment.control = _scale(segment.control)
            elif isinstance(segment, CubicBezier):
                # scale start, end and both control points of quadratic Bézier curve
                segment.start = _scale(segment.start)
                segment.end = _scale(segment.end)
                segment.control1 = _scale(segment.control1)
                segment.control2 = _scale(segment.control2)
            elif isinstance(segment, Arc):
                # scales arc components (start point, end point, center, radii)
                segment.start = _scale(segment.start)
                segment.end = _scale(segment.end)
                segment.center = _scale(segment.center)
                segment.radius = _scale(segment.radius)
            else:
                svg_path_logger.warning("unsupported path segment: {}".format(segment))

    def change_path_svg_to_dxf_coordinate(self, svg_height):
        """
        Changes the coordinates of the path to cartesian coordinates.
        :param svg_height: float, height of svg file
        :return: -
        """
        # Note: if we would do it via the matrix [[1, 0, 0], [0, -1, height], [0, 0, 1]] (which is the matrix transform of our step), the arc center would be adjusted to the actual coordinates, but we need the old center just translated

        # iterate over path segments
        for segment in self.parsed_path:
            if isinstance(segment, Line):
                # change start and end point of line
                segment.start = complex(segment.start.real,
                                        change_svg_to_dxf_coordinate(segment.start.imag, svg_height))
                segment.end = complex(segment.end.real, change_svg_to_dxf_coordinate(segment.end.imag, svg_height))
            elif isinstance(segment, QuadraticBezier):
                # change start, end and control point of quadratic Bézier curve
                segment.start = complex(segment.start.real,
                                        change_svg_to_dxf_coordinate(segment.start.imag, svg_height))
                segment.end = complex(segment.end.real, change_svg_to_dxf_coordinate(segment.end.imag, svg_height))
                segment.control = complex(segment.control.real,
                                          change_svg_to_dxf_coordinate(segment.control.imag, svg_height))
            elif isinstance(segment, CubicBezier):
                # change start, end and both control points of cubic Bézier curve
                segment.start = complex(segment.start.real,
                                        change_svg_to_dxf_coordinate(segment.start.imag, svg_height))
                segment.end = complex(segment.end.real, change_svg_to_dxf_coordinate(segment.end.imag, svg_height))
                segment.control1 = complex(segment.control1.real,
                                           change_svg_to_dxf_coordinate(segment.control1.imag, svg_height))
                segment.control2 = complex(segment.control2.real,
                                           change_svg_to_dxf_coordinate(segment.control2.imag, svg_height))

            elif isinstance(segment, Arc):
                # change start and end point of arc, as well as its center
                segment.start = complex(segment.start.real,
                                        change_svg_to_dxf_coordinate(segment.start.imag, svg_height))
                segment.end = complex(segment.end.real, change_svg_to_dxf_coordinate(segment.end.imag, svg_height))
                segment.center = complex(segment.center.real,
                                         change_svg_to_dxf_coordinate(segment.center.imag, svg_height))

            else:
                svg_path_logger.warning("unsupported path segment: {}".format(segment))
