import math

from src.utilities import calculate_euclidean_norm


class Ellipse:
    """
    Represents the ellipse-entity for the dxf file.

    Attributes:
        center (tuple): center of the ellipse (in cartesian coordinates), already rotated if stated
        mayor_axis: dominating axis
        ratio: minor axis / major axis
        start_param: start of the ellipsis (if only part of the ellipse, in radian from 0 to 2pi), default 0
        end_param: end of the ellipsis (if only part of the ellipse, in radian form 0 to 2pi), default 2pi
    """

    def __init__(self, svg_ellipse, start_param=0, end_param=2 * math.pi):
        """
        Initializes the "dxf"-ellipse from the SvgEllipse, which is transformed into dxf.
        :param svg_ellipse: SvgEllipse, already transformed, changed to cartesian coordinates
        :param start_param: float (from 0 to 2pi), start of elliptic arc
        :param end_param: float (from 0 to 2 pi), end of elliptic arc
        """

        # get the center from svgEllipse
        self.center = (svg_ellipse.center_x, svg_ellipse.center_y)

        # calculate norms of radii
        norm_x = calculate_euclidean_norm(svg_ellipse.radius_x)
        norm_y = calculate_euclidean_norm(svg_ellipse.radius_y)

        # determine mayor axis and ratio
        if norm_x >= norm_y:
            self.mayor_axis = svg_ellipse.radius_x
            self.ratio = norm_y / norm_x
        else:
            self.mayor_axis = svg_ellipse.radius_y
            self.ratio = norm_x / norm_y
            # if y-axis is mayor, start and end parameter is + 1/2 * pi (0 = y-axis)
            # thus rotate back
            start_param = start_param - 1 / 2 * math.pi
            end_param = end_param - 1 / 2 * math.pi

        # set start/end parameter
        self.start_param = start_param
        self.end_param = end_param

    def draw_dxf_ellipse(self, msp):
        """
        Adds ellipse object to a dxf file.

        :param msp: Modelspace of the dxf file.
        :return: -
        """
        msp.add_ellipse(self.center, self.mayor_axis, self.ratio, self.start_param, self.end_param)
