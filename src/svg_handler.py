import xml.etree.ElementTree as ET

from src.utilities import scale_rectangle

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
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Print the root tag (should be <svg>)
    print("Root tag:", root.tag)

    # Iterate through elements in the SVG
    #for element in root.iter():
    #    print(element.tag, element.attrib)

    return root

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
            height = height.replace('px','')
            return float(height) * 25.4 / 96 # 96 dpi standard for svg
        height = height.replace('mm', '')
        # TODO check if there are other measures missing
        return float(height)

    # if height is not given in svg-header, take it from view box
    view_box = root.attrib.get('viewBox')
    if view_box:
        _, _, _, box_height = map(float, view_box.split())
        return box_height

    # if none is specified
    print('no height parameter specified :(') # TODO handle error properly
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
            width = width.replace('px','')
            return float(width) * 25.4 / 96 # 96 dpi standard for svg
        width = width.replace('mm', '')
        # TODO check if there are other measures missing
        return float(width)

    # if height is not given in svg-header, take it from view box
    view_box = root.attrib.get('viewBox')
    if view_box:
        _, _, box_width, _ = map(float, view_box.split())
        return box_width

    # if none is specified
    print('no height parameter specified :(') # TODO handle error properly
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
    # calculate scaling in x/y-direction
    scale_x = new_width / get_svg_width(root)
    scale_y = new_height / get_svg_height(root)

    # set new width and height
    root.set('width', str(new_width) + 'mm')
    root.set('height', str(new_height) + 'mm')
    root.set('viewBox', '0 0 ' + str(new_width) + ' ' + str(new_height))

    # iterate through svg content
    for element in root.iter():
        match element.tag:
            case '{http://www.w3.org/2000/svg}circle':
                print(element.tag, element.attrib)
            case '{http://www.w3.org/2000/svg}ellipse':
                print(element.tag, element.attrib)
            case '{http://www.w3.org/2000/svg}rect':
                scale_rectangle(element, scale_x, scale_y)
            case '{http://www.w3.org/2000/svg}line':
                print(element.tag, element.attrib)
            case '{http://www.w3.org/2000/svg}polygone':
                print(element.tag, element.attrib)
            case '{http://www.w3.org/2000/svg}path':
                print(element.tag, element.attrib)
            case _:
                pass #TODO proper error handling

    return root