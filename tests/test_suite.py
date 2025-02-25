import unittest
from test_rectangle import TestRectangle
from test_circle import TestCircle
from test_line import TestLine
from test_polygon import TestPolygon

# Create a test suite
def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRectangle))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCircle))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestLine))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPolygon))
    return test_suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())