from src.dxf_handler import write_dxf
from src.svg_handler import read_svg_file, scale_file_param, scale_file
from logging_config import setup_logger

main_logger = setup_logger(__name__)

def main():
    """Main function to print Hello World."""
    print("Hello, World!")


if __name__ == "__main__":
    # /basic geometric forms/
    # /animals/without shapes/
    # /bezier curves/
    # /fruits and veggies/
    # /dohner ag/
    filepath = "C:/Users/ycasp/Documents/Projekt Lukas/svg collection/basic geometric forms/"
    filename = "triangle-half"
    ending = ".svg"
    try:
        # read in svg (xml) file into tree
        svg_root = read_svg_file(filepath + filename + ending)

        # scale file
        svg_root = scale_file(svg_root, 266.520, 373.335)
        # svg_root = scale_file_param(svg_root, 2, 2)

        # write svg content to dxf file and save it
        write_dxf(svg_root, filename)

    except FileNotFoundError as pathErr:
        main_logger.exception(pathErr)

