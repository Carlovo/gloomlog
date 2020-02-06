import json
import logging
import unittest
from unittest.mock import patch
import os
import sys
sys.path.insert(0, '../')
sys.path.insert(0, './')
from gloomview import UserInterface, UserInterfaceMain, UserInterfaceSave  # noqa


logging.basicConfig(level=logging.WARN, format='')


class TestMultipleChoiceQuestion(unittest.TestCase):
    """
    Test Gloomuser's multipleChoiceQuestion function
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info(
            "Setting up variables for testing multipleChoiceQuestion function")

        cls.faulOptions = ('okay', 'okay')

        cls.questionStr = "Choose a taste."
        cls.answersStr = ('sweet', 'sour', 'bitter')

        # technically all user input is str, but it seems good to check correct parsing of ints
        cls.questionInt = "What is your lucky number on a 6-sided die?"
        # remember: ranges include only starting number!
        cls.answersInt = tuple(str(i) for i in range(1, 7))

        cls.questionSingular = "???"
        cls.answerSingular = ('ABC123!',)

    def testNoOptions(self):
        """
        Test whether multipleChoiceQuestion can correctly detect no options
        """

        logging.info(
            "Testing whether multipleChoiceQuestion can correctly detect no options")

        testError = False

        try:
            gloomuser.multipleChoiceQuestion("Well?", ())
        except AssertionError:
            testError = True
        finally:
            self.assertTrue(testError)

    def testFaulOptions(self):
        """
        Test whether multipleChoiceQuestion can correctly detect double options
        """

        logging.info(
            "Testing whether multipleChoiceQuestion can correctly detect double options")

        testError = False

        try:
            gloomuser.multipleChoiceQuestion("Well?", self.faulOptions)
        except AssertionError:
            testError = True
        finally:
            self.assertTrue(testError)

    @patch('builtins.input', return_value='sour')
    def testQuestionString(self, input):
        """
        Test whether multipleChoiceQuestion can correctly parse str answers
        """

        logging.info(
            "Testing whether multipleChoiceQuestion can correctly parse str answers")

        self.assertEqual(gloomuser.multipleChoiceQuestion(
            self.questionStr, self.answersStr), 'sour')

    @patch('builtins.input', return_value='4')
    def testQuestionInt(self, input):
        """
        Test whether multipleChoiceQuestion can correctly parse int answers
        """

        logging.info(
            "Testing whether multipleChoiceQuestion can correctly parse int answers")

        self.assertEqual(gloomuser.multipleChoiceQuestion(
            self.questionInt, self.answersInt), '4')

    @patch('builtins.input', return_value='2')
    def testQuestionStringShortHand(self, input):
        """
        Test whether multipleChoiceQuestion can correctly parse int shorthand answers
        """

        logging.info(
            "Testing whether multipleChoiceQuestion can correctly parse int shorthand answers")

        self.assertEqual(gloomuser.multipleChoiceQuestion(
            self.questionStr, self.answersStr), 'sour')

    @patch('builtins.input', return_value='A')
    def testQuestionSingular(self, input):
        """
        Test whether multipleChoiceQuestion can correctly parse short hand answers and single options
        """

        logging.info(
            "Testing whether multipleChoiceQuestion can correctly parse short hand answers and single options")

        self.assertEqual(gloomuser.multipleChoiceQuestion(
            self.questionSingular, self.answerSingular), 'ABC123!')


class TestYesNoQuestion(unittest.TestCase):
    """
    Test Gloomuser's yesNoQuestion function
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info(
            "Setting up variables for testing yesNoQuestion function")

        cls.questionStr = "Does it taste like chicken?"

    @patch('builtins.input', return_value='yes')
    def testAnswerYes(self, input):
        """
        Test whether yesNoQuestion can correctly parse 'yes'
        """

        logging.info(
            "Testing whether yesNoQuestion can correctly parse 'yes'")

        self.assertTrue(gloomuser.yesNoQuestion(self.questionStr))

    @patch('builtins.input', return_value='1')
    def testAnswer1(self, input):
        """
        Test whether yesNoQuestion can correctly parse '1'
        """

        logging.info(
            "Testing whether yesNoQuestion can correctly parse '1'")

        self.assertTrue(gloomuser.yesNoQuestion(self.questionStr))

    @patch('builtins.input', return_value='y')
    def testAnswerSingularYes(self, input):
        """
        Test whether yesNoQuestion can correctly parse 'y'
        """

        logging.info(
            "Testing whether yesNoQuestion can correctly parse 'y'")

        self.assertTrue(gloomuser.yesNoQuestion(self.questionStr))

    @patch('builtins.input', return_value='no')
    def testAnswerNo(self, input):
        """
        Test whether yesNoQuestion can correctly parse 'no'
        """

        logging.info(
            "Testing whether yesNoQuestion can correctly parse 'no'")

        self.assertFalse(gloomuser.yesNoQuestion(self.questionStr))

    @patch('builtins.input', return_value='2')
    def testAnswer2(self, input):
        """
        Test whether yesNoQuestion can correctly parse '2'
        """

        logging.info(
            "Testing whether yesNoQuestion can correctly parse '2'")

        self.assertFalse(gloomuser.yesNoQuestion(self.questionStr))

    @patch('builtins.input', return_value='n')
    def testAnswerSingularNo(self, input):
        """
        Test whether yesNoQuestion can correctly parse 'n'
        """

        logging.info(
            "Testing whether yesNoQuestion can correctly parse 'n'")

        self.assertFalse(gloomuser.yesNoQuestion(self.questionStr))


if __name__ == "__main__":
    unittest.main(verbosity=2)
