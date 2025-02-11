import ezdxf
from src.shapes.circle import Circle
from src.shapes.ellipse import Ellipse
from src.shapes.line import Line
from src.shapes.path import Path
from src.shapes.rectangle import Rectangle
from src.svg_handler import get_svg_height


def write_dxf(root, filename):
    """
    Creates a new dxf file. Iterates it through the root, which contains all svg elements.
    Transforms them into dxf entities and writes it into the dxf file.
    At the end, saves it as filename.dxf

    :param root: iterable with all the contents of the svg file
    :param filename: name of the dxf file, how it will be stored
    :return: -
    """
    # create new dxf file
    doc = ezdxf.new()
    msp = doc.modelspace()

    # get height of svg-file
    height = get_svg_height(root)

    # iterate through svg content
    for element in root.iter():
        match element.tag:
            case '{http://www.w3.org/2000/svg}circle':
                circ = Circle(float(element.get('cx')), float(element.get('cy')), float(element.get('r')), height)
                circ.draw_dxf_circle(msp)
            case '{http://www.w3.org/2000/svg}ellipse':
                ell = Ellipse(float(element.get('cx')), float(element.get('cy')),
                              float(element.get('rx')), float(element.get('ry')),
                              element.get('transform'), height)
                ell.draw_dxf_ellipse(msp)
            case '{http://www.w3.org/2000/svg}rect':
                rect = Rectangle(float(element.get('x')), float(element.get('y')),
                                 float(element.get('width')), float(element.get('height')), element.get('transform'),
                                 element.get('rx'), element.get('ry'), height)
                rect.draw_dxf_rect(msp, height)
                # print('rectangle: ', element.tag, element.attrib)
            case '{http://www.w3.org/2000/svg}line':
                line = Line(float(element.get('x1')), float(element.get('y1')),
                            float(element.get('x2')), float(element.get('y2')), height)
                line.draw_dxf_line(msp)
                # print('line:' , element.tag, element.attrib)
            case '{http://www.w3.org/2000/svg}polygone':
                print('polygone: ', element.tag, element.attrib)
            case '{http://www.w3.org/2000/svg}path':
                # print('path:', element.tag, element.attrib)
                path = Path(element.get('d'))
                path.draw_svg_path(msp, height)
            case _:
                # print('nothing:', element.tag, element.attrib)
                pass

    doc.saveas("dxf files/" + filename + ".dxf")

