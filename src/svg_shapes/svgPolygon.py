from src.utilities import change_svg_to_dxf_coordinate, translate_coordinate, rotate_clockwise_around_point, \
    scale_coordinate, skew_x, skew_y
from src.svg_shapes.transform_messages import export_transformations
from src.logging_config import setup_logger

svg_polygon_logger = setup_logger(__name__)

class SvgPolygon:

    def __init__(self, element, svg_height):
        self.name = 'polygon'
        points = element.get('points')
        self.point_list = [(float(p.split(',')[0]), float(p.split(',')[1]))
            for p in points.strip().split()]
        transform_message = element.get('transform')
        if transform_message is not None:
            self.transformation_list = export_transformations(transform_message)
            self.transform()

        for i in range (0, len(self.point_list)):
            self.point_list[i] = (self.point_list[i][0], change_svg_to_dxf_coordinate(self.point_list[i][1], svg_height))


    def get_name(self):
        return self.name

    def scale(self, scale_x, scale_y):
        scaled_points = []

        for point in self.point_list:
            scaled_points.append((point[0] * scale_x, point[1] * scale_y))

        self.point_list = scaled_points

    def transform(self):
        len_points_list = len(self.point_list)
        for t_type, values in self.transformation_list:
            match t_type:
                case 'translate':
                    if len(values) == 1:
                        for i in range (0, len_points_list):
                            self.point_list[i] = (translate_coordinate(self.point_list[i][0], values[0]),
                            self.point_list[i][1])
                    elif len(values) == 2:
                        for i in range(0, len_points_list):
                            self.point_list[i] = (translate_coordinate(self.point_list[i][0], values[0]),
                            translate_coordinate(self.point_list[i][1], values[1]))
                    else:
                        svg_polygon_logger.warning(f"unknown translate entry in values, {len(values)}")
                case 'rotate':
                    if len(values) == 1:
                        for i in range (0, len_points_list):
                            rot_x, rot_y = rotate_clockwise_around_point(self.point_list[i][0], -self.point_list[i][1], values[0], 0, 0)
                            self.point_list[i] = (rot_x, (-1) * rot_y)
                    elif len(values) == 3:
                        for i in range (0, len_points_list):
                            rot_x, rot_y = rotate_clockwise_around_point(self.point_list[i][0], -self.point_list[i][1], values[0], values[1], -values[2])
                            self.point_list[i] = (rot_x, (-1) * rot_y)
                    else:
                        svg_polygon_logger.warning(f"unknown rotate entry in values, {len(values)}")
                case 'scale':
                    if len(values) == 1:
                        for i in range(0, len_points_list):
                            self.point_list[i] = (scale_coordinate(self.point_list[i][0], values[0]),
                            scale_coordinate(self.point_list[i][1], values[0]))
                    elif len(values) == 2:
                        for i in range(0, len_points_list):
                            self.point_list[i] = (scale_coordinate(self.point_list[i][0], values[0]),
                            scale_coordinate(self.point_list[i][1], values[1]))
                    else:
                        svg_polygon_logger.warning(f"unknown scale entry in values, {len(values)}")
                case 'skewX':
                    for i in range (0, len_points_list):
                        self.point_list[i] = (skew_x(self.point_list[i][0], self.point_list[i][1], values[0]), self.point_list[i][1])
                case 'skewY':
                    for i in range(0, len_points_list):
                        self.point_list[i] = (self.point_list[i][0], skew_y(self.point_list[i][0], self.point_list[i][1], values[0]))
                case 'matrix':
                    if len(values) == 4:
                        values.append(0)
                        values.append(0)

                    for i in range(0, len_points_list):
                        p_x = values[0] * self.point_list[i][0] + values[2] * self.point_list[i][1] + values[4]
                        p_y = values[1] * self.point_list[i][0] + values[3] * self.point_list[i][1] + values[5]
                        self.point_list[i] = (p_x, p_y)