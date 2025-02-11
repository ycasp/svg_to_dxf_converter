from src.svg_handler import read_svg_file, print_root
from src.dxf_handler import write_dxf


def main():
    """Main function to print Hello World."""
    print("Hello, World!")

if __name__ == "__main__":
    # /basic geometric forms/
    # /animals/without shapes/
    # /bezier curves/
    filepath = "C:/Users/ycasp/Documents/Projekt Lukas/svg collection/bezier curves/"
    filename = "simple_curves"
    ending = ".svg"
    svg_root = read_svg_file(filepath + filename + ending)
    print_root(svg_root)
    write_dxf(svg_root, filename)