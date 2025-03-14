from logging_config import setup_logger

# multiplication factor: thickness * factor = minimal bound
FACTOR = 0.7
# minimal line with for laser cutting (0.3 mm)
MIN_LINE_WIDTH = 0.3

cut_rules_logger = setup_logger(__name__)


def enforce_cut_rules(root, thickness):
    min_radius = FACTOR * thickness
    min_distance_between_rail = FACTOR * thickness
    min_steg_with = FACTOR * thickness
    # iterate through svg content
    for element in root.iter():
        match element.tag:
            case '{http://www.w3.org/2000/svg}circle':
                # min radius
                circle_cut_rules(element, min_radius)
            case '{http://www.w3.org/2000/svg}ellipse':
                pass
            case '{http://www.w3.org/2000/svg}rect':
                rectangle_cut_rules(element, min_radius)
            case '{http://www.w3.org/2000/svg}line':
                pass
            case '{http://www.w3.org/2000/svg}polygon':
                pass
            case '{http://www.w3.org/2000/svg}path':
                pass
            case _:
                cut_rules_logger.info(f"svg_element without matching figure tag: {element.tag}: {element.attrib}")

    return root


def circle_cut_rules(element, min_radius):
    # min radius
    if float(element.get('r')) < min_radius:
        cut_rules_logger.error(f"radius to small: r = {float(element.get('r'))} mm, requested: {min_radius} mm")


def rectangle_cut_rules(element, min_radius):
    rect_width = float(element.get('width'))
    rect_height = float(element.get('height'))
    if element.get('rx') is not None:
        rx = float(element.get('rx'))
    else:
        rx = 0

    if element.get('ry') is not None:
        ry = float(element.get('ry'))
    else:
        ry = 0

    # min line width
    if rect_width - 2 * rx < MIN_LINE_WIDTH:
        cut_rules_logger.error(f"rectangle width to small: width = {rect_width - 2 * rx} mm, "
                               f"requested: {MIN_LINE_WIDTH} mm")

    if rect_height - 2 * ry < MIN_LINE_WIDTH:
        cut_rules_logger.error(f"rectangle height to small: width = {rect_height - 2 * ry} mm, "
                               f"requested: {MIN_LINE_WIDTH} mm")

    if 0 < rx < min_radius:
        cut_rules_logger.error(f"corner radius in x direction of rectangle to small: rx = {rx} mm,"
                               f"requested: {min_radius} mm")

    if 0 < ry < min_radius:
        cut_rules_logger.error(f"corner radius in y direction of rectangle to small: ry = {ry} mm,"
                               f"requested: {min_radius} mm")
