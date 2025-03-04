from svgpathtools import parse_path

class SvgPath:

    def __init__(self, element, svg_height):
        self.name = 'path'
        self.path = element.get('d')
        self.transform = element.get('transform')

    def get_name(self):
        return self.name

    def scale(self, scale_x, scale_y):
        parsed_path = parse_path(self.path)
        scaled_path = parsed_path.scale(scale_x, scale_y)
        self.path = scaled_path.d()