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

        :param svg_line: SvgLine, line to be transformed to dxf, already transformed and
                         changed to cartesian coordinates
        """
        # extract start-, and end-point form SvgLine
        self.start = (svg_line.x1, svg_line.y1)
        self.end = (svg_line.x2, svg_line.y2)

    def draw_dxf_line(self, msp):
        """
        Adds line to the modelspace of dxf file.

        :param msp: Modelspace od dxf file
        :return: -
        """
        msp.add_line(self.start, self.end)
