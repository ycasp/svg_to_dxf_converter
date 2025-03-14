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

        :param svg_polyline: SvgPolyline, to be transformed in to dxf, already transformed and changed into cartesian coordinates
        """
        # extract the point_list from SvgPolyline
        self.points_list = svg_polyline.point_list

    def draw_dxf_polyline(self, msp):
        """
        Adds polyline to modelspace of dxf file.

        :param msp: Modelspace of dxf file
        :return: -
        """
        # add the lines to model space, only closed if last point = first point, but this is done manually - thus close = False
        msp.add_lwpolyline(self.points_list, close=False)
