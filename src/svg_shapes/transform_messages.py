import re

from src.logging_config import setup_logger

transform_logger = setup_logger("transform-messages")


def export_transformations(transformation):
    """
    Export the transformation message from the svg element.
    :param transformation: string, transform message from svg element
    :return: list of tuples, [(type, values), ..., (type, values)]
    """
    pattern = r"(translate|rotate|scale|skewX|skewY|matrix)\(([^)]+)\)"

    try:
        # match all possible transformation
        matches = re.findall(pattern, transformation)
    except TypeError as e:
        transform_logger.exception(e)
        return None
    else:
        # convert the patterns into tuples (type, [values])
        transformations = [(t_type, list(map(float, values.replace(', ', ',').replace(' ', ',').split(','))))
            for t_type, values in matches]

        return transformations
