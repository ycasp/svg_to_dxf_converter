

class SvgPolygon:

    def __init__(self, element, svg_height):
        self.name = 'polygon'
        points = element.get('points')
        self.point_list = [(float(p.split(',')[0]), float(p.split(',')[1]))
            for p in points.strip().split()]
        self.transform = element.get('transform')