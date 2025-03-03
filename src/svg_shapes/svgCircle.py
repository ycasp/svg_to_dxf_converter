from src.utilities import export_rotation, change_svg_to_dxf_coordinate, rotate_clockwise_around_point


class SvgCircle:

    def __init__(self, segment, svg_height):
        self.name = 'circle'

        # set center
        self.center_x = float(segment.get('cx'))
        self.center_y = change_svg_to_dxf_coordinate(float(segment.get('cy')), svg_height)

        # extract transformations
        self.transform = segment.get('transform')
        if self.transform is not None:
            # rotate if necessary
            rotation = export_rotation(self.transform)
            if rotation is not None:
                    self.center_x, self.center_y = rotate_clockwise_around_point(self.center_x, self.center_y,
                                            rotation[0], rotation[1], change_svg_to_dxf_coordinate(rotation[2], svg_height))

        # extract radius
        self.radius = float(segment.get('r'))

    def get_circle_name(self):
        return self.name
