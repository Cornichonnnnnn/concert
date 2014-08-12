import tempfile
import shutil
import numpy as np
import os.path as op
from concert.coroutines.base import coroutine, inject
from concert.storage import DummyWalker, DirectoryWalker, StorageError
from concert.tests import TestCase


class TestWalker(TestCase):

    def setUp(self):
        super(TestWalker, self).setUp()
        self.walker = DummyWalker()
        self.data = [0, 1]

    def check(self):
        truth = set([op.join('', 'foo', str(i)) for i in self.data])
        self.assertEqual(self.walker.paths, truth)

    def test_coroutine(self):
        inject(self.data, self.walker.write(fname='foo'))
        self.check()

    def test_generator(self):
        self.walker.write(data=self.data, fname='foo')
        self.check()


class TestDirectoryWalker(TestCase):

    def setUp(self):
        super(TestDirectoryWalker, self).setUp()
        self.path = tempfile.mkdtemp()
        self.walker = DirectoryWalker(root=self.path)
        self.data = np.ones((512, 512))

    def tearDown(self):
        shutil.rmtree(self.path)

    def test_directory_creation(self):
        self.walker.descend('foo')
        self.walker.descend('bar')
        self.assertTrue(op.exists(op.join(self.path, 'foo')))
        self.assertTrue(op.exists(op.join(self.path, 'foo', 'bar')))

    def test_default_write(self):
        self.walker.write([self.data, self.data])
        self.assertTrue(op.exists(op.join(self.path, 'frame_000000.tif')))
        self.assertTrue(op.exists(op.join(self.path, 'frame_000001.tif')))

        with self.assertRaises(StorageError):
            self.walker.write([self.data])

    def test_custom_write(self):
        self.walker.write([self.data], fname='foo-{}.tif')
        self.assertTrue(op.exists(op.join(self.path, 'foo-0.tif')))

    def test_invalid_ascend(self):
        with self.assertRaises(StorageError):
            self.walker.ascend()
