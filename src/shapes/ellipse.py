import math

from src.utilities import change_svg_to_dxf_coordinate, export_rotation, rotate_clockwise_around_svg_origin


class Ellipse:
    """
    Represents the ellipse-entity for the dxf file.

    Attributes:
        transformation (string): Message of any transformation of the original object, e.g. rotation.
        rot_angle (float): Default 0, unless transformation has a rotation angle stated.
        center (tuple): center of the ellipse (in cartesian coordinates), already rotated if stated
        mayor_axis: dominating axis
        ratio: minor axis / major axis
        start_param: start of the ellipsis (if only part of the ellipse, in radian from 0 to 2pi), default 0
        end_param: end of the ellipsis (if only part of the ellipse, in radian form 0 to 2pi), default 2pi
    """

    def __init__(self, cx, cy, rx, ry, transformation, height, rot_angle=0, start_param=0, end_param=2 * math.pi):
        # transformation message: until now, only rotation
        self.transformation = transformation

        # looks for rotation in transformation message and extract rotation angle (in degree)
        self.rot_angle = rot_angle
        if self.transformation is not None:
            # check for rotation
            self.rot_angle = export_rotation(self.transformation)

        # converts the center to cartesian coordinates and rotation (if given)
        center_y = change_svg_to_dxf_coordinate(float(cy), height)
        self.center = rotate_clockwise_around_svg_origin(float(cx), center_y, self.rot_angle, height)

        # determine mayor and minor axis, as well as ratio = minor axis / mayor axis
        rotated_origin = rotate_clockwise_around_svg_origin(0, 0, self.rot_angle, height)
        rotated_x_axis = rotate_clockwise_around_svg_origin(float(rx), 0, self.rot_angle, height)
        rotated_y_axis = rotate_clockwise_around_svg_origin(0, float(ry), self.rot_angle, height)
        rotated_x_axis = (rotated_x_axis[0] - rotated_origin[0], rotated_x_axis[1] - rotated_origin[1])
        rotated_y_axis = (rotated_y_axis[0] - rotated_origin[0], rotated_y_axis[1] - rotated_origin[1])

        # calc the norms
        norm_x = (rotated_x_axis[0] ** 2 + rotated_x_axis[1] ** 2) ** 0.5
        norm_y = (rotated_y_axis[0] ** 2 + rotated_y_axis[1] ** 2) ** 0.5
        if norm_x >= norm_y:
            self.mayor_axis = rotated_x_axis
            self.ratio = norm_y / norm_x
        else:
            self.mayor_axis = rotated_y_axis
            self.ratio = norm_x / norm_y
            # if y-axis is mayor, start and end parameter are rotated + 1/2 * pi
            # thus rotate back
            start_param = start_param - 1 / 2 * math.pi
            end_param = end_param - 1 / 2 * math.pi

        # self.ratio = (minor_axis[0] ** 2 + minor_axis[1] ** 2) ** 0.5 / (self.mayor_axis[0] ** 2 + self.mayor_axis[1] ** 2) ** 0.5
        self.start_param = start_param
        self.end_param = end_param

    def draw_dxf_ellipse(self, msp):
        """
        Adds ellipse object to a dxf file.

        :param msp: Modelspace of the dxf file.
        :return: -
        """
        msp.add_ellipse(self.center, self.mayor_axis, self.ratio, self.start_param, self.end_param)
