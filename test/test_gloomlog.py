import sys
sys.path.insert(0, '../')
sys.path.insert(0, './')
import unittest
import logging
import gloomlog

logging.basicConfig(level=logging.INFO, format='')



class TestGloomlogGridLocation(unittest.TestCase):
    """
    Test Gloomlog's Location class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info("Setting up variables for testing")

        cls.gridLocChar = "G"
        cls.gridLocNumb = 10

        cls.gridLoc = gloomlog.GridLocation(cls.gridLocChar, cls.gridLocNumb)

    
    def testGridLocationCharacter(self):
        """
        Test whether the grid location character has been correctly set
        """

        logging.info("Testing whether the grid location character has been correctly set")
        
        self.assertEqual(self.gridLocChar, self.gridLoc.getCharacter())


    def testGridLocationNumber(self):
        """
        Test whether the grid location number has been correctly set
        """

        logging.info("Testing whether the grid location number has been correctly set")
        
        self.assertEqual(self.gridLocNumb, self.gridLoc.getNumber())
    

    def testGridLocationEqual(self):
        """
        Test whether the grid location can test equality
        """

        logging.info("Testing whether the grid location can test equality")

        gridLocCopy = gloomlog.GridLocation(self.gridLocChar, self.gridLocNumb)
        
        self.assertEqual(self.gridLoc, gridLocCopy)

    
    def testGridLocationString(self):
        """
        Test whether the grid location string representation is correct
        """

        logging.info("Testing whether the grid location string representation is correct")

        expectedString = "(" + self.gridLocChar + "-" + str(self.gridLocNumb) + ")"
        
        logging.info("Expected scenario string representation: " + expectedString)
        logging.info("Outputted scenario string representation: " + self.gridLoc.__str__())

        self.assertEqual(self.gridLoc.__str__(), expectedString)



class TestGloomlogScenario(unittest.TestCase):
    """
    Test Gloomlog's Scenario class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info("Setting up variables for testing")

        cls.number = 1
        cls.name = "Black Barrow"
        cls.gridLocChar = "G"
        cls.gridLocNumb = 10

        cls.scenTest = gloomlog.Scenario(cls.number, cls.name, gloomlog.GridLocation(cls.gridLocChar, cls.gridLocNumb))


    def testScenarioNumber(self):
        """
        Test whether the scenario number has been correctly set
        """

        logging.info("Testing whether the scenario number has been correctly set")
        
        self.assertEqual(self.number, self.scenTest.getNumber())
    

    def testScenarioName(self):
        """
        Test whether the scenario name has been correctly set
        """

        logging.info("Testing whether the scenario name has been correctly set")
        
        self.assertEqual(self.name, self.scenTest.getName())

    
    def testScenarioLocationEqual(self):
        """
        Test whether the scenario location has been correctly set
        """

        logging.info("Testing whether the scenario location has been correctly set")

        gridLocCopy = gloomlog.GridLocation(self.gridLocChar, self.gridLocNumb)
        
        self.assertEqual(self.scenTest.getGridLocation(), gridLocCopy)
    

    def testScenarioEqual(self):
        """
        Test whether the scenario can test equality
        """

        logging.info("Testing whether the scenario can test equality")

        scenCopy = gloomlog.Scenario(self.number, self.name, gloomlog.GridLocation(self.gridLocChar, self.gridLocNumb))
        
        self.assertEqual(self.scenTest, scenCopy)

    
    def testScenarioString(self):
        """
        Test whether the scenario string representation is correct
        """

        logging.info("Testing whether the scenario string representation is correct")

        expectedString = str(self.number) + ". " + self.name + " (" + self.gridLocChar + "-" + str(self.gridLocNumb) + ")"
        
        logging.info("Expected scenario string representation: " + expectedString)
        logging.info("Outputted scenario string representation: " + self.scenTest.__str__())

        self.assertEqual(self.scenTest.__str__(), expectedString)



if __name__ == "__main__":
    unittest.main(verbosity=2)
