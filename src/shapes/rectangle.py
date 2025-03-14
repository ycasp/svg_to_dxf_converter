import math

from src.utilities import calculate_euclidean_norm


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

    def __init__(self, svg_rectangle):
        """
        Initialize a rectangle, which is ready to be written into dxf file.

        :param svg_rectangle: SvgRectangle, to be written into dxf file, already transformed and changed to dxf coordinates
        """
        # extract values from SvgRectangle
        self.x = svg_rectangle.x
        self.y = svg_rectangle.y
        self.rect_width = svg_rectangle.rect_width
        self.rect_height = svg_rectangle.rect_height
        self.rx = svg_rectangle.rx
        self.ry = svg_rectangle.ry

    def draw_dxf_rect(self, msp):
        """
        Draws a rectangle form the given svg data (from a rect attribute) into a dxf modelspace
        :param msp: dxf model space, where the figures are written into
        :return: -
        """
        # determine if corners are rounded or not
        if self.rx == (0, 0) and self.ry == (0, 0):
            # calculate the vertices of the rectangle
            vertices = [(self.x, self.y), (self.x + self.rect_width[0], self.y + self.rect_width[1]),
                (self.x + self.rect_width[0] + self.rect_height[0], self.y + self.rect_width[1] + self.rect_height[1]),
                (self.x + self.rect_height[0], self.y + self.rect_height[1])]
            # add it to the modelspace and close the figure
            msp.add_lwpolyline(vertices, close=True)
        else:
            # if corners are rounded, add it with rounded corners (= quarter elliptic arcs)
            self.draw_rounded_rectangle(msp)

    def draw_rounded_rectangle(self, msp):
        """
        Draws a rectangle with rounded corners into the model space.
        :param msp: dxf modelspace, where the figures are written into
        :return: -
        """
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
        self.y + self.rect_width[1] + self.rect_height[1] - self.rx[1])
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

        # determine major axis and ratio
        norm_rx = calculate_euclidean_norm(self.rx)
        norm_ry = calculate_euclidean_norm(self.ry)

        if norm_rx >= norm_ry:
            major_axis = self.rx
            ratio = norm_ry / norm_rx
        else:
            major_axis = self.ry
            ratio = norm_rx / norm_ry
            # if y is mayor axis, rotate back by 1/2*pi, as 0*pi == y-axis (not as always x-axis)
            rot_flag = 1 / 2 * math.pi

        # top right arc
        c1 = (self.x + self.rect_width[0] - self.rx[0] - self.ry[0],
        self.y + self.rect_width[1] - self.rx[1] - self.ry[1])
        msp.add_ellipse(center=c1, major_axis=major_axis, ratio=ratio,
                        start_param=0 - rot_flag, end_param=1 / 2 * math.pi - rot_flag)

        # bottom right arc
        c2 = (self.x + self.rect_width[0] + self.rect_height[0] - self.rx[0] + self.ry[0],
        self.y + self.rect_width[1] + self.rect_height[1] - self.rx[1] + self.ry[1])
        msp.add_ellipse(center=c2, major_axis=major_axis, ratio=ratio,
                        start_param=3 / 2 * math.pi - rot_flag, end_param=2 * math.pi - rot_flag)

        # bottem left arc
        c3 = (self.x + self.rect_height[0] + self.rx[0] + self.ry[0],
        self.y + self.rect_height[1] + self.rx[1] + self.ry[1])
        msp.add_ellipse(center=c3, major_axis=major_axis, ratio=ratio,
                        start_param=math.pi - rot_flag, end_param=3 / 2 * math.pi - rot_flag)

        # top left arc
        c4 = (self.x + self.rx[0] - self.ry[0],
        self.y + self.rx[1] - self.ry[1])
        msp.add_ellipse(center=c4, major_axis=major_axis, ratio=ratio,
                        start_param=1 / 2 * math.pi - rot_flag, end_param=math.pi - rot_flag)
