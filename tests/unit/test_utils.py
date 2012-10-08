#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os
import unittest

from mock import patch
from mock import MagicMock as Mock

import pyrax.utils as utils
import pyrax.exceptions as exc



class CF_UtilsTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(CF_UtilsTest, self).__init__(*args, **kwargs)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_self_deleting_temp_file(self):
        with utils.SelfDeletingTempfile() as tmp:
            self.assert_(isinstance(tmp, basestring))
            self.assert_(os.path.exists(tmp))
            self.assert_(os.path.isfile(tmp))
        # File shoud be deleted after exiting the block
        self.assertFalse(os.path.exists(tmp))

    def test_self_deleting_temp_directory(self):
        with utils.SelfDeletingTempDirectory() as tmp:
            self.assert_(isinstance(tmp, basestring))
            self.assert_(os.path.exists(tmp))
            self.assert_(os.path.isdir(tmp))
        # Directory shoud be deleted after exiting the block
        self.assertFalse(os.path.exists(tmp))

    def test_get_checksum_from_string(self):
        test = "some random text"
        md = hashlib.md5()
        md.update(test)
        expected = md.hexdigest()
        received = utils.get_checksum(test)
        self.assertEqual(expected, received)

    def test_get_checksum_from_file(self):
        test = "some random text"
        md = hashlib.md5()
        md.update(test)
        expected = md.hexdigest()
        with utils.SelfDeletingTempfile() as tmp:
            with file(tmp, "w") as testfile:
                testfile.write(test)
            with file(tmp, "r") as testfile:
                received = utils.get_checksum(testfile)
        self.assertEqual(expected, received)

    def test_folder_size_bad_folder(self):
        self.assertRaises(exc.FolderNotFound, utils.folder_size, "/doesnt_exist")

    def test_folder_size_no_ignore(self):
        with utils.SelfDeletingTempDirectory() as tmpdir:
            # write 10 files of 100 bytes each
            content = "x" * 100
            for idx in xrange(10):
                pth = os.path.join(tmpdir, "test%s" % idx)
                with file(pth, "w") as ff:
                    ff.write(content)
            fsize = utils.folder_size(tmpdir)
        self.assertEqual(fsize, 1000)

    def test_folder_size_ignore_string(self):
        with utils.SelfDeletingTempDirectory() as tmpdir:
            # write 10 files of 100 bytes each
            content = "x" * 100
            for idx in xrange(10):
                pth = os.path.join(tmpdir, "test%s" % idx)
                with file(pth, "w") as ff:
                    ff.write(content)
            # ignore one file
            fsize = utils.folder_size(tmpdir, ignore="*7")
        self.assertEqual(fsize, 900)

    def test_folder_size_ignore_list(self):
        with utils.SelfDeletingTempDirectory() as tmpdir:
            # write 10 files of 100 bytes each
            content = "x" * 100
            for idx in xrange(10):
                pth = os.path.join(tmpdir, "test%s" % idx)
                with file(pth, "w") as ff:
                    ff.write(content)
            # ignore odd files
            ignore = ["*1", "*3", "*5", "*7", "*9"] 
            fsize = utils.folder_size(tmpdir, ignore=ignore)
        self.assertEqual(fsize, 500)


if __name__ == "__main__":
    unittest.main()