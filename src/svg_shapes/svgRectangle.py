from src.utilities import change_svg_to_dxf_coordinate


class SvgRectangle:

    def __init__(self,element, svg_height):
        self.name = 'rectangle'

        self.x = float(element.get('x'))
        self.y = change_svg_to_dxf_coordinate(float(element.get('y')), svg_height)

        self.rect_width = float(element.get('width'))
        self.rect_height = (-1) * float(element.get('height'))

        self.rx = float(element.get('rx') or 0)
        self.ry = float(element.get('ry') or 0)
        self.transform = element.get('transform')

    def get_name(self):
        return self.name

    def scale(self, scale_x, scale_y):
        self.x = self.x * scale_x
        self.y = self.y * scale_y

        self.rect_width = self.rect_width * scale_x
        self.rect_height = self.rect_height * scale_y

        if self.rx != 0:
            self.rx = self.rx * scale_x

        if self.ry != 0:
            self.ry = self.ry * scale_y