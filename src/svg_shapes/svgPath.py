from svgpathtools import parse_path, Path, Line, CubicBezier, QuadraticBezier, Arc
from svgpathtools.parser import parse_transform
from svgpathtools.path import transform
import numpy as np
import math
from src.svg_shapes import export_transformations
from src.logging_config import setup_logger
from src.utilities import change_svg_to_dxf_coordinate

svg_path_logger = setup_logger(__name__)

class SvgPath:

    def __init__(self, element, svg_height):
        self.name = 'path'
        path_string = element.get('d')
        self.parsed_path = parse_path(path_string)
        transform_message = element.get('transform')
        if transform_message is not None:
            self.transformation_list = export_transformations(transform_message)
            transform_mat = parse_transform(transform_message)
            self.parsed_path = transform(self.parsed_path, transform_mat)

        self.change_path_svg_to_dxf_coordinate(svg_height)


    def get_name(self):
        return self.name

    def scale(self, scale_x, scale_y):
        def _scale(z):
            return scale_x * z.real + 1j * scale_y * z.imag

        for segment in self.parsed_path:
            if isinstance(segment, Line):
                segment.start = _scale(segment.start)
                segment.end = _scale(segment.end)
            elif isinstance(segment, QuadraticBezier):
                segment.start = _scale(segment.start)
                segment.end = _scale(segment.end)
                segment.control = _scale(segment.control)
            elif isinstance(segment, CubicBezier):
                segment.start = _scale(segment.start)
                segment.end = _scale(segment.end)
                segment.control1 = _scale(segment.control1)
                segment.control2 = _scale(segment.control2)
            elif isinstance(segment, Arc):
                segment.start = _scale(segment.start)
                segment.end = _scale(segment.end)
                segment.center = _scale(segment.center)
                segment.radius = _scale(segment.radius)
            else:
                svg_path_logger.warning("unsupported path segment: {}".format(segment))


    """def transform(self):
        transformed_path = self.parsed_path
        for t_type, values in self.transformation_list:
            match t_type:
                case 'translate':
                    if len(values) == 1:
                        transformed_path = transformed_path.translated(complex(values[0], 0))
                    elif len(values) == 2:
                        transformed_path = transformed_path.translated(complex(values[0], values[1]))
                    else:
                        svg_path_logger.warning(f"unknown translate entry in values, {len(values)}")
                case 'rotate':
                    if len(values) == 1:
                        transformed_path = transformed_path.rotated(values[0], complex(0, 0))
                    elif len(values) == 3:
                        transformed_path = transformed_path.rotated(values[0], complex(values[1], values[2]))
                    else:
                        svg_path_logger.warning(f"unknown rotate entry in values, {len(values)}")
                case 'scale':
                    if len(values) == 1:
                        transformed_path = transformed_path.scaled(values[0])
                    elif len(values) == 2:
                        transformed_path = transformed_path.scaled(values[0], values[1])
                    else:
                        svg_path_logger.warning(f"unknown scale entry in values, {len(values)}")
                case 'skewX':
                    skew_x = np.array([[1, math.tan(math.radians(values[0])), 0], [0, 1, 0], [0, 0, 1]])
                    transformed_path = transform(transformed_path, skew_x)
                case 'skewY':
                    skew_y = np.array([[1, 0, 0], [math.tan(math.radians(values[0])), 1, 0], [0, 0, 1]])
                    transformed_path = transform(transformed_path, skew_y)
                case 'matrix':
                    if len(values) == 4:
                        values.append(0)
                        values.append(0)

                    trafo_mat = np.array([[values[0], values[2], values[4]], [values[1], values[3], values[5]], [0, 0, 1]])
                    transformed_path = transform(transformed_path, trafo_mat)

        self.parsed_path = transformed_path"""

    def change_path_svg_to_dxf_coordinate(self, svg_height):
        for segment in self.parsed_path:
            if isinstance(segment, Line):
                segment.start = complex(segment.start.real, change_svg_to_dxf_coordinate(segment.start.imag, svg_height))
                segment.end = complex(segment.end.real, change_svg_to_dxf_coordinate(segment.end.imag, svg_height))
            elif isinstance(segment, QuadraticBezier):
                segment.start = complex(segment.start.real, change_svg_to_dxf_coordinate(segment.start.imag, svg_height))
                segment.end = complex(segment.end.real, change_svg_to_dxf_coordinate(segment.end.imag, svg_height))
                segment.control = complex(segment.control.real, change_svg_to_dxf_coordinate(segment.control.imag, svg_height))
            elif isinstance(segment, CubicBezier):
                segment.start = complex(segment.start.real, change_svg_to_dxf_coordinate(segment.start.imag, svg_height))
                segment.end = complex(segment.end.real, change_svg_to_dxf_coordinate(segment.end.imag, svg_height))
                segment.control1 = complex(segment.control1.real, change_svg_to_dxf_coordinate(segment.control1.imag, svg_height))
                segment.control2 = complex(segment.control2.real, change_svg_to_dxf_coordinate(segment.control2.imag, svg_height))

            elif isinstance(segment, Arc):
                segment.start = complex(segment.start.real, change_svg_to_dxf_coordinate(segment.start.imag, svg_height))
                segment.end = complex(segment.end.real, change_svg_to_dxf_coordinate(segment.end.imag, svg_height))
                segment.center = complex(segment.center.real, change_svg_to_dxf_coordinate(segment.center.imag, svg_height))

            else:
                svg_path_logger.warning("unsupported path segment: {}".format(segment))

