from src.logging_config import setup_logger

svg_header_logger = setup_logger(__name__)


class SvgHeader:

    def __init__(self, element):
        self.name = 'header'
        self.view_box = extract_view_box(element.get('viewBox'))

        if element.get('width') is not None:
            self.width = extract_header_width(element.get('width'))
        else:
            svg_header_logger.info('no width was specified in svg file - width is taken from view box')
            self.width = self.view_box[2]

        if element.get('height') is not None:
            self.height = extract_header_height(element.get('height'))
        else:
            svg_header_logger.info('no height was specified in svg file - height is taken from view box')
            self.height = self.view_box[3]

    def get_name(self):
        return self.name

    def get_header_width(self):
        return self.width

    def get_header_height(self):
        return self.height

    def scale(self, scale_x, scale_y):
        self.width = self.width * scale_x
        self.height = self.height * scale_y
        self.view_box = [self.view_box[0], self.view_box[1], self.width, self.height]


def extract_header_width(width_string):
    if 'px' in width_string:
        width_string = width_string.replace('px', '')
        return float(width_string) * 25.4 / 96
    if 'mm' in width_string:
        width_string = width_string.replace('mm', '')
        return float(width_string)

    svg_header_logger.info(f"unknown width unit: {width_string}")
    return 0


def extract_header_height(height_string):
    if 'px' in height_string:
        height_string = height_string.replace('px', '')
        return float(height_string) * 25.4 / 96
    if 'mm' in height_string:
        height_string = height_string.replace('mm', '')
        return float(height_string)

    svg_header_logger.info(f"unknown height unit: {height_string}")
    return 0


def extract_view_box(view_box_string):
    x_left, y_high, width, height = map(float, view_box_string.split())
    return [x_left, y_high, width, height]
