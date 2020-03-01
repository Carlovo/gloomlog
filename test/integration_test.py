import json
import logging
import unittest
from unittest import mock
import os
import shutil
import sys
sys.path.insert(0, "../")
sys.path.insert(0, "./")
from gloomcontroller import Controller  # noqa
from gloomview import UserInterfaceSave  # noqa


logging.basicConfig(level=logging.WARN, format="")


class TestInAndOut(unittest.TestCase):
    """
    Test exiting GloomLog and some simple user commands
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info(
            "Setting up variables for testing"
        )

        # TODO: check if there is a more Pythonic way for this
        assert not os.path.exists("__gloomsave__")

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
        Test whether a user can go to and exit the save interface
        """

        logging.info(
            "Testing whether a user can go to and exit the save interface"
        )

        self.controller.run()

        mock_exit.assert_called_once()
        mock_help.assert_called_once()

        os.remove("__gloomsave__/a.json.gml")
        os.rmdir("__gloomsave__")

    @mock.patch("gloomcontroller.Controller.exit_gloomlog")
    @mock.patch("builtins.input", side_effect="naclae")
    def test_loadnewsave_exit(self, mock_present, mock_exit):
        """
        Test whether a user can create a save file and load it
        """

        logging.info(
            "Testing whether a user can create a save file and load it"
        )

        self.controller.run()

        mock_exit.assert_called_once()

        os.remove("__gloomsave__/a.json.gml")
        os.rmdir("__gloomsave__")


class TestCorrectSaving(unittest.TestCase):
    """
    Test correct saving of GloomLog campaign save files
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info(
            "Setting up variables for testing"
        )

        # TODO: check if there is a more Pythonic way for this
        assert not os.path.exists("__gloomsave__")

        cls.controller = Controller()

    @mock.patch("gloomcontroller.Controller.exit_gloomlog")
    @mock.patch("builtins.input", side_effect="nae")
    def test_file_newsave(self, mock_present, mock_exit):
        """
        Test whether a new save is correctly created
        """

        logging.info(
            "Testing whether a new save is correctly created"
        )

        self.controller.run()

        # sanity check
        mock_exit.assert_called_once()

        with open("__gloomsave__/a.json.gml", "r") as file:
            test_text = file.read()
        with open("TestNewCampaignSave.json", "r") as file:
            validation_text = file.read()

        self.assertEqual(test_text, validation_text)

        os.remove("__gloomsave__/a.json.gml")
        os.rmdir("__gloomsave__")

    @mock.patch("gloomcontroller.Controller.exit_gloomlog")
    @mock.patch("builtins.input", side_effect="naas1BG4nac5Bar2Ae")
    def test_file_multiencounter(self, mock_present, mock_exit):
        """
        Test whether encounters can be added to a save file
        """

        logging.info(
            "Testing whether encounters can be added to a save file"
        )

        self.controller.run()

        # sanity check
        mock_exit.assert_called_once()

        with open("__gloomsave__/a.json.gml", "r") as file:
            test_text = file.read()
        with open("TestMultiEncounterSave.json", "r") as file:
            validation_text = file.read()

        self.assertEqual(test_text, validation_text)

        os.remove("__gloomsave__/a.json.gml.prev")
        os.remove("__gloomsave__/a.json.gml")
        os.rmdir("__gloomsave__")


class TestStdOut(unittest.TestCase):
    """
    Test whether GloomLog presents the right UI texts
    """

    # TODO:
    # implement global achievements
    # implement party achievements
    # implement golden chests loot
    # implement character retirement
    # implement available characters
    # implement available items
    # implement available events
    # implement available scenarios

    def setUp(self):
        """
        Set up variables for testing
        """

        logging.info(
            "Setting up variables for testing"
        )

        # TODO: check if there is a more Pythonic way for this
        assert not os.path.exists("__gloomsave__")

        self.controller = Controller()

        os.mkdir("__gloomsave__")
        shutil.copyfile(
            "TestMultiEncounterSave.json",
            "__gloomsave__/a.json.gml"
        )
        shutil.copyfile(
            "TestLongCampaignSave.json",
            "__gloomsave__/v.json.gml"
        )

    @mock.patch("gloomcontroller.Controller.exit_gloomlog")
    @mock.patch("builtins.input", side_effect="lale")
    @mock.patch("sys.stdout")
    def test_list_encounters(self, mock_stdout, mock_present, mock_exit):
        """
        Test whether GloomLog can correctly list the encounters had so far
        """

        logging.info(
            "Testing whether GloomLog can correctly list the encounters had so far"
        )

        self.controller.run()

        # sanity check
        mock_exit.assert_called_once()

        mock_stdout.assert_has_calls(
            [mock.call.write("City Event: 0.: A"),
             mock.call.write("Scenario: 1. B (G-4): failure"),
             mock.call.write("City Event: 5.: B"),
             mock.call.write("Road Event: 2.: A"),
             mock.call.write("ADD new encounter")],
            any_order=True
        )

    @mock.patch("gloomcontroller.Controller.exit_gloomlog")
    @mock.patch("builtins.input", side_effect="lvle")
    @mock.patch("sys.stdout")
    def test_list_campaign(self, mock_stdout, mock_present, mock_exit):
        """
        Test whether GloomLog can correctly list the encounters had so far
        """

        logging.info(
            "Testing whether GloomLog can correctly list the encounters had so far"
        )

        self.controller.run()

        # sanity check
        mock_exit.assert_called_once()

        mock_stdout.assert_has_calls(
            [mock.call.write("City Event: 0.: A"),
             mock.call.write("Treasure: 42."),
             mock.call.write("Scenario: 1. B (G-4): succes"),
             mock.call.write("Treasure: 17."),
             mock.call.write("Treasure: 1."),
             mock.call.write("Scenario: 2. L (D-8): failure"),
             mock.call.write("Scenario: 2. L (D-8): succes"),
             mock.call.write("City Event: 1.: B"),
             mock.call.write("Road Event: 9.: B"),
             mock.call.write("Treasure: 38."),
             mock.call.write("Scenario: 5. I (C-2): succes")],
            any_order=True
        )

    def tearDown(self):
        """
        Tear down variables for testing
        """

        logging.info(
            "Tearing down variables for testing"
        )

        os.remove("__gloomsave__/a.json.gml")
        os.remove("__gloomsave__/v.json.gml")
        os.rmdir("__gloomsave__")


if __name__ == "__main__":
    unittest.main(verbosity=2)
