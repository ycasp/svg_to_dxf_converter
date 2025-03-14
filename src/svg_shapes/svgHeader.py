from src.logging_config import setup_logger

svg_header_logger = setup_logger(__name__)


class SvgHeader:
    """
    Represents the header of a svg file.

    Attributes:
            view_box: array, len 4, x_min, y_min, width, height
            width: float, width of file (in mm)
            height: float, height of file (in mm)
    """

    def __init__(self, element):
        """
        Initializes the SvgHeader element.
        :param element: dictionary, svg header
        """
        self.name = 'header'
        # get the view box
        self.view_box = extract_view_box(element.get('viewBox'))

        # get the width
        if element.get('width') is not None:
            self.width = extract_header_width(element.get('width'))
        else:
            svg_header_logger.info('no width was specified in svg file - width is taken from view box')
            self.width = self.view_box[2]

        # extract the height
        if element.get('height') is not None:
            self.height = extract_header_height(element.get('height'))
        else:
            svg_header_logger.info('no height was specified in svg file - height is taken from view box')
            self.height = self.view_box[3]

    def get_name(self):
        """
        Getter for name.
        :return: 'header'
        """
        return self.name

    def get_header_width(self):
        """
        Getter for width
        :return: header.width (float)
        """
        return self.width

    def get_header_height(self):
        """
        Getter for height.
        :return: header.height (float)
        """
        return self.height

    def set_header_width(self, width):
        """
        Setter for width.
        :param width: float, (new) width for svg file
        :return: -
        """
        self.width = width

    def set_header_height(self, height):
        """
        Setter for height.
        :param height: float, (new) height for svg file
        :return: -
        """
        self.height = height

    def scale(self, scale_x, scale_y):
        """
        Scales the header.
        :param scale_x: float, scaling parameter in x-direction
        :param scale_y: float, scaling parameter in y-direction
        :return: -
        """
        self.width = self.width * scale_x
        self.height = self.height * scale_y
        self.view_box = [self.view_box[0], self.view_box[1], self.width, self.height]


def extract_header_width(width_string):
    """
    Extract the file width
    :param width_string: string, containing the width, e.g. "300mm"
    :return: width, float
    """
    if 'px' in width_string:  # if file is in pixel
        # replace px with nothing, and calculate the width to mm
        width_string = width_string.replace('px', '')
        return float(width_string) * 25.4 / 96
    if 'mm' in width_string:
        # replace mm and return float
        width_string = width_string.replace('mm', '')
        return float(width_string)

    # if unknown unit or no width found, return 0
    svg_header_logger.info(f"unknown width unit: {width_string}")
    return 0


def extract_header_height(height_string):
    """
    Extracts file height.
    :param height_string:  string, containing the height, e.g. "300mm"
    :return: -
    """
    if 'px' in height_string:  # if file is in pixel
        # replace px with nothing, and calculate the height to mm
        height_string = height_string.replace('px', '')
        return float(height_string) * 25.4 / 96
    if 'mm' in height_string:
        # replace mm and return float
        height_string = height_string.replace('mm', '')
        return float(height_string)

    # if unknown unit or no height found, return 0
    svg_header_logger.info(f"unknown height unit: {height_string}")
    return 0


def extract_view_box(view_box_string):
    """
    Extracts the view box from the svg file.
    :param view_box_string: string, of the form "x_min y_min width height"
    :return: array [x_min, y_min, width, height]
    """
    x_left, y_high, width, height = map(float, view_box_string.split())
    return [x_left, y_high, width, height]
