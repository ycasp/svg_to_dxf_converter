from src.utilities import change_svg_to_dxf_coordinate


class Polygon:
    """
    Represents a Polygon with several points in a point list.

    Attributes
        points_list:    a list of tuples (x,y) with points
    """

    def __init__(self, points, height):
        """
        Initializes the polygon object.
        Already changes the svg-coordinates to cartesian coordinates.

        :param points: string of points form svg file
        :param height: height of the svg file to change coordinates
        """
        self.points_list = [(float(p.split(',')[0]), change_svg_to_dxf_coordinate(float(p.split(',')[1]), height))
            for p in points.strip().split()]

    def draw_dxf_polygon(self, msp):
        """
        Adds polygon to modelspace of dxf file.

        :param msp: Modelspace of dxf file
        :return: -
        """
        msp.add_lwpolyline(self.points_list, close=True)
