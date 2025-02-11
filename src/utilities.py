def change_svg_to_dxf_coordinate(y, height):
    """
    Changes the svg coordinates to cartesian coordinates (y-axis in svg is from top to down).

    :param y: y coordinate in svg file
    :param height: height of svg file
    :return: y coordinate in cartesian coordinate
    """
    return (-1) * y + height

# scaling functions

def scale_rectangle(element, scale_x, scale_y):
    # scale x - top left corner x-coordinate
    new_x = float(element.attrib.get('x')) * scale_x
    element.set('x', str(new_x))

    # scale y - top left corner y-coordinate
    new_y = float(element.attrib.get('y')) * scale_y
    element.set('y', str(new_y))

    # scale width
    new_width = float(element.attrib.get('width')) * scale_x
    element.set('width', str(new_width))

    # scale height
    new_height = float(element.attrib.get('height')) * scale_y
    element.set('height', str(new_height))

    # scale rx - radius of rounded corners in x-direction
    rx = element.attrib.get('rx')
    if rx is not None and rx != 0:
        element.set('rx', str(float(rx) * scale_x))

    # scale ry - radius of rounded corners in y-direction
    ry = element.attrib.get('ry')
    if ry is not None and ry != 0:
        element.set('ry', str(float(ry) * scale_y))