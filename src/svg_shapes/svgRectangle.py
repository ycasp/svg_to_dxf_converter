from src.logging_config import setup_logger
from src.svg_shapes import export_transformations
from src.utilities import change_svg_to_dxf_coordinate, translate_coordinate, rotate_clockwise_around_point, \
    scale_coordinate, skew_x, skew_y, matrix_transformation

svg_rect_logger = setup_logger(__name__)


class SvgRectangle:
    """
    Represents an SvgRectangle, transforms it according to the transform message of svg and changes the coordinates into cartesian system.

    Attributes:
        name: string, 'rectangle'
        x: float, top left corner of rectangle
        y: float, top right corner of rectangle
        rect_width: float, width of rectangle
        rect_height: float, height of rectangle
        rx: float, radius in x-direction of rounded corner
        ry: float, radius in y-direction of rounded corner
        transformation_list: list, with all transformations and its values
    """

    def __init__(self, element, svg_height):
        """
        Initializes the svg rectangle.
        :param element: dictionary, with svg rectangle content
        :param svg_height: float, height of svg file
        """
        self.name = 'rectangle'
        # extract the top left corner
        self.x = float(element.get('x'))
        self.y = float(element.get('y'))

        # extract the width, height of the rect - transform it vectors
        self.rect_width = (float(element.get('width')), 0)
        self.rect_height = (0, float(element.get('height')))

        # extract the rounded corner radii, assure they are applicable and transform them to vectors
        self.rx = (ensure_applicable_radius(float(element.get('rx') or 0), self.rect_width[0]), 0)
        self.ry = (0, ensure_applicable_radius(float(element.get('ry') or 0), abs(self.rect_height[1])))

        # if one of them is zero, set them equal (but check if applicable)
        if self.rx != (0, 0) and self.ry == (0, 0):
            ry = ensure_applicable_radius(self.rx[0], abs(self.rect_height[1]))
            self.ry = (0, ry)
        elif self.rx == (0, 0) and self.ry != (0, 0):
            rx = ensure_applicable_radius(self.ry[1], self.rect_width[0])
            self.rx = (rx, 0)

        # get transform message and transform rect
        transform = element.get('transform')
        if transform is not None:
            self.transformation_list = export_transformations(transform)
            self.transform()

        # change to dxf / cartesian coordinates
        self.y = change_svg_to_dxf_coordinate(self.y, svg_height)
        self.rect_height = (self.rect_height[0], (-1) * self.rect_height[1])
        self.rect_width = (self.rect_width[0], (-1) * self.rect_width[1])

    def get_name(self):
        """
        Getter of rect name.
        :return: 'rectangle'
        """
        return self.name

    def scale(self, scale_x, scale_y):
        """
        Scale rectangle.
        :param scale_x: float, scaling parameter in x-direction
        :param scale_y: float, scaling parameter in y-direction
        :return: -
        """
        # scale top left corner
        self.x = self.x * scale_x
        self.y = self.y * scale_y
        # scale height and width of rectangle
        self.rect_width = (self.rect_width[0] * scale_x, self.rect_width[1] * scale_y)
        self.rect_height = (self.rect_height[0] * scale_x, self.rect_height[1] * scale_y)
        # scale rounded corner radii
        self.rx = (self.rx[0] * scale_x, self.rx[1] * scale_y)
        self.ry = (self.ry[0] * scale_x, self.ry[1] * scale_y)

    def transform(self):
        # iterate over transform message and its values
        for t_type, values in self.transformation_list:
            match t_type:
                case 'translate':
                    if len(values) == 1:  # only translate in x-direction
                        self.x = translate_coordinate(self.x, values[0])
                    elif len(values) == 2:  # translate in x- and y-direction
                        self.x = translate_coordinate(self.x, values[0])
                        self.y = translate_coordinate(self.y, values[1])
                    else:
                        svg_rect_logger.warning(f"unknown translate entry in values, {len(values)}")
                case 'rotate':
                    # rotate x,y
                    if len(values) == 1:  # around svg origin
                        self.x, y = rotate_clockwise_around_point(self.x, -self.y, values[0], 0, 0)
                        self.y = (-1) * y
                    elif len(values) == 3:  # around point (in svg coordinates)
                        self.x, y = rotate_clockwise_around_point(self.x, -self.y, values[0], values[1], -values[2])
                        self.y = (-1) * y
                    else:
                        svg_rect_logger.warning(f"unknown rotation value, length of values: {len(values)}")

                    # rotate rect_with,rect_height (around origin, as vectors/directions)
                    w_x, w_y = rotate_clockwise_around_point(self.rect_width[0], -self.rect_width[1],
                                                             values[0], 0, 0)
                    self.rect_width = (w_x, (-1) * w_y)
                    h_x, h_y = rotate_clockwise_around_point(self.rect_height[0], -self.rect_height[1],
                                                             values[0], 0, 0)
                    self.rect_height = (h_x, (-1) * h_y)

                    # rotate rx - if necessary
                    if self.rx != (0, 0):  # and self.ry != (0, 0)
                        self.rx = rotate_clockwise_around_point(self.rx[0], self.rx[1], values[0], 0, 0)
                        self.ry = rotate_clockwise_around_point(self.ry[0], self.ry[1], values[0], 0, 0)
                case 'scale':
                    if len(values) == 1:  # only one value - scale all with same parameter
                        # scale top left corner
                        self.x = scale_coordinate(self.x, values[0])
                        self.y = scale_coordinate(self.y, values[0])
                        # scale height and width of rectangle
                        self.rect_width = (scale_coordinate(self.rect_width[0], values[0]),
                        scale_coordinate(self.rect_width[1], values[0]))
                        self.rect_height = (scale_coordinate(self.rect_height[0], values[0]),
                        scale_coordinate(self.rect_height[1], values[0]))
                        # scale radii of rounded corners
                        self.rx = (scale_coordinate(self.rx[0], values[0]), scale_coordinate(self.rx[1], values[0]))
                        self.ry = (scale_coordinate(self.ry[0], values[0]), scale_coordinate(self.ry[1], values[0]))
                    elif len(values) == 2:  # two values - scale in x- and y-direction differently
                        # scale top left corner
                        self.x = scale_coordinate(self.x, values[0])
                        self.y = scale_coordinate(self.y, values[1])
                        # scale height and width of rectangle
                        self.rect_width = (scale_coordinate(self.rect_width[0], values[0]),
                        scale_coordinate(self.rect_width[1], values[1]))
                        self.rect_height = (scale_coordinate(self.rect_height[0], values[0]),
                        scale_coordinate(self.rect_height[1], values[1]))
                        # scale radii of rounded corners
                        self.rx = (scale_coordinate(self.rx[0], values[0]), scale_coordinate(self.rx[1], values[1]))
                        self.ry = (scale_coordinate(self.ry[0], values[0]), scale_coordinate(self.ry[1], values[1]))
                    else:
                        svg_rect_logger.warning(f"unknown scale entry in values, {len(values)}")
                case 'skewX':
                    # skew in x direction
                    self.x = skew_x(self.x, self.y, values[0])
                    self.rect_width = (skew_x(self.rect_width[0], self.rect_width[1], values[0]), self.rect_width[1])
                    self.rect_height = (
                        skew_x(self.rect_height[0], self.rect_height[1], values[0]), self.rect_height[1])
                    # TODO skewX/skewY and rounded corners
                case 'skewY':
                    # skew in y direction
                    self.y = skew_y(self.x, self.y, values[0])
                    self.rect_width = (
                        self.rect_width[0], skew_y(self.rect_width[0], self.rect_width[1], values[0]))
                    self.rect_height = (
                        self.rect_height[0], skew_y(self.rect_height[0], self.rect_height[1], values[0]))
                    # TODO skewX/skewY and rounded corners
                case 'matrix':
                    # if matrix without translation, add zeros
                    if len(values) == 4:
                        values.append(0)
                        values.append(0)

                    # transform top left corners
                    self.x, self.y = matrix_transformation(self.x, self.y, values)

                    # transform height and width from rectangle
                    rect_width_x = values[0] * self.rect_width[0] + values[2] * self.rect_width[1]
                    rect_width_y = values[1] * self.rect_width[0] + values[3] * self.rect_width[1]
                    self.rect_width = (rect_width_x, rect_width_y)

                    rect_height_x = values[0] * self.rect_height[0] + values[2] * self.rect_height[1]
                    rect_height_y = values[1] * self.rect_height[0] + values[3] * self.rect_height[1]
                    self.rect_height = (rect_height_x, rect_height_y)

                    # TODO skewX/skewY and rounded corners


def ensure_applicable_radius(r, length):
    """
    Ensures that the radius of the curves are applicable.
    The radius (in both directions) should only be as long as the half of the length (x radius) or height (y radius).
    :param r: radius of the corner
    :param length: length of the corresponding direction of the rectangle
    :return: r if radius is good, or length / 2 if radius was chosen to big
    """
    if r <= length / 2:
        return r
    else:
        return length / 2
