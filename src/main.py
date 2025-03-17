from logging_config import setup_logger
from src.dxf_handler import write_dxf
from src.svg_handler import read_svg_file, scale_file_param, scale_file

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
    # /fonts/
    filepath = "C:/Users/ycasp/Documents/Projekt Lukas/svg collection/dohner ag/"
    filename = "Wedding01_wAnchor"
    ending = ".svg"
    try:
        # read in svg (xml) file into tree
        svg_figures = read_svg_file(filepath + filename + ending)

        # scale file
        scale = 0.1

        #svg_figures = scale_file(svg_figures, 286.242, 254.179)
        svg_figures = scale_file_param(svg_figures, scale, scale)

        # cut rules
        # enforce_cut_rules(svg_root, 2)

        # write svg content to dxf file and save it
        write_dxf(svg_figures, filename)

    except FileNotFoundError as pathErr:
        main_logger.exception(pathErr)
