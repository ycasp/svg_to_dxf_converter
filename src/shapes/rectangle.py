import math

from src.shapes.ellipse import Ellipse
from src.utilities import change_svg_to_dxf_coordinate, export_rotation, rotate_clockwise_around_svg_origin


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

    def __init__(self, x, y, width, rect_height, transformation, rx, ry, height, rot_angle=0):
        """
        Initializes a rectangle object
        :param x: x-coordinate of top left corner
        :param y: y-coordinate of top left corner (in svg format)
        :param width: lengths of rectangle in x-direction
        :param rect_height: height of rectangle in y-direction (svg format, positive but goes down)
        :param transformation: information about transformation of rectangle (like rotation)
        :param rx: radius in x-direction of rounded corners
        :param ry: radius in y-direction of rounded corners
        :param height: height of the svg file for coordinate transformation to cartesian coordinates
        :param rot_angle: rotation angle of the rectangle, in degree, around the point (0, height)
        """
        # x,y are coordinates of the top left corners
        self.x = float(x)
        self.y = change_svg_to_dxf_coordinate(float(y), height)
        # width is x-coord length of rect
        self.width = float(width)
        # rect_height is y-coord length of rect
        # as y-coord in svg and dxf is in different direction: * (-1)
        self.rect_height = (-1) * float(rect_height)
        # transformation message: until now, only rotation
        self.transformation = transformation

        # rx / ry are radius of rounded corners
        # if rx/ry is None, we have no radius in this direction --> ensures rx/ry is float, at least 0
        if rx is None:
            self.rx = 0
        else:
            self.rx = float(rx)

        if ry is None:
            self.ry = 0
        else:
            self.ry = float(ry)

        self.rot_angle = float(rot_angle)
        if self.transformation is not None:
            # check for rotation
            self.rot_angle, _, _ = export_rotation(self.transformation)

    # draws a rectangle form the given svg data (from a rect attribute) into a dxf modelspace
    def draw_dxf_rect(self, msp, height):
        """
        Adds rectangle to dxf file, as polyline.

        :param msp: Modelspace of dxf file, to add lines.
        :param height: Height of svg file, for coordinates transformation or rotation point
        :return: -
        """
        if self.rx == 0 and self.ry == 0:
            # Calculate rectangle vertices (DXF uses bottom-left origin)
            vertices = [
                rotate_clockwise_around_svg_origin(self.x, self.y, self.rot_angle, height),  # top left
                rotate_clockwise_around_svg_origin(self.x + self.width, self.y, self.rot_angle, height),  # top right
                rotate_clockwise_around_svg_origin(self.x + self.width, self.y + self.rect_height, self.rot_angle,
                                                   height),  # bottom right (height is < 0)
                rotate_clockwise_around_svg_origin(self.x, self.y + self.rect_height, self.rot_angle, height),
                # bottem left (height is < 0)
            ]
            # Add rectangle as a closed polyline
            msp.add_lwpolyline(vertices, close=True)
        elif self.rx != 0 and self.ry == 0:
            self.ry = self.rx
            self.draw_rounded_rectangle(msp, height)
        elif self.rx == 0 and self.ry != 0:
            self.rx = self.ry
            self.draw_rounded_rectangle(msp, height)
        elif self.rx != 0 and self.ry != 0:
            self.draw_rounded_rectangle(msp, height)

    def draw_rounded_rectangle(self, msp, height):
        # ensure that rx/ry are only half of width / height
        rx = ensure_applicable_radius(self.rx, self.width)
        ry = ensure_applicable_radius(self.ry, self.rect_height * (-1))

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
        c1 = Ellipse(self.x + self.width - rx, (self.y - ry - height) * (-1), rx, ry,
                     None, height, self.rot_angle, 0, 1 / 2 * math.pi)
        c1.draw_dxf_ellipse(msp)
        # bottom right corner
        c2 = Ellipse(self.x + self.width - rx, (self.y + self.rect_height + ry - height) * (-1), rx, ry,
                     None, height, self.rot_angle, 3 / 2 * math.pi, 2 * math.pi)
        c2.draw_dxf_ellipse(msp)
        # bottom left corner
        c3 = Ellipse(self.x + rx, (-1) * (self.y + self.rect_height + ry - height), rx, ry,
                     None, height, self.rot_angle, math.pi, 3 / 2 * math.pi)
        c3.draw_dxf_ellipse(msp)
        # top left corner
        c4 = Ellipse(self.x + rx, (-1) * (self.y - ry - height), rx, ry,
                     None, height, self.rot_angle, 1 / 2 * math.pi, math.pi)
        c4.draw_dxf_ellipse(msp)


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
