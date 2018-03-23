import six
import unittest
from . import base_classes
from liquify import liquify


class LiquifyTests(unittest.TestCase):
    def test_simple(self):
        liquified = liquify(base_classes.LiquifySimple())
        expected_result = dict(miles="davis", john="coltrane")
        self.assertEqual(len(liquified), 2)
        self.assertEqual(liquified, expected_result)

    def test_simple__explicit_ingredients(self):
        liquified = liquify(base_classes.Base(ornette="coleman"), ingredients=["miles", "ornette"])
        expected_result = dict(miles="davis", ornette="coleman")
        self.assertEqual(len(liquified), 2)
        self.assertEqual(liquified, expected_result)

        # explicit ingredients overrides class attribute for liquify
        liquified = liquify(base_classes.LiquifySimple(), ingredients=["miles", "id"])
        expected_result = dict(miles="davis", id=12)
        self.assertEqual(len(liquified), 2)
        self.assertEqual(liquified, expected_result)

    def test_simple__mixed_objects(self):
        class TestObject():
            foo = 1
            bar = 2

        objs = (base_classes.LiquifySimple(), TestObject())
        expected_result = "Cannot liquify multiple classes with explicit ingredients"
        with six.assertRaisesRegex(self, TypeError, expected_result):
            liquified = liquify(*objs, ingredients=["miles", "id"])

    def test_multiple__no_groups(self):
        solid1 = base_classes.LiquifySimple()
        solid2 = base_classes.LiquifySimple(miles="brew")

        liquified = liquify(solid1, solid2)
        expect_result = dict(
            liquify_simple=[
                dict(miles="davis", john="coltrane"),
                dict(miles="brew", john="coltrane"),
            ]
        )
        self.assertEqual(len(liquified), 1)
        self.assertEqual(liquified, expect_result)

    def test_multiple__with_groups(self):
        solid1 = base_classes.LiquifySimple()
        solid2 = base_classes.LiquifySimple(john="love supreme")
        solid3 = base_classes.LiquifyComplex(miles="brew")

        liquified = liquify(solid1, solid2, solid3)
        expect_result = dict(
            liquify_simple=[
                dict(miles="davis", john="coltrane"),
                dict(miles="davis", john="love supreme"),
            ],
            complex=[
                dict(miles="brew", john="coltrane"),
            ]
        )
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

    def test_nested_object__depth(self):
        liquified = liquify(base_classes.LiquifyDoubleNested())
        expected_result = dict(
            miles=dict(
                miles=dict(
                    miles="davis",
                    john="coltrane"),
                john="coltrane"),
            john=dict(
                miles="davis",
                john="coltrane"))
        self.assertEqual(len(liquified), 2)
        self.assertEqual(liquified, expected_result)

        liquified = liquify(base_classes.LiquifyDoubleNested(), depth=1)
        expected_result = dict(
            miles=dict(
                miles="miles davis",  # casted to str due to depth
                john="coltrane"),
            john=dict(
                miles="davis",
                john="coltrane"))
        self.assertEqual(len(liquified), 2)
        self.assertEqual(liquified, expected_result)
