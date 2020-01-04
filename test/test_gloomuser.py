import json
import logging
import unittest
from unittest.mock import patch
import os
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

        cls.questionStr = "Choose a taste."
        cls.answersStr = ('sweet', 'sour', 'bitter')

        # technically all user input is str, but it seems good to check correct parsing of ints
        cls.questionInt = "What is your lucky number on a 6-sided die?"
        # remember: ranges include only starting number!
        cls.answersInt = tuple(str(i) for i in range(1, 7))

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


class TestWriteNewTextFile(unittest.TestCase):
    """
    Test Gloomuser's writeNewTextFile function
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info(
            "Setting up variables for testing writeNewTextFile function")

        cls.testFileName = "test.txt"
        cls.testFileText = '{-a1_B":,"" 2]c3-)'

    def testWriteNewTextFile(self):
        """
        Test whether writeNewTextFile can correctly write a file
        """

        logging.info(
            "Testing whether writeNewTextFile can correctly write a file")

        gloomuser.writeNewTextFile(self.testFileName, self.testFileText)

        with open(self.testFileName, "r") as file:
            contents = file.read()

        assert contents == self.testFileText

        os.remove(self.testFileName)


class TestSaveToFile(unittest.TestCase):
    """
    Test Gloomuser's saveToFile function
    This unit test also tests the functionality of _backupCreation_
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info(
            "Setting up variables for testing saveToFile function")

        cls.testPath = "__test__"
        cls.testFileName = "test.txt"
        basePath = cls.testPath + "/" + cls.testFileName
        cls.testSaveFiles = {"current": basePath,
                             "backup": basePath + ".prev"}
        cls.testContents = ["ABC123", "456QWERTY", "DVORAK789"]

        # saveToFile will not fail on existance, but it should not be there yet
        assert not os.path.exists(cls.testPath)

    def helperFunctionFileContentCheck(self, pathName, contentExpected):
        """
        pathName (str): relative path of a file
        contentExpected (any readable): expected content of the file

        Helper function for opening files and checking their contents
        """

        assert type(pathName) == str

        with open(pathName, "r") as file:
            contentRead = file.read()

        self.assertEqual(contentRead, contentExpected)

    def testSaveToFile(self):
        """
        Test whether saveToFile can correctly create a save directory and write save files there
        """

        logging.info(
            "Testing whether saveToFile can correctly create a save directory and write save files there")

        for i in range(len(self.testContents)):
            gloomuser.saveToFile(
                self.testPath, self.testFileName, self.testContents[i])
            self.helperFunctionFileContentCheck(
                self.testSaveFiles["current"], self.testContents[i])
            if i > 0:
                self.helperFunctionFileContentCheck(
                    self.testSaveFiles["backup"], self.testContents[i - 1])
            else:
                self.assertFalse(os.path.exists(self.testSaveFiles["backup"]))

    @classmethod
    def tearDownClass(cls):
        """
        Remove files and directories that were created
        """

        logging.info("Remove files and directories that were created")

        os.remove(cls.testSaveFiles["current"])
        os.remove(cls.testSaveFiles["backup"])
        os.rmdir(cls.testPath)


if __name__ == "__main__":
    unittest.main(verbosity=2)
