import json
import logging
import unittest
import sys
sys.path.insert(0, '../')
sys.path.insert(0, './')
import gloomlog  # noqa


logging.basicConfig(level=logging.WARN, format='')


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

        fileJSON = open("TestGloomlogEncounter.json", 'r')
        cls.textJSON = fileJSON.read()
        fileJSON.close()

        cls.nctrTest = EncounterCopy(cls.number)
        cls.nctrTestJSON = EncounterCopy(fullJSON=cls.textJSON)

    def helperFunctionEqualityAndFromJSON(self):
        """
        Helper function for testing the __eq__ and fromJSON methods
        """

        ncrtNumber, = self.nctrTest.fromJSON(self.textJSON)
        nctrCopy = EncounterCopy(ncrtNumber)

        self.assertEqual(self.nctrTest, nctrCopy)
        self.assertEqual(self.nctrTestJSON, nctrCopy)
        self.assertEqual(self.nctrTest, self.nctrTestJSON)

    def testEncounterNumber(self):
        """
        Test whether the Encounter number has been correctly set
        """

        logging.info(
            "Testing whether the Encounter number has been correctly set")

        self.assertEqual(self.number, self.nctrTest.number)

    def testEncounterFromJSON(self):
        """
        Test whether an Encounter can be succesfully generated from a correct JSON
        """

        logging.info(
            "Testing whether an Encounter can be succesfully generated from a correct JSON")

        self.helperFunctionEqualityAndFromJSON()

    def testEncounterToJSON(self):
        """
        Test whether the Encounter can generate a correct JSON with all information about itself
        """

        logging.info(
            "Testing whether the Encounter can generate a correct JSON with all information about itself")
        logging.info("Expected JSON: " + self.nctrTest.toJSON())

        self.assertEqual(self.textJSON, self.nctrTest.toJSON())

    def testEncounterEqual(self):
        """
        Test whether the Encounter can test equality
        """

        logging.info("Testing whether the Encounter can test equality")

        self.helperFunctionEqualityAndFromJSON()

    def testEncounterString(self):
        """
        Test whether the Encounter string representation is correct
        """

        logging.info(
            "Testing whether the Encounter string representation is correct")

        expectedString = str(self.number) + "."

        logging.info(
            "Expected Encounter string representation: " + expectedString)
        logging.info("Outputted Encounter string representation: " +
                     self.nctrTest.__str__())

        self.assertEqual(self.nctrTest.__str__(), expectedString)


class TestGloomlogGridLocation(unittest.TestCase):
    """
    Test Gloomlog's GridLocation class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info("Setting up variables for testing GridLocation class")

        cls.gridLocChar = "G"
        cls.gridLocNumb = 10

        fileJSON = open("TestGloomlogGridLocation.json", 'r')
        cls.textJSON = fileJSON.read()
        fileJSON.close()

        cls.gridLocTest = gloomlog.GridLocation(
            cls.gridLocChar, cls.gridLocNumb)
        cls.gridLocTestJSON = gloomlog.GridLocation(
            fullJSON=cls.textJSON)

    def helperFunctionEqualityAndFromJSON(self):
        """
        Helper function for testing the __eq__ and fromJSON methods
        """

        gridLocCharacter, gridLocNumber = self.gridLocTest.fromJSON(
            self.textJSON)
        gridLocCopy = gloomlog.GridLocation(gridLocCharacter, gridLocNumber)

        self.assertEqual(self.gridLocTest, gridLocCopy)
        self.assertEqual(self.gridLocTestJSON, gridLocCopy)
        self.assertEqual(self.gridLocTest, self.gridLocTestJSON)

    def testGridLocationCharacter(self):
        """
        Test whether the GridLocation character has been correctly set
        """

        logging.info(
            "Testing whether the GridLocation character has been correctly set")

        self.assertEqual(self.gridLocChar, self.gridLocTest.character)

    def testGridLocationNumber(self):
        """
        Test whether the GridLocation number has been correctly set
        """

        logging.info(
            "Testing whether the GridLocation number has been correctly set")

        self.assertEqual(self.gridLocNumb, self.gridLocTest.number)

    def testGridLocationFromJSON(self):
        """
        Test whether a GridLocation can be succesfully generated from a correct JSON
        """

        logging.info(
            "Testing whether a GridLocation can be succesfully generated from a correct JSON")

        self.helperFunctionEqualityAndFromJSON()

    def testGridLocationToJSON(self):
        """
        Test whether the GridLocation can generate a correct JSON with all information about itself
        """

        logging.info(
            "Testing whether the GridLocation can generate a correct JSON with all information about itself")
        logging.info("Expected JSON: " + self.gridLocTest.toJSON())

        fileJSON = open("TestGloomlogGridLocation.json", 'r')
        textJSON = fileJSON.read()
        fileJSON.close()

        self.assertEqual(textJSON, self.gridLocTest.toJSON())

    def testGridLocationEqual(self):
        """
        Test whether the GridLocation can test equality
        """

        logging.info("Testing whether the GridLocation can test equality")

        self.helperFunctionEqualityAndFromJSON()

    def testGridLocationString(self):
        """
        Test whether the GridLocation string representation is correct
        """

        logging.info(
            "Testing whether the GridLocation string representation is correct")

        expectedString = "(" + self.gridLocChar + "-" + \
            str(self.gridLocNumb) + ")"

        logging.info(
            "Expected scenario string representation: " + expectedString)
        logging.info("Outputted scenario string representation: " +
                     self.gridLocTest.__str__())

        self.assertEqual(self.gridLocTest.__str__(), expectedString)


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

        fileJSON = open("TestGloomlogScenario.json", 'r')
        cls.textJSON = fileJSON.read()
        fileJSON.close()

        cls.scenTest = gloomlog.Scenario(
            cls.number, cls.name, gloomlog.GridLocation(cls.gridLocChar, cls.gridLocNumb))
        cls.scenTestJSON = gloomlog.Scenario(fullJSON=cls.textJSON)

    def testScenarioFromJSON(self):
        """
        Test whether a Scenario can be succesfully generated from a correct JSON
        """

        logging.info(
            "Testing whether a Scenario can be succesfully generated from a correct JSON")

        scenNumber, scenName, scenGridLoc = self.scenTest.fromJSON(
            self.textJSON)
        scenCopy = gloomlog.Scenario(scenNumber, scenName, scenGridLoc)

        self.assertEqual(self.scenTest, scenCopy)
        self.assertEqual(self.scenTestJSON, scenCopy)
        self.assertEqual(self.scenTest, self.scenTestJSON)

    def testScenarioName(self):
        """
        Test whether the Scenario name has been correctly set
        """

        logging.info(
            "Testing whether the Scenario name has been correctly set")

        self.assertEqual(self.name, self.scenTest.name)

    def testScenarioToJSON(self):
        """
        Test whether the Scenario can generate a correct JSON with all information about itself
        """

        logging.info(
            "Testing whether the Scenario can generate a correct JSON with all information about itself")
        logging.info("Expected JSON: " + self.scenTest.toJSON())

        fileJSON = open("TestGloomlogScenario.json", 'r')
        textJSON = fileJSON.read()
        fileJSON.close()

        self.assertEqual(textJSON, self.scenTest.toJSON())

    def testScenarioLocationEqual(self):
        """
        Test whether the scenario location has been correctly set
        """

        logging.info(
            "Testing whether the scenario location has been correctly set")

        gridLocCopy = gloomlog.GridLocation(self.gridLocChar, self.gridLocNumb)

        self.assertEqual(self.scenTest.gridLocation, gridLocCopy)

    def testScenarioString(self):
        """
        Test whether the scenario string representation is correct
        """

        logging.info(
            "Testing whether the scenario string representation is correct")

        expectedString = "Scenario: " + \
            str(self.number) + ". " + self.name + \
            " (" + self.gridLocChar + "-" + str(self.gridLocNumb) + ")"

        logging.info(
            "Expected scenario string representation: " + expectedString)
        logging.info("Outputted scenario string representation: " +
                     self.scenTest.__str__())

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

        cls.eventTest = EventCopy(cls.number)

    def testEventString(self):
        """
        Test whether the Event string representation is correct
        """

        logging.info(
            "Testing whether the Event string representation is correct")

        expectedString = "Event: " + str(self.number) + "."

        logging.info("Expected Event string representation: " + expectedString)
        logging.info("Outputted Event string representation: " +
                     self.eventTest.__str__())

        self.assertEqual(self.eventTest.__str__(), expectedString)


class TestGloomlogRoadEvent(unittest.TestCase):
    """
    Test Gloomlog's RoadEvent class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info("Setting up variables for testing RoadEvent class")

        cls.number = 1000

        cls.roadEventTest = gloomlog.RoadEvent(cls.number)

    def testRoadEventString(self):
        """
        Test whether the RoadEvent string representation is correct
        """

        logging.info(
            "Testing whether the RoadEvent string representation is correct")

        expectedString = "Road Event: " + str(self.number) + "."

        logging.info(
            "Expected RoadEvent string representation: " + expectedString)
        logging.info("Outputted RoadEvent string representation: " +
                     self.roadEventTest.__str__())

        self.assertEqual(self.roadEventTest.__str__(), expectedString)


class TestGloomlogCityEvent(unittest.TestCase):
    """
    Test Gloomlog's CityEvent class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info("Setting up variables for testing CityEvent class")

        cls.number = 1000

        cls.cityEventTest = gloomlog.CityEvent(cls.number)

    def testCityEventString(self):
        """
        Test whether the CityEvent string representation is correct
        """

        logging.info(
            "Testing whether the CityEvent string representation is correct")

        expectedString = "City Event: " + str(self.number) + "."

        logging.info(
            "Expected CityEvent string representation: " + expectedString)
        logging.info("Outputted CityEvent string representation: " +
                     self.cityEventTest.__str__())

        self.assertEqual(self.cityEventTest.__str__(), expectedString)


if __name__ == "__main__":
    unittest.main(verbosity=2)
