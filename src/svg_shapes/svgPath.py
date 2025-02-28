

class SvgPath:

    def __init__(self, element):
        self.name = 'path'
        self.path = element.get('d')
        self.transform = element.get('transform')