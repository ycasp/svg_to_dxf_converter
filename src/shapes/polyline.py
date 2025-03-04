from src.utilities import change_svg_to_dxf_coordinate


class Polyline:
    """
    Represents a Polyline with several points in a point list.

    Attributes
        points_list:    a list of tuples (x,y) with points
    """

    def __init__(self, svg_polyline):
        """
        Initializes the polyline object.
        Already changes the svg-coordinates to cartesian coordinates.

        :param points: string of points form svg file
        :param height: height of the svg file to change coordinates
        """
        self.points_list = svg_polyline.point_list

    def draw_dxf_polyline(self, msp):
        """
        Adds polyline to modelspace of dxf file.

        :param msp: Modelspace of dxf file
        :return: -
        """
        msp.add_lwpolyline(self.points_list, close=False)
