from src.utilities import change_svg_to_dxf_coordinate


class Circle:
    """
    Represents a circle with given center and radius.

    Attributes:
        center (tuple): x- and y-coordinates of the center of the circle.
        radius (float): radius of the circle.
    """

    def __init__(self,cx, cy , radius, height):
        """
        Initializes the circle object.

        :param cx: x-coordinate of the center
        :param cy: y-coordinate of the center (svg coordinate)
        :param radius: radius of the center
        :param height: height of the svg file (to transform svg coordinate to cartesian coordinates)
        """
        center_y = change_svg_to_dxf_coordinate(float(cy), height)
        self.center = (float(cx), center_y)
        self.radius = float(radius)

    def draw_dxf_circle(self, msp):
        """
        Adds a circle with center (x,y) and radius r to the dxf file.

        :param msp: dxf file we are want the circle to be part of
        :return: -
        """
        msp.add_circle(self.center, self.radius)