import math
import re

import numpy as np

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
