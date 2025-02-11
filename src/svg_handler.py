import xml.etree.ElementTree as ET

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

def change_svg_to_dxf_coordinate(y, height):
    """
    Changes the svg coordinates to cartesian coordinates (y-axis in svg is from top to down).

    :param y: y coordinate in svg file
    :param height: height of svg file
    :return: y coordinate in cartesian coordinate
    """
    return (-1) * y + height

def print_root(root):
    for element in root.iter():
        print(element.tag, element.attrib)
        print('\n')