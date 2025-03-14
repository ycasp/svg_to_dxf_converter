from src.logging_config import setup_logger
from src.svg_shapes.transform_messages import export_transformations
from src.utilities import change_svg_to_dxf_coordinate, rotate_clockwise_around_point, \
    translate_coordinate, scale_coordinate, matrix_transformation

svg_circle_logger = setup_logger('svg_circle')


class SvgCircle:
    """"
    Represents an SvgCircle, transforms it according to the transform message of svg and changes the coordinates into cartesian system.

    Attributes:
        name: 'circle', default for all circles
        center_x: x-coordinate of the center of the circle
        center_y: y-coordinate of the center of the circle
        radius:   radius of the circle
        radius_y: y-coordinate of the radius, default = 0 (if radius == radius_y) but need if transform transforms the circle into an ellipse
        transformation_list: list with all transformation given in the svg figure with its values
    """

    def __init__(self, segment, svg_height):
        """
        Initialisation of SvgCircle. Transforms the svg command to a circle in the cartesian coordinates.
        :param segment: dictionary, svg segment
        :param svg_height: float, height of the svg file, for coordinate transformation
        """
        self.name = 'circle'

        # set center
        self.center_x = float(segment.get('cx'))
        self.center_y = float(segment.get('cy'))

        # extract radius
        self.radius = float(segment.get('r'))
        self.radius_y = 0
        # extract transformations
        transform_message = segment.get('transform')
        if transform_message is not None:
            self.transformation_list = export_transformations(transform_message)
            # transform according to transformations given in svg
            self.transform()

        # change to dxf coordinates
        self.center_y = change_svg_to_dxf_coordinate(self.center_y, svg_height)

    def get_name(self):
        """
        Getter for name
        :return: 'circle'
        """
        return self.name

    def scale(self, scale_x, scale_y):
        """
        Scales the figure.
        :param scale_x: float, scaling in x-direction
        :param scale_y: float, scaling in y-direction
        :return: -
        """
        self.center_x = self.center_x * scale_x
        self.center_y = self.center_y * scale_y
        self.radius = self.radius * scale_x
        self.radius_y = self.radius_y * scale_y

    def transform(self):
        """
        Transforms the figure according to the transform attribute of the svg string.
        :return: -
        """
        # iterate over the transformations
        for t_type, values in self.transformation_list:
            match t_type:
                case 'translate':
                    if len(values) == 1:  # only translation in x-direction
                        self.center_x = translate_coordinate(self.center_x, values[0])
                    elif len(values) == 2:  # translation in x- & y-direction
                        self.center_x = translate_coordinate(self.center_x, values[0])
                        self.center_y = translate_coordinate(self.center_y, values[1])
                    else:
                        svg_circle_logger.warning(f'unknown translate values - values length: {len(values)}')
                case 'rotate':
                    if len(values) == 3:  # rotate around given point
                        self.center_x, center_y = rotate_clockwise_around_point(self.center_x, -self.center_y,
                                                                                values[0], values[1], -values[2])
                        self.center_y = center_y * (-1)
                    elif len(values) == 1:  # rotate around origin
                        self.center_x, center_y = rotate_clockwise_around_point(self.center_x, -self.center_y,
                                                                                values[0], 0, 0)
                        self.center_y = (-1) * center_y
                    else:
                        svg_circle_logger.warning(f"unknown rotation message, value length: {len(values)}")
                case 'scale':
                    if len(values) == 1:
                        # only one scale value given, scale along x and y with same value
                        self.center_x = scale_coordinate(self.center_x, values[0])
                        self.center_y = scale_coordinate(self.center_y, values[0])
                        self.radius = scale_coordinate(self.radius, values[0])
                    elif len(values) == 2:
                        # two scale values given - x- and y-scaling for according coordinate direction
                        self.center_x = scale_coordinate(self.center_x, values[0])
                        self.center_y = scale_coordinate(self.center_y, values[1])
                        r = self.radius
                        self.radius = scale_coordinate(self.radius, values[0])
                        self.radius_y = scale_coordinate(r, values[1])
                    else:
                        svg_circle_logger.warning(f"unknown scale transformation, values len: {len(values)}")
                case 'skewX':
                    # not done, as it will shear the circle to ellipse
                    svg_circle_logger.warning("skewX in circle - would give an ellipse, not handled")
                case 'skewY':
                    # not done, as it will shear the circle to ellipse
                    svg_circle_logger.warning("skewY in circle - would give an ellipse, not handled")
                case 'matrix':
                    # matrix trafo without transforming the radius...
                    if len(values) == 6:
                        self.center_x, self.center_y = matrix_transformation(self.center_x, self.center_y, values)
                    elif len(values) == 4:
                        values.append(0)
                        values.append(0)
                        self.center_x, self.center_y = matrix_transformation(self.center_x, self.center_y, values)
                    else:
                        svg_circle_logger.warning(f"unknown matrix message, values length: {len(values)}")
