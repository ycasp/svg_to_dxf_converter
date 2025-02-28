import logging
import unittest
from token import EQUAL

from src.svg_shapes.svgHeader import *

class TestSvgHeader(unittest.TestCase):

    def setUp(self):
        self.normal_element = {'height': '300mm', 'width': '400mm', 'viewBox': '0 0 200 150'}
        self.px_element = {'height': '800px', 'width': '800px', 'viewBox': '0 0 200 200'}
        self.empty_element = {'viewBox': '0 0 200 200'}

    def test_initialization(self):
        header = SvgHeader(self.normal_element)

        self.assertEqual(header.name, 'header')
        self.assertEqual(header.height, 300)
        self.assertEqual(header.width, 400)
        self.assertEqual(header.view_box, [0, 0, 200, 150])

        empty_header = SvgHeader(self.empty_element)

        self.assertEqual(empty_header.name, 'header')
        self.assertEqual(empty_header.height, 200)
        self.assertEqual(empty_header.width, 200)
        self.assertEqual(empty_header.view_box, [0, 0, 200, 200])


    def test_getters(self):
        header_px = SvgHeader(self.px_element)

        self.assertEqual(header_px.get_header_name(), 'header')
        self.assertEqual(header_px.get_header_height(), 800 * 25.4 / 96)
        self.assertEqual(header_px.get_header_width(), 800 * 25.4 / 96)

    def test_extract_attributes(self):
        self.assertEqual(extract_view_box('0 0 250 500'), [0, 0, 250, 500])

        with self.assertLogs("src.svg_shapes.svgHeader", level = "INFO") as log:
            width = extract_header_width('800cm')
        self.assertEqual(width, 0)
        self.assertIn("unknown width unit: 800cm", log.output[0])

        with self.assertLogs("src.svg_shapes.svgHeader", level = "INFO") as log:
            height = extract_header_height('300m')
        self.assertEqual(height, 0)
        self.assertIn("unknown height unit: 300m", log.output[0])
