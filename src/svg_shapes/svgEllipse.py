
class SvgEllipse:

    def __init__(self, element):
        self.name = 'ellipse'
        self.center_x = float(element.get('cx'))
        self.center_y = float(element.get('cy'))
        self.radius_x = float(element.get('rx'))
        self.radius_y = float(element.get('ry'))
        self.transform = element.get('transform')