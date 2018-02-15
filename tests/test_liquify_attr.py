import asyncio
import unittest
from mock import patch
from . import base_classes, BaseTest, make_async
from liquify import liquify_attr


class LiquifyAttrTests(BaseTest):
    def test_simple(self):
        solid = base_classes.LiquifySimple()
        liquified = self.loop.run_until_complete(liquify_attr(solid, "miles"))
        self.assertEqual(liquified, ("miles", "davis"))

        # check on @property
        liquified = self.loop.run_until_complete(liquify_attr(solid, "artists"))
        self.assertEqual(liquified, ("artists", ["davis", "coltrane"]))

    def test_function(self):
        solid = base_classes.LiquifySimple()
        liquified = self.loop.run_until_complete(liquify_attr(solid, "jazz"))
        self.assertEqual(liquified, ("jazz", "Birth of Cool (1957)"))

    @patch("liquify._liquify")
    def test_nested(self, mock_liquify):
        make_async(mock_liquify)

        solid = base_classes.LiquifyNested()
        liquified = self.loop.run_until_complete(liquify_attr(solid, "john"))
        self.assertFalse(mock_liquify.called)

        solid = base_classes.LiquifyNested()
        liquified = self.loop.run_until_complete(liquify_attr(solid, "miles"))
        self.assertTrue(mock_liquify.called)

        # check that the return of a method is also checked for nested obj
        mock_liquify.called = False
        solid = base_classes.LiquifyNested()
        liquified = self.loop.run_until_complete(liquify_attr(solid, "nested"))
        self.assertTrue(mock_liquify.called)
