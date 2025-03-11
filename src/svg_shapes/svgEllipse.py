from src.svg_shapes import export_transformations
from src.utilities import change_svg_to_dxf_coordinate, rotate_clockwise_around_point, \
    translate_coordinate, scale_coordinate
from src.logging_config import setup_logger

svg_ellipse_logger = setup_logger(__name__)

class SvgEllipse:

    def __init__(self, element, svg_height):
        self.name = 'ellipse'

        self.center_x = float(element.get('cx'))
        self.center_y = float(element.get('cy'))

        self.radius_x = (float(element.get('rx')), 0)
        self.radius_y = (0, float(element.get('ry')))

        transform_message = element.get('transform')
        if transform_message is not None:
            self.transformation_list = export_transformations(transform_message)
            self.transform()

        self.center_y = change_svg_to_dxf_coordinate(self.center_y, svg_height)



    def get_name(self):
        return self.name

    def scale(self, scale_x, scale_y):
        self.center_x = self.center_x * scale_x
        self.center_y = self.center_y * scale_y
        self.radius_x = (self.radius_x[0] * scale_x, self.radius_x[1] * scale_y)
        self.radius_y = (self.radius_y[0] * scale_x, self.radius_y[1] * scale_y)

    def transform(self):
        for t_type, values in self.transformation_list:
            match t_type:
                case 'translate':
                    if len(values) == 1:
                        self.center_x = translate_coordinate(self.center_x, values[0])
                    elif len(values) == 2:
                        self.center_x = translate_coordinate(self.center_x, values[0])
                        self.center_y = translate_coordinate(self.center_y, values[1])
                    else:
                        svg_ellipse_logger.warning(f"unknown translate entry in values, {len(values)}")
                case 'rotate':
                    if len(values) == 1:
                        self.center_x, center_y = rotate_clockwise_around_point(self.center_x, -self.center_y,
                                                                                     values[0], 0, 0)
                        self.center_y = (-1) * center_y
                        self.radius_x = rotate_clockwise_around_point(self.radius_x[0], self.radius_x[1],
                                                                      values[0], 0, 0)
                        self.radius_y = rotate_clockwise_around_point(self.radius_y[0], self.radius_y[1],
                                                                      values[0], 0, 0)
                    elif len(values) == 3:
                        self.center_x, center_y = rotate_clockwise_around_point(self.center_x, -self.center_y,
                                                                                values[0], values[1], -values[2])
                        self.center_y = (-1) * center_y
                        self.radius_x = rotate_clockwise_around_point(self.radius_x[0], self.radius_x[1],
                                                                      values[0], 0, 0)
                        self.radius_y  = rotate_clockwise_around_point(self.radius_y[0], self.radius_y[1],
                                                                      values[0], 0, 0)
                    else:
                        svg_ellipse_logger.warning(f"unknown rotate entry in values, {len(values)}")
                case 'scale':
                    if len(values) == 1:
                        self.center_x = scale_coordinate(self.center_x, values[0])
                        self.center_y = scale_coordinate(self.center_y, values[0])
                        self.radius_x = (scale_coordinate(self.radius_x[0], values[0]),
                            scale_coordinate(self.radius_x[1], values[0]))
                        self.radius_y = (scale_coordinate(self.radius_y[0], values[0]),
                            scale_coordinate(self.radius_y[1], values[0]))
                    elif len(values) == 2:
                        self.center_x = scale_coordinate(self.center_x, values[0])
                        self.center_y = scale_coordinate(self.center_y, values[1])
                        self.radius_x = (scale_coordinate(self.radius_x[0], values[0]),
                        scale_coordinate(self.radius_x[1], values[1]))
                        self.radius_y = (scale_coordinate(self.radius_y[0], values[0]),
                        scale_coordinate(self.radius_y[1], values[1]))
                    else:
                        svg_ellipse_logger.warning(f"unknown scale entry in values, {len(values)}")
                case 'skewX':
                    svg_ellipse_logger.warning(f'skewX not implemented for ellipse')
                case 'skewY':
                    svg_ellipse_logger.warning(f'skewY not implemented for ellipse')
                case 'matrix':
                    svg_ellipse_logger.warning(f'matrix not implemented for ellipse')