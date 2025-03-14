from src.logging_config import setup_logger
from src.svg_shapes.transform_messages import export_transformations
from src.utilities import translate_coordinate, rotate_clockwise_around_point, change_svg_to_dxf_coordinate, \
    scale_coordinate, skew_x, skew_y

svg_line_logger = setup_logger(__name__)


class SvgLine:

    def __init__(self, element, svg_height):
        self.name = 'line'
        self.x1 = float(element.get('x1'))
        self.y1 = float(element.get('y1'))
        self.x2 = float(element.get('x2'))
        self.y2 = float(element.get('y2'))
        transform_message = element.get('transform')
        if transform_message is not None:
            self.transformation_list = export_transformations(transform_message)
            self.transform(svg_height)

        self.y1 = change_svg_to_dxf_coordinate(self.y1, svg_height)
        self.y2 = change_svg_to_dxf_coordinate(self.y2, svg_height)

    def get_name(self):
        return self.name

    def scale(self, scale_x, scale_y):
        self.x1 = self.x1 * scale_x
        self.y1 = self.y1 * scale_y
        self.x2 = self.x2 * scale_x
        self.y2 = self.y2 * scale_y

    def transform(self, svg_height):
        for t_type, values in self.transformation_list:
            match t_type:
                case 'translate':
                    self.x1 = translate_coordinate(self.x1, values[0])
                    self.x2 = translate_coordinate(self.x2, values[0])
                    if len(values) > 1:
                        self.y1 = translate_coordinate(self.y1, values[1])
                        self.y2 = translate_coordinate(self.y2, values[1])
                case 'rotate':
                    if len(values) == 1:
                        self.x1, y1 = rotate_clockwise_around_point(self.x1, -self.y1, values[0], 0, 0)
                        self.y1 = (-1) * y1
                        self.x2, y2 = rotate_clockwise_around_point(self.x2, -self.y2, values[0], 0, 0)
                        self.y2 = (-1) * y2
                    elif len(values) == 3:
                        self.x1, y1 = rotate_clockwise_around_point(self.x1, -self.y1, values[0], values[1],
                                                                    -values[2])
                        self.y1 = (-1) * y1
                        self.x2, y2 = rotate_clockwise_around_point(self.x2, -self.y2, values[0], values[1],
                                                                    -values[2])
                        self.y2 = (-1) * y2
                    else:
                        svg_line_logger.warning(f"unknown values length for rotate, length: {len(values)}")
                case 'scale':
                    self.x1 = scale_coordinate(self.x1, values[0])
                    self.x2 = scale_coordinate(self.x2, values[0])
                    if len(values) == 2:
                        self.y1 = scale_coordinate(self.y1, values[1])
                        self.y2 = scale_coordinate(self.y2, values[1])
                    else:
                        self.y1 = scale_coordinate(self.y1, values[0])
                        self.y2 = scale_coordinate(self.y2, values[0])
                case 'skewX':
                    self.x1 = skew_x(self.x1, self.y1, values[0])
                    self.x2 = skew_x(self.x2, self.y2, values[0])
                case 'skewY':
                    self.y1 = skew_y(self.x1, self.y1, values[0])
                    self.y2 = skew_y(self.x2, self.y2, values[0])
                case 'matrix':
                    if len(values) == 4:
                        values.append(0)
                        values.append(0)
                    new_x1 = values[0] * self.x1 + values[2] * self.y1 + values[4]
                    new_y1 = values[1] * self.x1 + values[3] * self.y1 + values[5]
                    self.x1, self.y1 = new_x1, new_y1
                    new_x2 = values[0] * self.x2 + values[2] * self.y2 + values[4]
                    new_y2 = values[1] * self.x2 + values[3] * self.y2 + values[5]
                    self.x2, self.y2 = new_x2, new_y2
