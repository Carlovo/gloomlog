import os
import logging
import unittest
import sys
sys.path.insert(0, '../')
sys.path.insert(0, './')
from gloombackend import Backend  # noqa

logging.basicConfig(level=logging.WARN, format='')


class TestGloomlogBackend(unittest.TestCase):
    """
    Test GloomLog's Backend class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info(
            "Setting up variables for testing GloomLog's Backend class")

        cls.backend = Backend()
        cls.test_file_name = "test.txt"
        cls.test_file_text = '{-a1_B":,"" 2]c3-)'

        cls.test_full_file_name = cls.backend.save_path + "/" + \
            cls.test_file_name + cls.backend.save_extension

    def test_write_new_text_file(self):
        """
        Test whether write_new_text_file can correctly write a file
        """

        logging.info(
            "Testing whether write_new_text_file can correctly write a file")

        self.backend.write_new_text_file(
            file_name=self.test_file_name,
            file_text=self.test_file_text
        )

        with open(self.test_file_name, "r") as file:
            contents = file.read()

        self.assertEqual(contents, self.test_file_text)

        os.remove(self.test_file_name)

    def helper_assert_file_contents(self, file_name: str, contents: str = ""):
        """
        Helper function for testing _backup_creation_ and save_to_file
        """

        with open(file_name, "r") as file:
            file_contents = file.read()

        self.assertEqual(file_contents, contents)

    def test__backup_creation_(self):
        """
        Test whether _backup_creation_ can correctly rotate backups
        """

        logging.info(
            "Testing whether _backup_creation_ can correctly rotate backups")

        with open(self.test_file_name, "x") as file:
            file.write("")

        with open(self.test_file_name + self.backend.new_extension, "x") as file:
            file.write(self.test_file_text)

        self.backend._backup_creation_(save_file=self.test_file_name)

        self.helper_assert_file_contents(
            file_name=self.test_file_name + self.backend.backup_extension
        )

        self.helper_assert_file_contents(
            file_name=self.test_file_name,
            contents=self.test_file_text
        )

        os.remove(self.test_file_name + self.backend.backup_extension)
        os.remove(self.test_file_name)

    def helper_save_to_file(
        self,
        old_contents: str = "",
        new_contents: str = "",
        raw_file_name: str = None,
        backup_extension: str = None,
        test_full_file_name: str = None
    ):
        """
        Helper function for testing save_to_file
        """

        if raw_file_name is None:
            raw_file_name = self.test_file_name
        if backup_extension is None:
            backup_extension = self.backend.backup_extension
        if test_full_file_name is None:
            test_full_file_name = self.test_full_file_name

        self.backend.save_to_file(
            save_file=raw_file_name,
            save_info=new_contents
        )

        self.helper_assert_file_contents(
            file_name=test_full_file_name + backup_extension,
            contents=old_contents
        )
        self.helper_assert_file_contents(
            file_name=test_full_file_name,
            contents=new_contents
        )

    def test_save_to_file(self):
        """
        Test whether save_to_file can correctly create save files
        """

        logging.info(
            "Testing whether save_to_file can correctly create save files")

        self.backend.save_to_file(
            save_file=self.test_file_name,
            save_info=""
        )

        self.helper_assert_file_contents(file_name=self.test_full_file_name)

        self.helper_save_to_file(new_contents=self.test_file_text)

        self.helper_save_to_file(old_contents=self.test_file_text)

        os.remove(self.test_full_file_name + self.backend.backup_extension)
        os.remove(self.test_full_file_name)
        os.rmdir(self.backend.save_path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
