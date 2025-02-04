import os
import shutil
import unittest
from unittest.mock import patch


class TestMain(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_main_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.file1 = os.path.join(self.test_dir, "testfile.txt")
        with open(self.file1, "w") as f:
            f.write("content")

    def test_copy_command(self):
        dest = os.path.join(self.test_dir, "copy.txt")
        with patch('sys.argv', ['manager', 'copy', self.file1, dest]):
            from src.main import main
            main()
        self.assertTrue(os.path.exists(dest))

    def tearDown(self):
        shutil.rmtree(self.test_dir)
