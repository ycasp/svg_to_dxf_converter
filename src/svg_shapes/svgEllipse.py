from src.utilities import change_svg_to_dxf_coordinate, export_rotation, rotate_clockwise_around_point


class SvgEllipse:

    def __init__(self, element, svg_height):
        self.name = 'ellipse'

        self.center_x = float(element.get('cx'))
        self.center_y = change_svg_to_dxf_coordinate(float(element.get('cy')), svg_height)

        self.radius_x = (float(element.get('rx')), 0)
        self.radius_y = (0, float(element.get('ry')))

        self.transform = element.get('transform')
        if self.transform is not None:
            rotation = export_rotation(self.transform)
            if rotation is not None:
                self.center_x, self.center_y = rotate_clockwise_around_point(self.center_x, self.center_y,
                                        rotation[0], rotation[1], change_svg_to_dxf_coordinate(rotation[2], svg_height))
                self.radius_x = rotate_clockwise_around_point(self.radius_x[0], self.radius_x[1],
                                        rotation[0], 0, 0)
                self.radius_y = rotate_clockwise_around_point(self.radius_y[0], self.radius_y[1],
                                        rotation[0], 0, 0)


    def get_name(self):
        return self.name

    def scale(self, scale_x, scale_y):
        self.center_x = self.center_x * scale_x
        self.center_y = self.center_y * scale_y
        self.radius_x = (self.radius_x[0] * scale_x, self.radius_x[1] * scale_y)
        self.radius_y = (self.radius_y[0] * scale_x, self.radius_y[1] * scale_y)