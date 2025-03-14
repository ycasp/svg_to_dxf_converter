class Polygon:
    """
    Represents a Polygon with several points in a point list.

    Attributes
        points_list:    a list of tuples (x,y) with points
    """

    def __init__(self, svg_polygon):
        """
        Initializes the polygon object.
        Already changes the svg-coordinates to cartesian coordinates.

        :param points: string of points form svg file
        :param height: height of the svg file to change coordinates
        """
        self.points_list = svg_polygon.point_list

    def draw_dxf_polygon(self, msp):
        """
        Adds polygon to modelspace of dxf file.

        :param msp: Modelspace of dxf file
        :return: -
        """
        msp.add_lwpolyline(self.points_list, close=True)
