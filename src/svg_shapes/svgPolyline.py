from src.logging_config import setup_logger
from src.svg_shapes import export_transformations
from src.utilities import change_svg_to_dxf_coordinate, translate_coordinate, rotate_clockwise_around_point, \
    scale_coordinate, skew_x, skew_y, matrix_transformation

svg_polyline_logger = setup_logger(__name__)


class SvgPolyline:
    """
    Represents a SvgPolyline, transforms it according to the transform message of svg and changes the coordinates into cartesian system.

    Attributes:
        name: string, 'polyline'
        point_list: list of all vertices in the polyline
        transformation_list: list, with all transformations and its values
    """

    def __init__(self, element, svg_height):
        """
        Initializes the svg polyline.
        :param element: dictionary, with the svg polyline content
        :param svg_height: float, height of the svg file
        """
        self.name = 'polyline'
        # extract the points
        points = element.get('points')
        # transform it from string to list
        self.point_list = [(float(p.split(',')[0]), float(p.split(',')[1]))
            for p in points.strip().split()]
        # extract the transform message and apply it to the point list
        transform_message = element.get('transform')
        if transform_message is not None:
            self.transformation_list = export_transformations(transform_message)
            self.transform()

        # change the svg coordinates to dxf/cartesian coordinates
        for i in range(0, len(self.point_list)):
            self.point_list[i] = (
                self.point_list[i][0], change_svg_to_dxf_coordinate(self.point_list[i][1], svg_height))

    def get_name(self):
        """
        Getter of name.
        :return: 'polyline'
        """
        return self.name

    def scale(self, scale_x, scale_y):
        """
        Scales the polyline.
        :param scale_x: float, scaling in x-direction
        :param scale_y: float, scaling in y-direction
        :return:
        """
        scaled_points = []
        # iterate over points and scale it accordingly
        for point in self.point_list:
            scaled_points.append((point[0] * scale_x, point[1] * scale_y))

        self.point_list = scaled_points

    def transform(self):
        """
        Transform the polyline after the transform message.
        :return: -
        """
        len_points_list = len(self.point_list)
        # iterate over transform message and its values
        for t_type, values in self.transformation_list:
            match t_type:
                case 'translate':
                    if len(values) == 1:  # only translation in x-direction
                        for i in range(0, len_points_list):
                            self.point_list[i] = (translate_coordinate(self.point_list[i][0], values[0]),
                            self.point_list[i][1])
                    elif len(values) == 2:  # translation in x- & y-direction
                        for i in range(0, len_points_list):
                            self.point_list[i] = (translate_coordinate(self.point_list[i][0], values[0]),
                            translate_coordinate(self.point_list[i][1], values[1]))
                    else:
                        svg_polyline_logger.warning(f"unknown translate entry in values, {len(values)}")
                case 'rotate':
                    if len(values) == 1:  # rotate around origin
                        for i in range(0, len_points_list):
                            rot_x, rot_y = rotate_clockwise_around_point(self.point_list[i][0], -self.point_list[i][1],
                                                                         values[0], 0, 0)
                            self.point_list[i] = (rot_x, (-1) * rot_y)
                    elif len(values) == 3:  # rotate around given point
                        for i in range(0, len_points_list):
                            rot_x, rot_y = rotate_clockwise_around_point(self.point_list[i][0], -self.point_list[i][1],
                                                                         values[0], values[1], -values[2])
                            self.point_list[i] = (rot_x, (-1) * rot_y)
                    else:
                        svg_polyline_logger.warning(f"unknown rotate entry in values, {len(values)}")
                case 'scale':
                    if len(values) == 1:  # if only one value, scale x- and y-direction the same
                        for i in range(0, len_points_list):
                            self.point_list[i] = (scale_coordinate(self.point_list[i][0], values[0]),
                            scale_coordinate(self.point_list[i][1], values[0]))
                    elif len(values) == 2:  # scale x- and y-coordinates to according values
                        for i in range(0, len_points_list):
                            self.point_list[i] = (scale_coordinate(self.point_list[i][0], values[0]),
                            scale_coordinate(self.point_list[i][1], values[1]))
                    else:
                        svg_polyline_logger.warning(f"unknown scale entry in values, {len(values)}")
                case 'skewX':
                    # skew in x-direction with tan(value[0])
                    for i in range(0, len_points_list):
                        self.point_list[i] = (
                            skew_x(self.point_list[i][0], self.point_list[i][1], values[0]), self.point_list[i][1])
                case 'skewY':
                    # skew in y-direction with tan(value[0])
                    for i in range(0, len_points_list):
                        self.point_list[i] = (
                            self.point_list[i][0], skew_y(self.point_list[i][0], self.point_list[i][1], values[0]))
                case 'matrix':
                    # if matrix has no translation - add zeros
                    if len(values) == 4:
                        values.append(0)
                        values.append(0)

                    for i in range(0, len_points_list):
                        self.point_list[i] = matrix_transformation(self.point_list[i][0], self.point_list[i][1], values)
                        """p_x = values[0] * self.point_list[i][0] + values[2] * self.point_list[i][1] + values[4]
                        p_y = values[1] * self.point_list[i][0] + values[3] * self.point_list[i][1] + values[5]
                        self.point_list[i] = (p_x, p_y)"""
