import math
import re

import numpy as np
from svgpathtools import parse_path


# svg transformation functions

def change_svg_to_dxf_coordinate(y, height):
    """
    Changes the svg coordinates to cartesian coordinates (y-axis in svg is from top to down).

    :param y: y coordinate in svg file
    :param height: height of svg file
    :return: y coordinate in cartesian coordinate
    """
    return (-1) * y + height


# exports rotation angle (in degree!!) from transformation-string of svg ellipse
def export_rotation(transformation):
    """
    Exports the rotation angle (in degree) given in the transformation message.
    If none is given, the method returns 0.

    :param transformation: transformation message of the svg object
    :return: rotation angle given in the transformation message, if none is given, it returns 0
    """
    match = re.search(r'rotate\(([-\d.]+)', transformation)
    if match:
        return float(match.group(1))  # Extract the angle as a float
    return 0  # Return 0 if no rotation is found


# geometric functions

def rotate_clockwise_around_svg_origin(x, y, rot_angle, height):
    """
    Rotate a point x,y counterclockwise around the moved svg-origin (0, height).
    :param x: x-coordinate of point to be rotated
    :param y: y-coordinate of point to be rotated
    :param rot_angle: rotation angle in degree
    :param height: height of svg file, to have proper rotation point
    :return: (rot_x, rot_y) (tuple) rotated point
    """
    # rot_angle is in degree (from svg file) - transform it to radian
    rot_angle_rad = rot_angle * math.pi / 180
    return (round(x * np.cos(rot_angle_rad) + (y - height) * np.sin(rot_angle_rad), 5),
    round(height - x * np.sin(rot_angle_rad) + (y - height) * np.cos(rot_angle_rad), 5))


def rotate_clockwise_around_cartesian_origin(x, y, rot_angle):
    # TODO description + testing
    rot_angle_rad = math.radians(rot_angle)

    return (round(x * np.cos(rot_angle_rad) + y * np.sin(rot_angle_rad), 5),
    round(- x * np.sin(rot_angle_rad) + y * np.cos(rot_angle_rad), 5))


def rotate_counterclockwise_around_cartesian_origin(x, y, rot_angle):
    # TODO description + testing
    rot_angle_rad = math.radians(rot_angle)

    return (round(x * np.cos(rot_angle_rad) - y * np.sin(rot_angle_rad), 5),
    round(x * np.sin(rot_angle_rad) + y * np.cos(rot_angle_rad), 5))


def calculate_angle_between_vectors_in_rad(x_vec, y_vec, large_angle):
    norm_x = calculate_euclidean_norm(x_vec)
    norm_y = calculate_euclidean_norm(y_vec)

    scalar_prod_x_y = calculate_scalar_product(x_vec, y_vec)
    # TODO if norm == 0 throw exception
    angle = math.acos(scalar_prod_x_y / (norm_x * norm_y))

    """
    if not large_angle:
        return angle
    elif large_angle:
        return 2 * math.pi - angle
    """
    return angle


def rad_to_degree(rad):
    return rad * 180 / math.pi


def calculate_euclidean_norm(x_vec):
    return (x_vec[0] ** 2 + x_vec[1] ** 2) ** 0.5


def calculate_scalar_product(x_vec, y_vec):
    return x_vec[0] * y_vec[0] + x_vec[1] * y_vec[1]


# scaling functions

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
