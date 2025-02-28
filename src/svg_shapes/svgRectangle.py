

class SvgRectangle:

    def __init__(self,element, svg_height):
        self.name = 'rectangle'
        self.x = float(element.get('x'))
        self.y = float(element.get('y'))
        self.rect_width = float(element.get('width'))
        self.rect_height = float(element.get('height'))
        self.rx = float(element.get('rx') or 0)
        self.ry = float(element.get('ry') or 0)
        self.transform = element.get('transform')

