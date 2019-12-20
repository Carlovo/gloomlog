import json
import logging
import unittest
from unittest.mock import patch
import sys
sys.path.insert(0, '../')
sys.path.insert(0, './')
import gloomuser  # noqa


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

        cls.questionStr = "Does it taste like chicken?"
        cls.answersStr = ["yes", "no"]

        # technically all user input is str, but it seems good to check correct parsing of ints
        cls.questionInt = "What is your lucky number on a 6-sided die?"
        # ranges include only starting number!
        cls.answersInt = [str(i) for i in range(1, 7)]

    @patch('builtins.input', return_value='yes')
    def testQuestionString(self, input):
        """
        Test whether multipleChoiceQuestion can correctly parse str answers
        """

        logging.info(
            "Testing whether multipleChoiceQuestion can correctly parse str answers")

        self.assertEqual(gloomuser.multipleChoiceQuestion(
            self.questionStr, self.answersStr), 'yes')

    @patch('builtins.input', return_value='4')
    def testQuestionInt(self, input):
        """
        Test whether multipleChoiceQuestion can correctly parse int answers
        """

        logging.info(
            "Testing whether multipleChoiceQuestion can correctly parse int answers")

        self.assertEqual(gloomuser.multipleChoiceQuestion(
            self.questionInt, self.answersInt), '4')


if __name__ == "__main__":
    unittest.main(verbosity=2)
