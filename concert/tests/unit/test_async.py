import time
import random
from concurrent.futures import Future
from concert.devices.dummy import DummyDevice
from concert.helpers import async, wait
from concert.tests import slow, TestCase


@async
def func():
    pass


@async
def bad_func():
    raise RuntimeError


class TestAsync(TestCase):

    def setUp(self):
        super(TestAsync, self).setUp()
        self.device = DummyDevice()

    @slow
    def test_wait(self):
        @async
        def long_func():
            time.sleep(random.random() / 50.)

        futs = []
        for i in range(10):
            futs.append(long_func())

        wait(futs)

        for future in futs:
            self.assertTrue(future.done(), "Not all futures finished.")

    def test_exceptions(self):
        with self.assertRaises(TypeError):
            func(0).join()

        with self.assertRaises(RuntimeError):
            bad_func().join()
