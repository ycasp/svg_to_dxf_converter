import math

from src.utilities import calculate_euclidean_norm


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

    def __init__(self, svg_ellipse, start_param=0, end_param=2 * math.pi):
        # transformation message: until now, only rotation
        self.center = (svg_ellipse.center_x, svg_ellipse.center_y)
        norm_x = calculate_euclidean_norm(svg_ellipse.radius_x)
        norm_y = calculate_euclidean_norm(svg_ellipse.radius_y)

        if norm_x >= norm_y:
            self.mayor_axis = svg_ellipse.radius_x
            self.ratio = norm_y / norm_x
        else:
            self.mayor_axis = svg_ellipse.radius_y
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
