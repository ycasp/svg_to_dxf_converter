import xml.etree.ElementTree as ElementTree
from xml.etree.ElementTree import ParseError

from src.scaling_functions import scale_rectangle, scale_circle, scale_ellipse, scale_line, scale_path, scale_polygon
from src.svg_shapes import *

svg_logger = setup_logger(__name__)


def read_svg_file(name):
    """
    Reads in the svg file under the path given by "name".
    Parses into an iterable, containing all svg elements in the file.
    This is done with xml.etree.ElementTree package.

    :param name: Path of the svg file, we want to convert.
    :return: root, iterable with all svg entities in the file
    """
    # Path to your SVG file
    file_path = name

    # Parse the SVG file
    try:
        tree = ElementTree.parse(file_path)
        root = tree.getroot()

        svg_figures = []

        header = SvgHeader(root)
        svg_height = header.get_header_height()
        svg_figures.append(header)

        # iterate through svg content
        for element in root.iter():
            match element.tag:
                # case '{http://www.w3.org/2000/svg}svg':
                #    header = SvgHeader(element)
                #    svg_height = header.get_header_height()
                #    svg_figures.append(header)
                case '{http://www.w3.org/2000/svg}circle':
                    circle = SvgCircle(element, svg_height)
                    if circle.radius_y == 0:
                        svg_figures.append(circle)
                    else:  # circle.radius_y != 0:
                        element = {'cx': circle.center_x, 'cy': (-1) * circle.center_y, 'rx': circle.radius,
                            'ry': circle.radius_y}
                        ellipse = SvgEllipse(element, 0)
                        svg_figures.append(ellipse)
                case '{http://www.w3.org/2000/svg}ellipse':
                    svg_figures.append(SvgEllipse(element, svg_height))
                case '{http://www.w3.org/2000/svg}rect':
                    svg_figures.append(SvgRectangle(element, svg_height))
                case '{http://www.w3.org/2000/svg}line':
                    svg_figures.append(SvgLine(element, svg_height))
                case '{http://www.w3.org/2000/svg}polygon':
                    svg_figures.append(SvgPolygon(element, svg_height))
                case '{http://www.w3.org/2000/svg}polyline':
                    svg_figures.append(SvgPolyline(element, svg_height))
                case '{http://www.w3.org/2000/svg}path':
                    svg_figures.append(SvgPath(element, svg_height))
                case _:
                    svg_logger.info(f"svg_element without matching figure tag: {element.tag}: {element.attrib}")

        return svg_figures
    except ParseError as parseErr:
        svg_logger.exception(parseErr)
    except FileNotFoundError as pathErr:
        raise FileNotFoundError(pathErr)


def get_svg_height(root):
    """
    Gets the height of the svg file, specified in the header.
    If in pixel, the height is converted to millimeter.
    If no height is specified, the method returns 0.

    :param root: Iterable, containing all the elements and infos to a svg file
    :return: height (float): returns the height in mm (max. y-axis) specified in the svg header, or 0 if none is specified
    """
    # get the height parameter of the svg-header, replace all measures to remain with a number
    height = root.attrib.get('height')
    if height:
        if 'px' in height:
            height = height.replace('px', '')
            return float(height) * 25.4 / 96  # 96 dpi standard for svg
        height = height.replace('mm', '')
        # TODO check if there are other measures missing
        return float(height)

    # if height is not given in svg-header, take it from view box
    view_box = root.attrib.get('viewBox')
    if view_box:
        _, _, _, box_height = map(float, view_box.split())
        return box_height

    # if none is specified
    svg_logger.warning("no height found in svg file")
    return 0


def get_svg_width(root):
    """
    Gets the width of the svg file, specified in the header.
    If in pixel, the width is converted to millimeter.
    If no width is specified, the method returns 0.

    :param root: Iterable, containing all the elements and infos to a svg file
    :return: width (float): returns the width in mm (max. x-axis) specified in the svg header, or 0 if none is specified
    """
    # get the width parameter of the svg-header, replace all measures to remain with a number
    width = root.attrib.get('width')
    if width:
        if 'px' in width:
            width = width.replace('px', '')
            return float(width) * 25.4 / 96  # 96 dpi standard for svg
        width = width.replace('mm', '')
        # TODO check if there are other measures missing
        return float(width)

    # if height is not given in svg-header, take it from view box
    view_box = root.attrib.get('viewBox')
    if view_box:
        _, _, box_width, _ = map(float, view_box.split())
        return box_width

    # if none is specified
    svg_logger.warning("no width found in svg file")
    return 0


def print_root(root):
    """
    Prints all the elements in root.
    :param root: svg file content
    :return: -
    """
    for element in root.iter():
        print(element.tag, element.attrib)
        print('\n')


def scale_file(root, new_width, new_height):
    """
    Scales all figures in a svg file. Changes the attributes in the tree.

    :param root: tree with svg figures
    :param new_width: new width in mm
    :param new_height: new height in mm
    :return: scaled svg content in a root
    """

    old_width = get_svg_width(root)
    old_height = get_svg_height(root)

    try:
        old_ratio = old_height / old_width
        new_ratio = new_height / new_width
    except ZeroDivisionError as e:
        svg_logger.exception(e)
        return root
    else:
        if old_ratio != new_ratio:
            svg_logger.warning(f"format of file is changed badly - new ratio: {new_ratio} != old ratio: {old_ratio}")

    # calculate scaling in x/y-direction
    scale_x = new_width / old_width
    scale_y = new_height / old_height

    # set new width and height
    root.set('width', str(new_width) + 'mm')
    root.set('height', str(new_height) + 'mm')
    root.set('viewBox', '0 0 ' + str(new_width) + ' ' + str(new_height))

    # iterate through svg content
    for element in root.iter():
        match element.tag:
            case '{http://www.w3.org/2000/svg}circle':
                scale_circle(element, scale_x, scale_y)
                # cut rules
            case '{http://www.w3.org/2000/svg}ellipse':
                scale_ellipse(element, scale_x, scale_y)
            case '{http://www.w3.org/2000/svg}rect':
                scale_rectangle(element, scale_x, scale_y)
            case '{http://www.w3.org/2000/svg}line':
                scale_line(element, scale_x, scale_y)
            case '{http://www.w3.org/2000/svg}polygon':
                scale_polygon(element, scale_x, scale_y)
            case '{http://www.w3.org/2000/svg}path':
                scale_path(element, scale_x, scale_y)
            case _:
                pass  # TODO proper error handling

    return root


def scale_file_param(svg_figures, scale_x, scale_y):
    """
    Scales all figures in a svg file. Changes the attributes in the tree.

    :param svg_figures: list with svg figures
    :param scale_x: integer scaling factor in x direction
    :param scale_y: integer scaling factor in y direction
    :return: scaled svg content in a root
    """

    # here no error handling, as we have no (possible) division by zero

    # calculate scaling in x/y-direction
    new_width = scale_x * svg_figures[0].get_header_width()
    new_height = scale_y * svg_figures[0].get_header_height()

    # set new width and height
    for figures in svg_figures:
        figures.scale(scale_x, scale_y)

    return svg_figures
