import sys
sys.path.insert(0, '../')
sys.path.insert(0, './')
import unittest
import logging
import gloomlog

logging.basicConfig(level=logging.INFO, format='')



class EncounterCopy(gloomlog.Encounter):
    """
    Encounter is an abstract class, but its functionality should still be tested
    """
    pass



class EventCopy(gloomlog.Event):
    """
    Event is an abstract class, but its functionality should still be tested
    """
    pass



class TestGloomlogEncounter(unittest.TestCase):
    """
    Test Gloomlog's Encounter class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info("Setting up variables for testing Encounter class")

        cls.number = 1000
        cls.name = "Toeter toetert"

        cls.nctrTest = EncounterCopy(cls.number, cls.name)


    def testEncounterNumber(self):
        """
        Test whether the Encounter number has been correctly set
        """

        logging.info("Testing whether the Encounter number has been correctly set")
        
        self.assertEqual(self.number, self.nctrTest.getNumber())
    

    def testEncounterName(self):
        """
        Test whether the Encounter name has been correctly set
        """

        logging.info("Testing whether the Encounter name has been correctly set")
        
        self.assertEqual(self.name, self.nctrTest.getName())
    

    def testEncounterEqual(self):
        """
        Test whether the Encounter can test equality
        """

        logging.info("Testing whether the Encounter can test equality")

        nctrCopy = EncounterCopy(self.number, self.name)
        
        self.assertEqual(self.nctrTest, nctrCopy)

    
    def testEncounterString(self):
        """
        Test whether the Encounter string representation is correct
        """

        logging.info("Testing whether the Encounter string representation is correct")

        expectedString = str(self.number) + ". " + self.name
        
        logging.info("Expected Encounter string representation: " + expectedString)
        logging.info("Outputted Encounter string representation: " + self.nctrTest.__str__())

        self.assertEqual(self.nctrTest.__str__(), expectedString)



class TestGloomlogGridLocation(unittest.TestCase):
    """
    Test Gloomlog's Location class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info("Setting up variables for testing Location class")

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

        logging.info("Setting up variables for testing Scenario class")

        cls.number = 1
        cls.name = "Black Barrow"
        cls.gridLocChar = "G"
        cls.gridLocNumb = 10

        cls.scenTest = gloomlog.Scenario(cls.number, cls.name, gloomlog.GridLocation(cls.gridLocChar, cls.gridLocNumb))

    
    def testScenarioLocationEqual(self):
        """
        Test whether the scenario location has been correctly set
        """

        logging.info("Testing whether the scenario location has been correctly set")

        gridLocCopy = gloomlog.GridLocation(self.gridLocChar, self.gridLocNumb)
        
        self.assertEqual(self.scenTest.getGridLocation(), gridLocCopy)


    
    def testScenarioString(self):
        """
        Test whether the scenario string representation is correct
        """

        logging.info("Testing whether the scenario string representation is correct")

        expectedString = str(self.number) + ". " + self.name + " (" + self.gridLocChar + "-" + str(self.gridLocNumb) + ")"
        
        logging.info("Expected scenario string representation: " + expectedString)
        logging.info("Outputted scenario string representation: " + self.scenTest.__str__())

        self.assertEqual(self.scenTest.__str__(), expectedString)



class TestGloomlogEvent(unittest.TestCase):
    """
    Test Gloomlog's Event class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info("Setting up variables for testing Event class")

        cls.number = 1000
        cls.name = "Toeter toetert"

        cls.eventTest = EventCopy(cls.number, cls.name)
    

    def testEventString(self):
        """
        Test whether the Event string representation is correct
        """

        logging.info("Testing whether the Event string representation is correct")

        expectedString = "Event: " + str(self.number) + ". " + self.name
        
        logging.info("Expected Event string representation: " + expectedString)
        logging.info("Outputted Event string representation: " + self.eventTest.__str__())

        self.assertEqual(self.eventTest.__str__(), expectedString)



if __name__ == "__main__":
    unittest.main(verbosity=2)
