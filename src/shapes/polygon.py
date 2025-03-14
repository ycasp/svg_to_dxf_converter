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

        :param svg_polygon: SvgPolygon, polygon to be transformed into dxf, already transformed and changed to cartesian coordinates
        """
        # extract the polygon points from the SvgPolygon
        self.points_list = svg_polygon.point_list

    def draw_dxf_polygon(self, msp):
        """
        Adds polygon to modelspace of dxf file.

        :param msp: Modelspace of dxf file
        :return: -
        """
        # add the polygon as polyline to the modelspace, a polygon is always closed - thus close = True
        msp.add_lwpolyline(self.points_list, close=True)
