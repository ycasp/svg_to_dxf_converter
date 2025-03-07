import math

from src.shapes.ellipse import Ellipse
from src.svg_shapes import SvgEllipse
from src.utilities import change_svg_to_dxf_coordinate, export_rotation, rotate_clockwise_around_svg_origin, \
    calculate_euclidean_norm


class Rectangle:
    """
    Represents a rectangle object.

    Attributes
        x, y (float): coordinates of the top left corner, y-coordinate is converted to cartesian coordinates
        width (float): length of the x-coordinate direction
        rect_height (float): height of the rectangle in y-coord (top -> down direction, is negative)
        transformation (string): transformation message of the rectangle, infos about rotation
        rx, ry (floats): radius of rounded corner of the rectangle (default value = 0)
        rot_angle (float): rotation angle of the rectangle (in degree) given in the transformation message (default value 0)
    """

    def __init__(self, svg_rectangle, rot_angle=0):

        self.x = svg_rectangle.x
        self.y = svg_rectangle.y
        self.rect_width = svg_rectangle.rect_width
        self.rect_height = svg_rectangle.rect_height
        self.rx = svg_rectangle.rx
        self.ry = svg_rectangle.ry

    # draws a rectangle form the given svg data (from a rect attribute) into a dxf modelspace
    def draw_dxf_rect(self, msp, height):
        if self.rx == (0, 0) and self.ry == (0, 0):
            vertices = [ (self.x, self.y), (self.x + self.rect_width[0], self.y + self.rect_width[1]),
                (self.x + self.rect_width[0] + self.rect_height[0], self.y + self.rect_width[1] + self.rect_height[1]),
                (self.x + self.rect_height[0], self.y + self.rect_height[1])]
            msp.add_lwpolyline(vertices, close=True)
        else:
            self.draw_rounded_rectangle(msp, height)

    def draw_rounded_rectangle(self, msp, height):
        # define corner points
        # top left vertice, after arc
        p1 = (self.x + self.rx[0],
                self.y + self.rx[1])
        # top right vertice, before arc
        p2 = (self.x + self.rect_width[0] - self.rx[0],
                self.y + self.rect_width[1] - self.rx[1])
        # top right vertice, after arc
        p3 = (self.x + self.rect_width[0] - self.ry[0],
                self.y + self.rect_width[1] - self.ry[1])
        # bottem right vertice, before arc
        p4 = (self.x + self.rect_width[0] + self.rect_height[0] + self.ry[0],
                self.y + self.rect_width[1] + self.rect_height[1] + self.ry[1])
        # bottom right vertice, after arc
        p5 = (self.x + self.rect_width[0] + self.rect_height[0] - self.rx[0],
                self.y + self.rect_width[1] +self.rect_height[1] - self.rx[1])
        # bottom left vertice, before arc
        p6 = (self.x + self.rect_height[0] + self.rx[0],
                self.y + self.rect_height[1] + self.rx[1])
        # bottom left vertice, after arc
        p7 = (self.x + self.rect_height[0] + self.ry[0],
                self.y + self.rect_height[1] + self.ry[1])
        # top left vertice, before arc
        p8 = (self.x - self.ry[0],
                self.y - self.ry[1])

        # add edges
        msp.add_line(p1, p2)  # top edge
        msp.add_line(p3, p4)  # right edge
        msp.add_line(p5, p6)  # bottom ege
        msp.add_line(p7, p8)  # left edge

        # add rounded corners
        rot_flag = 0

        # determine major axis
        norm_rx = calculate_euclidean_norm(self.rx)
        norm_ry = calculate_euclidean_norm(self.ry)

        if norm_rx >= norm_ry:
            major_axis = self.rx
            ratio = norm_ry / norm_rx
        else:
            major_axis = self.ry
            ratio = norm_rx / norm_ry
            rot_flag = 1/2 * math.pi

        # top right arc
        c1 = (self.x + self.rect_width[0] - self.rx[0] - self.ry[0],
                self.y + self.rect_width[1] - self.rx[1] - self.ry[1])
        msp.add_ellipse(center= c1, major_axis= major_axis, ratio= ratio,
                        start_param= 0 - rot_flag, end_param= 1/2 * math.pi - rot_flag)

        # bottom right arc
        c2 = (self.x + self.rect_width[0] + self.rect_height[0] - self.rx[0] + self.ry[0],
                self.y + self.rect_width[1] + self.rect_height[1] - self.rx[1] + self.ry[1])
        msp.add_ellipse(center=c2, major_axis=major_axis, ratio=ratio,
                        start_param=3 / 2 * math.pi - rot_flag, end_param= 2 * math.pi - rot_flag)

        # bottem left arc
        c3 = (self.x + self.rect_height[0] + self.rx[0] + self.ry[0],
                self.y + self.rect_height[1] + self.rx[1] + self.ry[1])
        msp.add_ellipse(center=c3, major_axis=major_axis, ratio=ratio,
                        start_param=math.pi - rot_flag, end_param=3 / 2 * math.pi - rot_flag)

        # top left arc
        c4 = (self.x + self.rx[0] - self.ry[0],
                self.y + self.rx[1] - self.ry[1])
        msp.add_ellipse(center=c4, major_axis=major_axis, ratio=ratio,
                        start_param=1/2 * math.pi - rot_flag, end_param= math.pi - rot_flag)
        """
        rx = self.rx
        ry = self.ry
        # define corner points
        p1 = rotate_clockwise_around_svg_origin(self.x + rx, self.y, self.rot_angle,
                                                height)  # top left vertice, after arc
        p2 = rotate_clockwise_around_svg_origin(self.x + self.width - rx, self.y, self.rot_angle,
                                                height)  # top right vertice, before arc, rotation included
        p3 = rotate_clockwise_around_svg_origin(self.x + self.width, self.y - ry, self.rot_angle,
                                                height)  # top right vertice, after arc, rotation included
        p4 = rotate_clockwise_around_svg_origin(self.x + self.width, self.y + self.rect_height + ry, self.rot_angle,
                                                height)  # bottom right vertice, before arc, rotation included
        p5 = rotate_clockwise_around_svg_origin(self.x + self.width - rx, self.y + self.rect_height, self.rot_angle,
                                                height)  # bottom right vertice, after arc, rotation included
        p6 = rotate_clockwise_around_svg_origin(self.x + rx, self.y + self.rect_height, self.rot_angle,
                                                height)  # bottom left vertice, before arc, rotation included
        p7 = rotate_clockwise_around_svg_origin(self.x, self.y + self.rect_height + ry, self.rot_angle,
                                                height)  # bottom left vertice, after arc, rotation included
        p8 = rotate_clockwise_around_svg_origin(self.x, self.y - ry, self.rot_angle,
                                                height)  # top left vertice, before arc, rotation included

        # add edges
        msp.add_line(p1, p2)  # top edge
        msp.add_line(p3, p4)  # right edge
        msp.add_line(p5, p6)  # bottom ege
        msp.add_line(p7, p8)  # left edge

        # add arcs / ellipses
        # top right corner
        top_right_ellipse_element = {'cx':self.x + self.width - rx, 'cy':(self.y - ry - height) * (-1), 'rx':rx, 'ry':ry,
        'transform': f"rotate({self.rot_angle})"}
        top_right_ellipse = SvgEllipse(top_right_ellipse_element, height)
        c1 = Ellipse(top_right_ellipse, 0, 1 / 2 * math.pi)
        c1.draw_dxf_ellipse(msp)

        # bottom right corner
        bottom_right_ellipse_element = {'cx':self.x + self.width - rx, 'cy':(self.y + self.rect_height + ry - height) * (-1), 'rx':rx, 'ry':ry,
        'transform': f"rotate({self.rot_angle})"}
        bottom_right_ellipse = SvgEllipse(bottom_right_ellipse_element, height)
        c2 = Ellipse(bottom_right_ellipse, 3 / 2 * math.pi, 2 * math.pi)
        c2.draw_dxf_ellipse(msp)
        # bottom left corner
        bottom_left_ellipse_element = {'cx':self.x + rx, 'cy':(self.y + self.rect_height + ry - height) * (-1), 'rx':rx, 'ry':ry,
        'transform': f"rotate({self.rot_angle})"}
        bottom_right_ellipse = SvgEllipse(bottom_left_ellipse_element, height)
        c3 = Ellipse(bottom_right_ellipse, math.pi, 3 / 2 * math.pi)
        c3.draw_dxf_ellipse(msp)
        # top left corner
        top_left_ellipse_element = {'cx': self.x + rx, 'cy': (self.y - ry - height) * (-1), 'rx': rx, 'ry': ry,
            'transform': f"rotate({self.rot_angle})"}
        top_left_ellipse = SvgEllipse(top_left_ellipse_element, height)
        c4 = Ellipse(top_left_ellipse, 1 / 2 * math.pi, math.pi)
        c4.draw_dxf_ellipse(msp)
        """

