import json
import logging
import unittest
from unittest import mock
import os
import sys
sys.path.insert(0, "../")
sys.path.insert(0, "./")
from gloomview import UserInterface, UserInterfaceMain, UserInterfaceSave  # noqa


logging.basicConfig(level=logging.WARN, format="")


class UserInterfaceCopy(UserInterface):
    """
    UserInterface is an abstract class, but its functionality should still be tested
    """
    pass


class TestUserInterfaceCopy(unittest.TestCase):
    """
    Test Gloomview's UserInterface class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info(
            "Setting up variables for testing Gloomview's UserInterface class"
        )

        cls.user_interface = UserInterfaceCopy()

        cls.faul_options = ("okay", "okay")

        cls.question_str = "Choose a taste."
        cls.answers_str = ("sweet", "sour", "bitter")

        # technically all user input is str, but it seems good to check correct parsing of ints
        cls.question_int = "What is your lucky number on a 6-sided die?"
        # remember: ranges include only starting number!
        cls.answers_int = tuple(str(i) for i in range(1, 7))

        cls.question_singular = "???"
        cls.answer_singular = ("ABC123!",)

        cls.bool_question_str = "Does it taste like chicken?"

    def test_no_options(self):
        """
        Test whether multiple_choice_question can correctly detect no options
        """

        logging.info(
            "Testing whether multiple_choice_question can correctly detect no options"
        )

        test_error = False

        try:
            self.user_interface.multiple_choice_question("Well?", ())
        except AssertionError:
            test_error = True
        finally:
            self.assertTrue(test_error)

    def test_faul_options(self):
        """
        Test whether multiple_choice_question can correctly detect double options
        """

        logging.info(
            "Testing whether multiple_choice_question can correctly detect double options"
        )

        test_error = False

        try:
            self.user_interface.multiple_choice_question(
                "Well?",
                self.faul_options
            )
        except AssertionError:
            test_error = True
        finally:
            self.assertTrue(test_error)

    @mock.patch("builtins.input", return_value="sour")
    def test_question_string(self, input):
        """
        Test whether multiple_choice_question can correctly parse str answers
        """

        logging.info(
            "Testing whether multiple_choice_question can correctly parse str answers"
        )

        answer = self.user_interface.multiple_choice_question(
            options=self.answers_str
        )

        self.assertEqual(answer, "sour")

    @mock.patch("builtins.input", return_value="4")
    def test_question_int(self, input):
        """
        Test whether multiple_choice_question can correctly parse int answers
        """

        logging.info(
            "Testing whether multiple_choice_question can correctly parse int answers"
        )

        answer = self.user_interface.multiple_choice_question(
            options=self.answers_int,
            question=self.question_int,
            range_options="blabla"
        )

        self.assertEqual(answer, "4")

    @mock.patch("builtins.input", return_value="2")
    def test_question_string_shortHand(self, input):
        """
        Test whether multiple_choice_question can correctly parse int shorthand answers
        """

        logging.info(
            "Testing whether multiple_choice_question can correctly parse int shorthand answers"
        )

        answer = self.user_interface.multiple_choice_question(
            options=self.answers_str,
            question=self.question_str
        )

        self.assertEqual(answer, "sour")

    @mock.patch("builtins.input", return_value="A")
    def test_question_singular(self, input):
        """
        Test whether multiple_choice_question can correctly parse short hand answers and single options
        """

        logging.info(
            "Testing whether multiple_choice_question can correctly parse short hand answers and single options"
        )

        answer = self.user_interface.multiple_choice_question(
            options=self.answer_singular,
            question=self.question_singular
        )

        self.assertEqual(answer, "ABC123!")

    @mock.patch("builtins.input", return_value="yes")
    def test_answer_yes(self, input):
        """
        Test whether yes_no_question can correctly parse "yes"
        """

        logging.info(
            "Testing whether yes_no_question can correctly parse 'yes'"
        )

        self.assertTrue(
            self.user_interface.yes_no_question(
                question=self.question_str
            )
        )

    @mock.patch("builtins.input", return_value="1")
    def test_answer_1(self, input):
        """
        Test whether yes_no_question can correctly parse "1"
        """

        logging.info(
            "Testing whether yes_no_question can correctly parse '1'"
        )

        self.assertTrue(self.user_interface.yes_no_question())

    @mock.patch("builtins.input", return_value="y")
    def test_answer_singular_yes(self, input):
        """
        Test whether yes_no_question can correctly parse "y"
        """

        logging.info(
            "Testing whether yes_no_question can correctly parse 'y'"
        )

        self.assertTrue(
            self.user_interface.yes_no_question(
                question=self.question_str
            )
        )

    @mock.patch("builtins.input", return_value="no")
    def test_answer_no(self, input):
        """
        Test whether yes_no_question can correctly parse "no"
        """

        logging.info(
            "Testing whether yes_no_question can correctly parse 'no'"
        )

        self.assertFalse(
            self.user_interface.yes_no_question(question=self.question_str)
        )

    @mock.patch("builtins.input", return_value="2")
    def test_answer_2(self, input):
        """
        Test whether yes_no_question can correctly parse "2"
        """

        logging.info(
            "Testing whether yes_no_question can correctly parse '2'"
        )

        self.assertFalse(
            self.user_interface.yes_no_question(question=self.question_str)
        )

    @mock.patch("builtins.input", return_value="n")
    def test_answer_singular_no(self, input):
        """
        Test whether yes_no_question can correctly parse "n"
        """

        logging.info(
            "Testing whether yes_no_question can correctly parse 'n'"
        )

        self.assertFalse(
            self.user_interface.yes_no_question()
        )


class TestUserInterfaceMain(unittest.TestCase):
    """
    Test GloomLog's UserInterfaceMain class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info(
            "Setting up variables for testing GloomLog's UserInterfaceMain class"
        )

        cls.user_interface_main = UserInterfaceMain([])

    @mock.patch("gloomview.UserInterface.present_interface")
    def test_present_super(self, mock_present):
        """
        Test whether present_interface can return from super
        """

        logging.info(
            "Testing whether present_interface can return from super"
        )

        self.user_interface_main.save_interface = None

        mock_present.return_value = True

        self.assertTrue(self.user_interface_main.present_interface())

        mock_present.assert_called_once()

    @mock.patch("gloomview.UserInterfaceSave.present_interface")
    def test_loop_save(self, mock_save):
        """
        Test whether present_interface can return from save
        """

        logging.info(
            "Testing whether present_interface can return from save"
        )

        self.user_interface_main.save_interface = UserInterfaceSave("test", [])

        mock_save.side_effect = [True, True, False]

        self.assertFalse(self.user_interface_main.present_interface())

    @mock.patch("gloomview.UserInterfaceSave.present_interface")
    def test_close_save(self, mock_save):
        """
        Test whether present_interface can parse a close return value
        """

        logging.info(
            "Testing whether present_interface can parse a close return value"
        )

        self.user_interface_main.save_interface = UserInterfaceSave("test", [])

        mock_save.return_value = 2

        self.assertTrue(self.user_interface_main.present_interface())

        self.assertEqual(self.user_interface_main.save_interface, None)

    @mock.patch("gloomview.UserInterfaceSave.present_interface")
    def test_save_update(self, mock_save):
        """
        Test whether present_interface can parse a save update
        """

        logging.info(
            "Testing whether present_interface can parse a save update"
        )

        test_save_interface = UserInterfaceSave("test", [])

        self.user_interface_main.save_interface = test_save_interface

        test_tuple = ("abc", "xyz")

        mock_save.return_value = test_tuple

        self.assertEqual(
            self.user_interface_main.present_interface(),
            test_tuple
        )

        self.assertEqual(
            self.user_interface_main.save_interface,
            test_save_interface
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
