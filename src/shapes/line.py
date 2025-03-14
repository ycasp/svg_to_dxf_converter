class Line:
    """
    Represent a Line with start point and end point.

    Attributes:
        start (tuple): start point of the line
        end (tuple): endpoint of the line
    """

    def __init__(self, svg_line):
        """
        Initializes the line object.

        :param x1: x-coordinate of start point
        :param y1: y-coordinate (in svg format) of start point
        :param x2: x-coordinate of end point
        :param y2: y-coordinate (in svg format) of end point
        :param height: height of svg format, used to convert y-coordinates in to cartesian form
        """
        self.start = (svg_line.x1, svg_line.y1)
        self.end = (svg_line.x2, svg_line.y2)

    def draw_dxf_line(self, msp):
        """
        Adds line to the modelspace of dxf file.

        :param msp: Modelspace od dxf file
        :return: -
        """
        msp.add_line(self.start, self.end)
