import unittest
import decimal
from . import base_classes
from liquify import parse_ingredients


class ParseIngredientsTests(unittest.TestCase):
    def test_without_attribute(self):
        solid = base_classes.Base()
        ingredients = parse_ingredients(solid)
        expected_result = ["artists", "id", "john", "miles"]
        self.assertEqual(ingredients, expected_result)

        # test on a standard library object
        ingredients = parse_ingredients(decimal.Decimal())
        expected_result = ["imag", "real"]
        self.assertEqual(ingredients, expected_result)

    def test_with_attribute(self):
        solid = base_classes.LiquifySimple()
        ingredients = parse_ingredients(solid)
        expected_result = ["miles", "john"]
        self.assertEqual(ingredients, expected_result)
