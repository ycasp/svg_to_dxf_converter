# scaling functions
from svgpathtools import parse_path


def scale_rectangle(element, scale_x, scale_y):
    """
    Scales a svg rectangle with scale_x and scale_y.
    Writes the scaled rectangle back to the tree.

    :param element: svg element, in this case rect
    :param scale_x: factor for scaling in x direction
    :param scale_y: factor for scaling in y direction
    :return: -
    """
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


def scale_circle(element, scale_x, scale_y):
    """
    Scales a svg circle with scale_x and scale_y.
    Writes the scaled circle back to the tree.

    :param element: svg element, in this case circle
    :param scale_x: factor for scaling in x direction
    :param scale_y: factor for scaling in y direction
    :return: -
    """
    # scale cx - center of circle x-coordinate
    new_x = float(element.attrib.get('cx')) * scale_x
    element.set('cx', str(new_x))

    # scale cy - center of circle y-coordinate
    new_y = float(element.attrib.get('cy')) * scale_y
    element.set('cy', str(new_y))

    # scale r - radius
    new_r = float(element.attrib.get('r')) * scale_x
    element.set('r', str(new_r))


def scale_ellipse(element, scale_x, scale_y):
    """
    Scales a svg ellipse with scale_x and scale_y.
    Writes the scaled ellipse back to the tree.

    :param element: svg element, in this case ellipse
    :param scale_x: factor for scaling in x direction
    :param scale_y: factor for scaling in y direction
    :return: -
    """
    # scale cx - center of ellipse x-coordinate
    new_x = float(element.attrib.get('cx')) * scale_x
    element.set('cx', str(new_x))

    # scale cy - center of ellipse y-coordinate
    new_y = float(element.attrib.get('cy')) * scale_y
    element.set('cy', str(new_y))

    # scale rx - radius of ellipse x-direction
    rx = element.attrib.get('rx')
    if rx is not None and rx != 0:
        element.set('rx', str(float(rx) * scale_x))

    # scale ry - radius of ellipse in y-direction
    ry = element.attrib.get('ry')
    if ry is not None and ry != 0:
        element.set('ry', str(float(ry) * scale_y))


def scale_line(element, scale_x, scale_y):
    """
    Scales a svg line with scale_x and scale_y.
    Writes the scaled line back to the tree.

    :param element: svg element, in this case line
    :param scale_x: factor for scaling in x direction
    :param scale_y: factor for scaling in y direction
    :return: -
    """
    # scale x1 - x-coord of starting point of line
    new_x1 = float(element.attrib.get('x1')) * scale_x
    element.set('x1', str(new_x1))

    # scale y1 - y-cord of starting point of line
    new_y1 = float(element.attrib.get('y1')) * scale_y
    element.set('y1', str(new_y1))

    # scale x2 - x-coord of end point of line
    new_x2 = float(element.attrib.get('x2')) * scale_x
    element.set('x2', str(new_x2))

    # scale y2 - y-coord of end point of line
    new_y2 = float(element.attrib.get('y2')) * scale_y
    element.set('y2', str(new_y2))


def scale_path(element, scale_x, scale_y):
    """
    Scales a svg path with scale_x and scale_y.
    Writes the scaled path back to the tree.

    :param element: svg element, in this case path
    :param scale_x: factor for scaling in x direction
    :param scale_y: factor for scaling in x direction
    :return: -
    """
    path = element.attrib.get('d')
    parsed_path = parse_path(path)
    scaled_path = parsed_path.scaled(scale_x, scale_y)
    element.set('d', scaled_path.d())


def scale_polygon(element, scale_x, scale_y):
    """
    Scales a svg polygon with scale_x and scale_y.
    Write the scaled polygon back to the tree
    :param element: svg element, in this case polygon
    :param scale_x: factor for scaling in x direction
    :param scale_y: factor for scaling in x direction
    :return: -
    """
    points = element.get("points")
    scaled_points = [f"{float(p.split(',')[0]) * scale_x},{float(p.split(',')[1]) * scale_y}"
        for p in points.strip().split()]
    element.set("points", " ".join(scaled_points))