import unittest
from . import base_classes
from liquify import liquify


class LiquifyTests(unittest.TestCase):
    def test_simple(self):
        liquified = liquify(base_classes.LiquifySimple())
        expected_result = dict(miles="davis", john="coltrane")
        self.assertEqual(len(liquified), 2)
        self.assertEqual(liquified, expected_result)

    def test_multiple(self):
        solid1 = base_classes.LiquifySimple()
        solid2 = base_classes.LiquifySimple(miles="brew")

        liquified = liquify(solid1, solid2)
        expect_result = [
            dict(miles="davis", john="coltrane"),
            dict(miles="brew", john="coltrane"),
        ]
        self.assertEqual(len(liquified), 2)
        self.assertEqual(liquified, expect_result)

    def test_nested_object(self):
        liquified = liquify(base_classes.LiquifyNested())
        expected_result = dict(
            miles=dict(
                miles="davis",
                john="coltrane"
            ),
            john="coltrane"
        )
        self.assertEqual(len(liquified), 2)
        self.assertEqual(liquified, expected_result)

        # check for non-liquify specific nested classes
        solid = base_classes.LiquifyNested(miles=base_classes.Base())
        liquified = liquify(solid)
        expected_result = dict(
            miles=dict(
                artists=["davis", "coltrane"],
                id=12,
                john="coltrane",
                miles="davis"
            ),
            john="coltrane"
        )
        self.assertEqual(len(liquified), 2)
        self.assertEqual(liquified, expected_result)
