from src.utilities import change_svg_to_dxf_coordinate


class SvgPolyline:

    def __init__(self, element, svg_height):
        self.name = 'polyline'
        points = element.get('points')
        self.point_list = [(float(p.split(',')[0]), change_svg_to_dxf_coordinate(float(p.split(',')[1]), svg_height))
            for p in points.strip().split()]
        self.transform = element.get('transform')

    def get_name(self):
        return self.name

    def scale(self, scale_x, scale_y):
        scaled_points = []

        for point in self.point_list:
            scaled_points.append((point[0] * scale_x, point[1] * scale_y))

        self.point_list = scaled_points

