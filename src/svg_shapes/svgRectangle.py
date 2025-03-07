from src.svg_shapes import export_transformations
from src.utilities import change_svg_to_dxf_coordinate, translate_coordinate, rotate_clockwise_around_point, \
    scale_coordinate, scale_coordinate_svg, skew_x, change_dxf_to_svg_coordinate, skew_x_for_changed_point, \
    skew_y_for_changed_point, skew_y, matrix_transformation
from src.logging_config import setup_logger

svg_rect_logger = setup_logger(__name__)

class SvgRectangle:

    def __init__(self,element, svg_height):
        self.name = 'rectangle'

        self.x = float(element.get('x'))
        self.y = change_svg_to_dxf_coordinate(float(element.get('y')), svg_height)

        self.rect_width = (float(element.get('width')), 0)
        self.rect_height = (0, (-1) * float(element.get('height')))

        self.rx = (ensure_applicable_radius(float(element.get('rx') or 0), self.rect_width[0]), 0)
        self.ry = (0, ensure_applicable_radius(float(element.get('ry') or 0), abs(self.rect_height[1])))

        if self.rx != (0, 0) and self.ry == (0, 0):
            ry = ensure_applicable_radius(self.rx[0], abs(self.rect_height[1]))
            self.ry = (0, ry)
        elif self.rx == (0, 0) and self.ry != (0, 0):
            rx = ensure_applicable_radius(self.ry[1], self.rect_width[0])
            self.rx = (rx, 0)

        transform = element.get('transform')
        if transform is not None:
            self.transformation_list = export_transformations(transform)
            self.transform(svg_height)


    def get_name(self):
        return self.name

    def scale(self, scale_x, scale_y):
        self.x = self.x * scale_x
        self.y = self.y * scale_y

        self.rect_width = (self.rect_width[0] * scale_x, self.rect_width[1] * scale_y)
        self.rect_height = (self.rect_height[0] * scale_x, self.rect_height[1] * scale_y)

        self.rx = (self.rx[0] * scale_x, self.rx[1] * scale_y)
        self.ry = (self.ry[0] * scale_x, self.ry[1] * scale_y)

    def transform(self, svg_height):
        for t_type, values in self.transformation_list:
            match t_type:
                case 'translate':
                    self.x = translate_coordinate(self.x, values[0])
                    if len(values) > 1:
                        self.y = translate_coordinate(self.y, values[1])
                case 'rotate':
                    # rotate x,y
                    if len(values) == 1:
                        self.x, self.y = rotate_clockwise_around_point(self.x, self.y, values[0], 0, svg_height)
                    elif len(values) == 3:
                        self.x, self.y = rotate_clockwise_around_point(self.x, self.y,
                                            values[0], values[1], change_svg_to_dxf_coordinate(values[2], svg_height))
                    else:
                        svg_rect_logger.warning(f"unknown rotation value, length of values: {len(values)}")

                    # rotate rect_with,rect_height (around origin, as vectors/directions)
                    self.rect_width = rotate_clockwise_around_point(self.rect_width[0], self.rect_width[1],
                                                                    values[0], 0, 0)
                    self.rect_height = rotate_clockwise_around_point(self.rect_height[0], self.rect_height[1],
                                                                     values[0], 0, 0)

                    # rotate rx - if necessary
                    if self.rx != (0, 0): # and self.ry != (0, 0)
                        self.rx = rotate_clockwise_around_point(self.rx[0], self.rx[1], values[0], 0,0)
                        self.ry = rotate_clockwise_around_point(self.ry[0], self.ry[1], values[0], 0, 0)
                case 'scale':
                    self.x = scale_coordinate(self.x, values[0])
                    rect_width_x = scale_coordinate(self.rect_width[0], values[0])
                    rect_height_x = scale_coordinate(self.rect_height[0], values[0])
                    rx_x = scale_coordinate(self.rx[0], values[0])
                    ry_x = scale_coordinate(self.ry[0], values[0])
                    if len(values) == 2:
                        self.y = scale_coordinate_svg(self.y, values[1], svg_height)
                        rect_width_y = scale_coordinate(self.rect_width[1], values[1])
                        rect_height_y = scale_coordinate(self.rect_height[1], values[1])
                        rx_y = scale_coordinate(self.rx[1], values[1])
                        ry_y = scale_coordinate(self.ry[1], values[1])
                    else: # len(values) == 1
                        self.y = scale_coordinate_svg(self.y, values[0], svg_height)
                        rect_width_y = scale_coordinate(self.rect_width[1], values[0])
                        rect_height_y = scale_coordinate(self.rect_height[1], values[0])
                        rx_y = scale_coordinate(self.rx[1], values[0])
                        ry_y = scale_coordinate(self.ry[1], values[0])

                    self.rect_width = (rect_width_x, rect_width_y)
                    self.rect_height = (rect_height_x, rect_height_y)
                    self.rx = (rx_x, rx_y)
                    self.ry = (ry_x, ry_y)
                case 'skewX':
                    self.x = skew_x_for_changed_point(self.x, self.y, values[0], svg_height)
                    self.rect_width = (skew_x(self.rect_width[0], self.rect_width[1], values[0]), self.rect_width[1])
                    self.rect_height = (skew_x(self.rect_height[0], (-1) * self.rect_height[1], values[0]), self.rect_height[1])
                    # TODO skewX/skewY and rounded corners
                    """
                    self.rx = (skew_x(self.rx[0], self.rx[1], values[0]), self.rx[1])
                    self.ry = (skew_x(self.ry[0], self.ry[1], values[0]), self.ry[1])
                    """
                case 'skewY':
                    self.y = skew_y_for_changed_point(self.x, self.y, values[0])
                    self.rect_width = (self.rect_width[0], skew_y_for_changed_point(self.rect_width[0], self.rect_width[1], values[0]))
                    self.rect_height = (self.rect_height[0], skew_y_for_changed_point(self.rect_height[0], self.rect_height[1], values[0]))
                    # TODO skewX/skewY and rounded corners
                    """self.ry = (self.ry[0], skew_y(self.ry[0], self.ry[1], values[0]))
                    self.rx = (self.rx[0], skew_y(self.rx[0], self.rx[1], values[0]))"""
                case 'matrix':
                    if len(values) == 4:
                        values.append(0)
                        values.append(0)

                    new_x = values[0]*self.x - values[2]*self.y + values[2]*svg_height + values[4]
                    new_y = - values[1]*self.x + values[3]*self.y + (1 - values[3])*svg_height - values[5]
                    self.x, self.y = new_x, new_y

                    rect_width_x = values[0]*self.rect_width[0] + values[2]*self.rect_width[1]
                    rect_width_y = - values[1]*self.rect_width[0] - values[3]*self.rect_width[1]
                    self.rect_width = (rect_width_x, rect_width_y)

                    rect_height_x = values[0]*self.rect_height[0] - values[2]*self.rect_height[1]
                    rect_height_y = - values[1]*self.rect_height[0] + values[3]*self.rect_height[1]
                    self.rect_height = (rect_height_x, rect_height_y)
                    # TODO skewX/skewY and rounded corners
                    """ 
                    rx_x = values[0]*self.rx[0] + values[2]*self.rx[1]
                    rx_y = values[1]*self.rx[0] + values[3]*self.rx[1]
                    self.rx = (rx_x, rx_y)

                    ry_x = values[0] * self.ry[0] + values[2] * self.ry[1]
                    ry_y = values[1] * self.ry[0] + values[3] * self.ry[1]
                    self.ry = (ry_x, ry_y)
                    """
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
