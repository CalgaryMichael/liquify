import unittest
from . import base_classes
from liquify import liquify_list


class LiquifyListTests(unittest.TestCase):
    def test_simple(self):
        solid = base_classes.LiquifySimple()
        liquified = liquify_list(solid, ["id", "miles"])
        expected_result = dict(
            id=12,
            miles="davis"
        )
        self.assertEqual(len(liquified), 2)
        self.assertEqual(liquified, expected_result)

    def test_invalid_field(self):
        solid = base_classes.LiquifySimple()
        with self.assertRaises(AttributeError):
            liquified = liquify_list(solid, ["id", "fake"])

    def test_invalid_format(self):
        solid = base_classes.LiquifySimple()
        with self.assertRaises(TypeError):
            liquified = liquify_list(solid, dict(attributes=["miles"]))

    def test_nested_object(self):
        solid = base_classes.LiquifyNested()
        liquified = liquify_list(solid, ["miles", "john"])
        expected_result = dict(
            miles=dict(
                miles="davis",
                john="coltrane"
            ),
            john="coltrane"
        )
        self.assertEqual(len(liquified), 2)
        self.assertEqual(liquified, expected_result)