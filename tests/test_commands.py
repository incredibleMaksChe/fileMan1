import os
import shutil
import unittest
from datetime import datetime

from src.commands import copy_file, delete_path, count_files, search_files, add_date_to_filenames, analyse_directory


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.file1 = os.path.join(self.test_dir, "file1.txt")
        with open(self.file1, "w") as f:
            f.write("test")
        self.subdir = os.path.join(self.test_dir, "subdir")
        os.makedirs(self.subdir, exist_ok=True)
        self.file2 = os.path.join(self.subdir, "file2.log")
        with open(self.file2, "w") as f:
            f.write("test")

    def test_copy_file(self):
        dest = os.path.join(self.test_dir, "copied.txt")
        copy_file(self.file1, dest)
        self.assertTrue(os.path.exists(dest))

    def test_delete_file(self):
        delete_path(self.file1)
        self.assertFalse(os.path.exists(self.file1))

    def test_count_files(self):
        self.assertEqual(count_files(self.test_dir), 2)

    def test_search_files(self):
        files = search_files(self.test_dir, r"\.txt$")
        self.assertIn(self.file1, files)

    def test_add_date_to_files(self):
        add_date_to_filenames(self.test_dir, recursive=True)
        date_str = datetime.fromtimestamp(os.path.getctime(self.file1)).strftime("%Y%m%d")
        new_name = f"file1_{date_str}.txt"
        new_path = os.path.join(self.test_dir, new_name)
        self.assertTrue(os.path.exists(new_path))

    def test_analyse_directory(self):
        analyse_directory(self.test_dir)  # Just check it runs without error

    def tearDown(self):
        shutil.rmtree(self.test_dir)
