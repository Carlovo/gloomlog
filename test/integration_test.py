import json
import logging
import unittest
from unittest import mock
import os
import sys
sys.path.insert(0, "../")
sys.path.insert(0, "./")
from gloomcontroller import Controller  # noqa
from gloomview import UserInterfaceSave  # noqa


logging.basicConfig(level=logging.WARN, format="")


class TestInAndOut(unittest.TestCase):
    """
    Test exiting GloomLog
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info(
            "Setting up variables for testing"
        )

        cls.controller = Controller()

    @mock.patch("gloomcontroller.Controller.exit_gloomlog")
    @mock.patch("builtins.input", return_value="e")
    def test_immediately_exit(self, mock_present, mock_exit):
        """
        Test whether a user can immediately exit GloomLog
        """

        logging.info(
            "Testing whether a user can immediately exit GloomLog"
        )

        self.controller.run()

        mock_exit.assert_called_once()

    @mock.patch("gloomcontroller.UserInterfaceMain.print_help")
    @mock.patch("gloomcontroller.Controller.exit_gloomlog")
    @mock.patch("builtins.input", side_effect="he")
    def test_help_exit(self, mock_present, mock_exit, mock_help):
        """
        Test whether a user can exit GloomLog after reading help
        """

        logging.info(
            "Testing whether a user can exit GloomLog after reading help"
        )

        self.controller.run()

        mock_exit.assert_called_once()
        mock_help.assert_called_once()

    @mock.patch("gloomview.UserInterfaceSave.print_help")
    @mock.patch("gloomcontroller.Controller.exit_gloomlog")
    @mock.patch("builtins.input", side_effect="nahce")
    def test_newsave_help_close_exit(self, mock_present, mock_exit, mock_help):
        """
        Test whether a user can immediately exit GloomLog
        """

        logging.info(
            "Testing whether a user can immediately exit GloomLog"
        )

        self.controller.run()

        mock_exit.assert_called_once()
        mock_help.assert_called_once()

        os.remove("__gloomsave__/a.json.gml")
        os.rmdir("__gloomsave__")


if __name__ == "__main__":
    unittest.main(verbosity=2)
