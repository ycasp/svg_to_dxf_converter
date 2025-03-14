import re

from src.logging_config import setup_logger

transform_logger = setup_logger("transform-messages")


# get values of transformation messages

def export_transformations(transformation):
    pattern = r"(translate|rotate|scale|skewX|skewY|matrix)\(([^)]+)\)"

    try:
        matches = re.findall(pattern, transformation)
    except TypeError as e:
        transform_logger.exception(e)
        return None
    else:
        transformations = [(t_type, list(map(float, values.replace(', ', ',').replace(' ', ',').split(','))))
            for t_type, values in matches]

        return transformations
