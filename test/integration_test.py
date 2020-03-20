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
    @mock.patch("builtins.input", side_effect=[
        "new",  # "Please choose from" -> "Create NEW campaign save file"
        "testers",  # "How would you like to call your campaign save file?: "
        "add",  # "What would you like to do with campaign save 'testers'?" -> "ADD new encounter"
        "treasure",  # "What type of encounter?"
        "18",  # "What is the treasure's identifier number?"
        "yes",  # "Would you like to add an unlocked encounter?"
        "scenario",  # "What type of encounter?"
        "5",  # "What is the scenario's identifier number?"
        "Candy Mountain",  # "What is the scenario's name?"
        "C",  # "What is the character of that scenario's location?"
        "2",  # "What is the identifier number of that scenario's location?"
        "no",  # "Would you like to add an unlocked encounter?"
        "add",  # "What would you like to do with campaign save 'testers'?" -> "ADD new encounter"
        "scenario",  # "What type of encounter?"
        "1",  # "What is the scenario's identifier number?"
        "Black Barrow",  # "What is the scenario's name?"
        "G",  # "What is the character of that scenario's location?"
        "4",  # "What is the identifier number of that scenario's location?"
        "no",  # "Did you succesfully complete the scenario?"
        "no",  # "Would you like to add an unlocked encounter?"
        "add",  # "What would you like to do with campaign save 'testers'?" -> "ADD new encounter"
        "donation",  # "What type of encounter?"
        "no",  # "Would you like to add an unlocked encounter?"
        "add",  # "What would you like to do with campaign save 'testers'?" -> "ADD new encounter"
        "donation",  # "What type of encounter?"
        "no",  # "Would you like to add an unlocked encounter?"
        "add",  # "What would you like to do with campaign save 'testers'?" -> "ADD new encounter"
        "quest",  # "What type of encounter?"
        "511",  # "What is the quest's identifier number?"
        "Because we can",  # "What is the quest's name?"
        "yes",  # "Would you like to add an unlocked encounter?"
        "character",  # "What type of encounter?"
        "Sassy Savvas",  # "What is the character's identifier name?"
        "yes",  # "Would you like to add an unlocked encounter?"
        "city event",  # "What type of encounter?"
        "40",  # "What is the city event's identifier number?"
        "yes",  # "Would you like to add an unlocked encounter?"
        "road event",  # "What type of encounter?"
        "58",  # "What is the road event's identifier number?"
        "no",  # "Would you like to add an unlocked encounter?"
        "add",  # "What would you like to do with campaign save 'testers'?" -> "ADD new encounter"
        "city event",  # "What type of encounter?"
        "5",  # "What is the city event's identifier number?"
        "B",  # "Which option did you choose?"
        "yes",  # Should the event be removed from the game?
        "no",  # "Would you like to add an unlocked encounter?"
        "add",  # "What would you like to do with campaign save 'testers'?" -> "ADD new encounter"
        "road event",  # "What type of encounter?"
        "2",  # "What is the road event's identifier number?"
        "A",  # "Which option did you choose?"
        "no",  # Should the event be removed from the game?
        "no",  # "Would you like to add an unlocked encounter?"
        "exit"  # "What would you like to do with campaign save 'testers'?" -> "EXIT GloomLog"
    ])
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

        with open("__gloomsave__/testers.json.gml", "r") as file:
            test_text = file.read()
        with open("TestMultiEncounterSave.json", "r") as file:
            validation_text = file.read()

        self.assertEqual(test_text, validation_text)

        os.remove("__gloomsave__/testers.json.gml.prev")
        os.remove("__gloomsave__/testers.json.gml")
        os.rmdir("__gloomsave__")


class TestStdOut(unittest.TestCase):
    """
    Test whether GloomLog presents the right UI texts
    """

    # TODO:
    # implement available characters
    # implement available items
    # implement available events
    # implement available scenarios
    # implement Drake achievements
    # implement Gloomhaven prosperity
    # implement Party reputation

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
            [mock.call.write("City event 0.: A"),
             mock.call.write("Treasure 18."),
             mock.call.write("Scenario 1. Black Barrow (G-4): failure"),
             mock.call.write("Donation 1."),
             mock.call.write("Donation 2."),
             mock.call.write("Quest 511. Because we can"),
             mock.call.write("City event 5.: B-"),
             mock.call.write("Road event 2.: A"),
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

        # TODO: implement and uncomment below
        mock_stdout.assert_has_calls(
            [mock.call.write("Donation 1."),
             mock.call.write("City event 0.: A-"),
             mock.call.write("Donation 2."),
             mock.call.write("Quest 537. Help Vermlings"),
             mock.call.write("+ Character Sassy Savvas"),
             mock.call.write("+ Road event 40."),
             mock.call.write("+ City event 40."),
             mock.call.write("+ Road event 58."),
             mock.call.write("+ City event 58."),
             mock.call.write("Donation 3."),
             mock.call.write("Road event 13.: B"),
             mock.call.write("+ Ancient technology 1."),
             mock.call.write("Treasure 42."),
             mock.call.write("+ Scenario 18. High Ocean (H-11)"),
             mock.call.write("Scenario 1. Black Barrel (G-4): succes"),
             mock.call.write("+ Party achievement Leave the City"),
             mock.call.write("+ Scenario 2. Left Hill (D-8)"),
             mock.call.write("Treasure 17."),
             mock.call.write("Treasure 1."),
             mock.call.write("Scenario 2. Left Hill (D-8): failure"),
             mock.call.write("Scenario 2. Left Hill (D-8): succes"),
             mock.call.write("+ Ancient technology 2."),
             mock.call.write("+ Road event 9."),
             mock.call.write("Quest 512. Kill Enemies"),
             mock.call.write("+ Scenario 5. Candy Mountain (C-2)"),
             mock.call.write("+ Item design 143. Sharp Arrow"),
             mock.call.write("City event 1.: B"),
             mock.call.write("+ Item design 112. Expensive Crown"),
             mock.call.write("Donation 4."),
             mock.call.write("Donation 5."),
             mock.call.write("Road event 9.: B-"),
             mock.call.write("+ City event 31."),
             mock.call.write("Treasure 38."),
             mock.call.write("+ Item design 97. Old Coin"),
             mock.call.write("Scenario 5. Candy Mountain (C-2): succes"),
             mock.call.write("+ Global achievement Candy Eaten"),
             mock.call.write("+ City event 33."),
             mock.call.write("City event 17.: B"),
             mock.call.write("Road event 24.: A")],
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
