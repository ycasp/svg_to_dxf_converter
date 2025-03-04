from src.utilities import change_svg_to_dxf_coordinate


class SvgLine:

    def __init__(self, element, svg_height):
        self.name = 'line'
        self.x1 = float(element.get('x1'))
        self.y1 = change_svg_to_dxf_coordinate(float(element.get('y1')), svg_height)
        self.x2 = float(element.get('x2'))
        self.y2 = change_svg_to_dxf_coordinate(float(element.get('y2')), svg_height)
        self.transform = element.get('transform')

    def get_name(self):
        return self.name

    def scale(self, scale_x, scale_y):
        self.x1 = self.x1 * scale_x
        self.y1 = self.y1 * scale_y
        self.x2 = self.x2 * scale_x
        self.y2 = self.y2 * scale_y