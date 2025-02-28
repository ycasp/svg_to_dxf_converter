

class SvgLine:

    def __init__(self, element):
        self.name = 'line'
        self.x1 = float(element.get('x1'))
        self.y1 = float(element.get('y1'))
        self.x2 = float(element.get('x2'))
        self.y2 = float(element.get('y2'))
        self.transform = element.get('transform')