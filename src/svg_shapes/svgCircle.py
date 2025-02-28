

class SvgCircle:

    def __init__(self, segment, svg_height):
        self.figure = 'circle'
        self.transform = segment.get('transform')
        self.center_x = float(segment.get('cx'))
        self.center_y = float(segment.get('cy'))
        self.radius = float(segment.get('r'))

