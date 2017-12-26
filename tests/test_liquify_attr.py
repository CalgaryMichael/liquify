import unittest
from unittest.mock import patch
from . import base_classes
from liquify import liquify_attr


class LiquifyAttrTests(unittest.TestCase):
    def test_simple(self):
        solid = base_classes.LiquifySimple()
        liquified = liquify_attr(solid, "miles")
        self.assertEqual(liquified, ("miles", "davis"))

        # check on @property
        liquified = liquify_attr(solid, "artists")
        self.assertEqual(liquified, ("artists", ["davis", "coltrane"]))

    def test_function(self):
        solid = base_classes.LiquifySimple()
        liquified = liquify_attr(solid, "jazz")
        self.assertEqual(liquified, ("jazz", "Birth of Cool (1957)"))

    @patch("liquify.liquify")
    def test_nested(self, mock_liquify):
        solid = base_classes.LiquifyNested()
        liquified = liquify_attr(solid, "john")
        self.assertFalse(mock_liquify.called)

        solid = base_classes.LiquifyNested()
        liquified = liquify_attr(solid, "miles")
        self.assertTrue(mock_liquify.called)

        # check that the return of a method is also checked for nested obj
        mock_liquify.called = False
        solid = base_classes.LiquifyNested()
        liquified = liquify_attr(solid, "nested")
        self.assertTrue(mock_liquify.called)
