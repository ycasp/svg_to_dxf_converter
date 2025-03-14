from src.logging_config import setup_logger
from src.svg_shapes import export_transformations
from src.utilities import change_svg_to_dxf_coordinate, rotate_clockwise_around_point, \
    translate_coordinate, scale_coordinate

svg_ellipse_logger = setup_logger(__name__)


class SvgEllipse:
    """"
    Represents an SvgEllipse, transforms it according to the transform message of svg and changes the coordinates into cartesian system.

    Attributes:
        name: 'ellipse', default for all ellipses
        center_x: x-coordinate of the center of the ellipse
        center_y: y-coordinate of the center of the ellipse
        radius_x: radius in x direction of the ellipse
        radius_y: radius in y direction of the ellipse
        transformation_list: list with all transformation given in the svg figure with its values  
    """

    def __init__(self, element, svg_height):
        """
        Initializes the SvgEllipse. Already transforms the data and changes it to cartesian coordinates.
        :param element: dictionary, svg ellipse string
        :param svg_height: float, height of svg file
        """
        self.name = 'ellipse'
        # extract center
        self.center_x = float(element.get('cx'))
        self.center_y = float(element.get('cy'))
        # extract radius, transform it to vec (for rotation, skew, usw)
        self.radius_x = (float(element.get('rx')), 0)
        self.radius_y = (0, float(element.get('ry')))

        transform_message = element.get('transform')
        if transform_message is not None:
            self.transformation_list = export_transformations(transform_message)
            # transform according to transform message in svg string
            self.transform()

        # change the coordinate to cartesian coordinates
        self.center_y = change_svg_to_dxf_coordinate(self.center_y, svg_height)

    def get_name(self):
        """
        Getter for element name
        :return: 'ellipse'
        """
        return self.name

    def scale(self, scale_x, scale_y):
        """
        Scales the ellipse with scale_x, scale_y.
        :param scale_x: float, scaling parameter in x-direction
        :param scale_y: float, scaling parameter in y-direction
        :return: -
        """
        # scale center
        self.center_x = self.center_x * scale_x
        self.center_y = self.center_y * scale_y
        # scale radii
        self.radius_x = (self.radius_x[0] * scale_x, self.radius_x[1] * scale_y)
        self.radius_y = (self.radius_y[0] * scale_x, self.radius_y[1] * scale_y)

    def transform(self):
        """
        Transform the ellipse according to the transform message given in the svg string.
        :return: -
        """
        for t_type, values in self.transformation_list:
            match t_type:
                case 'translate':
                    if len(values) == 1:
                        # only translation in x-direction
                        self.center_x = translate_coordinate(self.center_x, values[0])
                    elif len(values) == 2:
                        # translation in x- and y-direction
                        self.center_x = translate_coordinate(self.center_x, values[0])
                        self.center_y = translate_coordinate(self.center_y, values[1])
                    else:
                        svg_ellipse_logger.warning(f"unknown translate entry in values, {len(values)}")
                case 'rotate':
                    if len(values) == 1:
                        # rotate around origin (svg origin)
                        self.center_x, center_y = rotate_clockwise_around_point(self.center_x, -self.center_y,
                                                                                values[0], 0, 0)
                        self.center_y = (-1) * center_y
                        self.radius_x = rotate_clockwise_around_point(self.radius_x[0], self.radius_x[1],
                                                                      values[0], 0, 0)
                        self.radius_y = rotate_clockwise_around_point(self.radius_y[0], self.radius_y[1],
                                                                      values[0], 0, 0)
                    elif len(values) == 3:
                        # rotate around given point (in svg coordinate system)
                        self.center_x, center_y = rotate_clockwise_around_point(self.center_x, -self.center_y,
                                                                                values[0], values[1], -values[2])
                        self.center_y = (-1) * center_y
                        self.radius_x = rotate_clockwise_around_point(self.radius_x[0], self.radius_x[1],
                                                                      values[0], 0, 0)
                        self.radius_y = rotate_clockwise_around_point(self.radius_y[0], self.radius_y[1],
                                                                      values[0], 0, 0)
                    else:
                        svg_ellipse_logger.warning(f"unknown rotate entry in values, {len(values)}")
                case 'scale':
                    if len(values) == 1:
                        # only one scale value given, scale x- & y-direction with same value
                        self.center_x = scale_coordinate(self.center_x, values[0])
                        self.center_y = scale_coordinate(self.center_y, values[0])
                        self.radius_x = (scale_coordinate(self.radius_x[0], values[0]),
                        scale_coordinate(self.radius_x[1], values[0]))
                        self.radius_y = (scale_coordinate(self.radius_y[0], values[0]),
                        scale_coordinate(self.radius_y[1], values[0]))
                    elif len(values) == 2:
                        # scale x according to first value, y according to second value
                        self.center_x = scale_coordinate(self.center_x, values[0])
                        self.center_y = scale_coordinate(self.center_y, values[1])
                        self.radius_x = (scale_coordinate(self.radius_x[0], values[0]),
                        scale_coordinate(self.radius_x[1], values[1]))
                        self.radius_y = (scale_coordinate(self.radius_y[0], values[0]),
                        scale_coordinate(self.radius_y[1], values[1]))
                    else:
                        svg_ellipse_logger.warning(f"unknown scale entry in values, {len(values)}")
                case 'skewX':
                    # not done, as it will no longer be an ellipse
                    svg_ellipse_logger.warning(f'skewX not implemented for ellipse')
                case 'skewY':
                    # not done, as it will no longer be an ellipse
                    svg_ellipse_logger.warning(f'skewY not implemented for ellipse')
                case 'matrix':
                    # not done, as it will no longer be an ellipse
                    svg_ellipse_logger.warning(f'matrix not implemented for ellipse')
