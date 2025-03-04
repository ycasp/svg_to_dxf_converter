import ezdxf

from src.shapes.circle import Circle
from src.shapes.ellipse import Ellipse
from src.shapes.line import Line
from src.shapes.path import Path
from src.shapes.polygon import Polygon
from src.shapes.polyline import Polyline
from src.shapes.rectangle import Rectangle
from src.svg_handler import get_svg_height

from logging_config import setup_logger

dxf_logger = setup_logger(__name__)

def write_dxf(svg_figures, filename):
    """
    Creates a new dxf file. Iterates it through the root, which contains all svg elements.
    Transforms them into dxf entities and writes it into the dxf file.
    At the end, saves it as filename.dxf

    :param svg_figures: iterable with all the figures in an svg file
    :param filename: name of the dxf file, how it will be stored
    :return: -
    """
    # create new dxf file
    doc = ezdxf.new()
    msp = doc.modelspace()

    # get height of svg-file
    svg_height = svg_figures[0].get_header_height()

    # iterate through svg content
    for figure in svg_figures:
        match figure.get_name():
            case 'circle':
                circ = Circle(figure)
                circ.draw_dxf_circle(msp)
            case 'ellipse':
                ell = Ellipse(figure)
                ell.draw_dxf_ellipse(msp)
            case 'rectangle':
                rect = Rectangle(figure)
                rect.draw_dxf_rect(msp, svg_height)
                # print('rectangle: ', element.tag, element.attrib)
            case 'line':
                line = Line(figure)
                line.draw_dxf_line(msp)
                # print('line:' , element.tag, element.attrib)
            case 'polygon':
                polygon = Polygon(figure)
                polygon.draw_dxf_polygon(msp)
            case 'polyline':
                polyline = Polyline(figure)
                polyline.draw_dxf_polyline(msp)
            case 'path':
                # print('path:', element.tag, element.attrib)
                path = Path(figure)
                path.draw_svg_path(msp, svg_height)
            case _:
                # print('nothing:', element.tag, element.attrib)
                dxf_logger.info(f"svg_element without matching figure tag: {figure.get_name()}")

    doc.saveas("dxf_files/" + filename + ".dxf")
    dxf_logger.info(f"file saved under: src/dxf_files/ + {filename} . dxf")
