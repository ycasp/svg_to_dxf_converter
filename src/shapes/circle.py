class Circle:
    """
    Represents a circle with given center and radius.

    Attributes:
        center (tuple): x- and y-coordinates of the center of the circle.
        radius (float): radius of the circle.
    """

    def __init__(self, svg_circle):
        self.center = (svg_circle.center_x, svg_circle.center_y)
        self.radius = svg_circle.radius

    def draw_dxf_circle(self, msp):
        """
        Adds a circle with center (x,y) and radius r to the dxf file.

        :param msp: dxf file we are want the circle to be part of
        :return: -
        """
        msp.add_circle(self.center, self.radius)
