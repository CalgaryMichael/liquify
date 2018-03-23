import unittest
from mock import patch
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
        liquified = liquify_attr(solid, "miles")
        self.assertTrue(mock_liquify.called)

    @patch("liquify.liquify")
    def test_nested__builtin(self, mock_liquify):
        solid = base_classes.LiquifyNested()
        liquified = liquify_attr(solid, "john")
        self.assertFalse(mock_liquify.called)

    @patch("liquify.liquify")
    def test_nested__function(self, mock_liquify):
        solid = base_classes.LiquifyNested()
        liquified = liquify_attr(solid, "nested")
        self.assertTrue(mock_liquify.called)

    @patch("liquify.liquify")
    def test_nested__depth(self, mock_liquify):
        solid = base_classes.LiquifyNested()
        liquified = liquify_attr(solid, "nested", depth=0)
        self.assertFalse(mock_liquify.called)
        self.assertEqual(liquified, ("nested", "miles davis"))
