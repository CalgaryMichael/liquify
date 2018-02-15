import asyncio
import unittest


def make_async(mock, return_value=None):
    future = asyncio.Future()
    future.set_result(return_value)
    mock.return_value = future


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.get_event_loop()
        if cls.loop.is_closed():
            cls.loop = asyncio.new_event_loop()

    @classmethod
    def tearDownClass(cls):
        cls.loop.close()
