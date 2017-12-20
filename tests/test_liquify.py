import unittest
from liquify import liquify

class BaseLiquify(object):
    id = 12
    miles = "davis"
    john = "coltrane"

    __liquify__ = dict(
        attributes=["miles", "john"]
    )


class LiquifyTests(unittest.TestCase):
    def test_simple(self):
        liquified = liquify(BaseLiquify())
        self.assertEqual(len(liquified), 2)
        self.assertEqual(liquified["miles"], "davis")
        self.assertEqual(liquified["john"], "coltrane")

    def test_multiple(self):
        base1 = BaseLiquify()
        base2 = BaseLiquify()
        base2.miles = "brew"

        liquified = liquify(base1, base2)
        self.assertEqual(len(liquified), 2)
        self.assertEqual(liquified[0]["miles"], "davis")
        self.assertEqual(liquified[1]["miles"], "brew")

    def test_nested_object(self):
        base1 = BaseLiquify()
        base2 = BaseLiquify()
        base2.john = "smith"
        base1.miles = base2

        liquified = liquify(base1)
        self.assertEqual(len(liquified), 2)
        self.assertEqual(liquified["miles"], dict(miles="davis", john="smith"))
