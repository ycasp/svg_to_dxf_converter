from src.logging_config import setup_logger
from src.svg_shapes.transform_messages import export_transformations
from src.utilities import translate_coordinate, rotate_clockwise_around_point, change_svg_to_dxf_coordinate, \
    scale_coordinate, skew_x, skew_y, matrix_transformation

svg_line_logger = setup_logger(__name__)


class SvgLine:
    """"
    Represents an SvgLine, transforms it according to the transform message of svg and changes the coordinates into cartesian system.

    Attributes:
        name: string, 'line'
        x1: float, x-coordinate of start point
        y1: float, y-coordinate of start point
        x2: float, x-coordinate of end point
        y2: float, y-coordinate of end point
        transformation_list: list, with all transformations and its values
    """

    def __init__(self, element, svg_height):
        """
        Initializes the svg line.
        :param element: dictionary, svg line element
        :param svg_height: float, height of svg file
        """
        self.name = 'line'
        # extract the start/end point
        self.x1 = float(element.get('x1'))
        self.y1 = float(element.get('y1'))
        self.x2 = float(element.get('x2'))
        self.y2 = float(element.get('y2'))
        # extract transformations
        transform_message = element.get('transform')
        if transform_message is not None:
            self.transformation_list = export_transformations(transform_message)
            # transform according to transformations given in svg
            self.transform()

        # change svg to cartesian coordinates
        self.y1 = change_svg_to_dxf_coordinate(self.y1, svg_height)
        self.y2 = change_svg_to_dxf_coordinate(self.y2, svg_height)

    def get_name(self):
        """
        Getter of name.
        :return: 'line'
        """
        return self.name

    def scale(self, scale_x, scale_y):
        """
        Scales the line.
        :param scale_x: float, parameter for scaling in x-direction
        :param scale_y: float, parameter for scaling in y-direction
        :return: -
        """
        # scale start point
        self.x1 = self.x1 * scale_x
        self.y1 = self.y1 * scale_y
        # scale end point
        self.x2 = self.x2 * scale_x
        self.y2 = self.y2 * scale_y

    def transform(self):
        """
        Transforms the line according to the transformations in svg string.
        :return: -
        """
        # iterate over the transformations
        for t_type, values in self.transformation_list:
            match t_type:
                case 'translate':
                    if len(values) == 1:  # only translation in x-direction
                        self.x1 = translate_coordinate(self.x1, values[0])
                        self.x2 = translate_coordinate(self.x2, values[0])
                    elif len(values) == 2:  # translation in x- & y-direction
                        self.x1 = translate_coordinate(self.x1, values[0])
                        self.x2 = translate_coordinate(self.x2, values[0])
                        self.y1 = translate_coordinate(self.y1, values[1])
                        self.y2 = translate_coordinate(self.y2, values[1])
                    else:
                        svg_line_logger.warning(f'unknown translate values - values length: {len(values)}')
                case 'rotate':
                    if len(values) == 1:  # rotate around origin
                        self.x1, y1 = rotate_clockwise_around_point(self.x1, -self.y1, values[0], 0, 0)
                        self.y1 = (-1) * y1
                        self.x2, y2 = rotate_clockwise_around_point(self.x2, -self.y2, values[0], 0, 0)
                        self.y2 = (-1) * y2
                    elif len(values) == 3:  # rotate around given point
                        self.x1, y1 = rotate_clockwise_around_point(self.x1, -self.y1, values[0], values[1],
                                                                    -values[2])
                        self.y1 = (-1) * y1
                        self.x2, y2 = rotate_clockwise_around_point(self.x2, -self.y2, values[0], values[1],
                                                                    -values[2])
                        self.y2 = (-1) * y2
                    else:
                        svg_line_logger.warning(f"unknown values length for rotate, length: {len(values)}")
                case 'scale':
                    if len(values) == 1:  # if only one value, scale x- and y-direction the same
                        self.x1 = scale_coordinate(self.x1, values[0])
                        self.x2 = scale_coordinate(self.x2, values[0])
                        self.y1 = scale_coordinate(self.y1, values[0])
                        self.y2 = scale_coordinate(self.y2, values[0])
                    elif len(values) == 2:  # scale x- and y-coordinates to according values
                        self.x1 = scale_coordinate(self.x1, values[0])
                        self.x2 = scale_coordinate(self.x2, values[0])
                        self.y1 = scale_coordinate(self.y1, values[1])
                        self.y2 = scale_coordinate(self.y2, values[1])
                    else:
                        svg_line_logger.warning(f"unknown scale transformation, values len: {len(values)}")
                case 'skewX':
                    # skew in x-direction with tan(value[0])
                    self.x1 = skew_x(self.x1, self.y1, values[0])
                    self.x2 = skew_x(self.x2, self.y2, values[0])
                case 'skewY':
                    # skew in y-direction with tan(value[0])
                    self.y1 = skew_y(self.x1, self.y1, values[0])
                    self.y2 = skew_y(self.x2, self.y2, values[0])
                case 'matrix':
                    # if matrix has no translation - add zeros
                    if len(values) == 4:
                        values.append(0)
                        values.append(0)

                    # transform according to the matrix
                    self.x1, self.y1 = matrix_transformation(self.x1, self.y1, values)
                    self.x2, self.y2 = matrix_transformation(self.x2, self.y2, values)

                    """new_x1 = values[0] * self.x1 + values[2] * self.y1 + values[4]
                    new_y1 = values[1] * self.x1 + values[3] * self.y1 + values[5]
                    self.x1, self.y1 = new_x1, new_y1
                    new_x2 = values[0] * self.x2 + values[2] * self.y2 + values[4]
                    new_y2 = values[1] * self.x2 + values[3] * self.y2 + values[5]
                    self.x2, self.y2 = new_x2, new_y2"""
