from src.svg_handler import read_svg_file, print_root, scale_file
from src.dxf_handler import write_dxf


def main():
    """Main function to print Hello World."""
    print("Hello, World!")

if __name__ == "__main__":
    # /basic geometric forms/
    # /animals/without shapes/
    # /bezier curves/
    filepath = "C:/Users/ycasp/Documents/Projekt Lukas/svg collection/basic geometric forms/"
    filename = "geom_house"
    ending = ".svg"
    svg_root = read_svg_file(filepath + filename + ending)
    # print_root(svg_root)
    scale_file(svg_root, 800, 1600)
    # print_root(svg_root)
    write_dxf(svg_root, filename)