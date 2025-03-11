from src.svg_shapes.transform_messages import export_transformations
from src.utilities import change_svg_to_dxf_coordinate, rotate_clockwise_around_point, \
    translate_coordinate, scale_coordinate, matrix_transformation
from src.logging_config import setup_logger

svg_circle_logger = setup_logger('svg_circle')

class SvgCircle:

    def __init__(self, segment, svg_height):
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
            self.transform()

        self.center_y = change_svg_to_dxf_coordinate(self.center_y, svg_height)

    def get_name(self):
        return self.name

    def scale(self, scale_x, scale_y):
        self.center_x = self.center_x * scale_x
        self.center_y = self.center_y * scale_y
        self.radius = self.radius * scale_x
        # self.radius_y = self.radius_y * scale_y

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
                        svg_circle_logger.warning(f'unknown translate values - values length: {len(values)}')
                case 'rotate':
                    if len(values) == 3:
                        self.center_x, center_y = rotate_clockwise_around_point(self.center_x, -self.center_y,
                                                    values[0], values[1], -values[2])
                        self.center_y = center_y * (-1)
                    elif len(values) == 1:
                        self.center_x, center_y = rotate_clockwise_around_point(self.center_x, -self.center_y,
                                                                                     values[0], 0, 0)
                        self.center_y = (-1) * center_y
                    else:
                        svg_circle_logger.warning(f"unknown rotation message, value length: {len(values)}")
                case 'scale':

                    if len(values) == 1:
                        self.center_x = scale_coordinate(self.center_x, values[0])
                        self.center_y = scale_coordinate(self.center_y, values[0])
                        self.radius = scale_coordinate(self.radius, values[0])
                    elif len(values) == 2:
                        self.center_x = scale_coordinate(self.center_x, values[0])
                        self.center_y = scale_coordinate(self.center_y, values[1])
                        r = self.radius
                        self.radius = scale_coordinate(self.radius, values[0])
                        self.radius_y = scale_coordinate(r, values[1])
                    else:
                        svg_circle_logger.warning(f"unknown scale transformation, values len: {len(values)}")
                case 'skewX':
                    svg_circle_logger.warning("skewX in circle - would give an ellipse, not handled")
                case 'skewY':
                    svg_circle_logger.warning("skewY in circle - would give an ellipse, not handled")
                case 'matrix':
                    if len(values) == 6:
                        self.center_x, self.center_y = matrix_transformation(self.center_x, self.center_y, values)
                    elif len(values) == 4:
                        values.append(0)
                        values.append(0)
                        self.center_x, self.center_y = matrix_transformation(self.center_x, self.center_y, values)
                    else:
                        svg_circle_logger.warning(f"unknown matrix message, values length: {len(values)}")