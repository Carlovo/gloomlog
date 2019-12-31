import json


class HandlerJSON(object):
    """
    An abstract class to standardize JSON handling among objects
    """

    def __init__(self):
        """
        There can only be none
        """

        # enforce only abstract use of this class
        assert type(self) != HandlerJSON

    def fromJSON(self, fullJSON):
        """
        fullJSON (str):
            JSON representation of an object

        Checks whether the JSON is generally correct to form an object
        Strips the object header

        Returns a dict with the object parameters in the JSON
        """

        assert type(fullJSON) == str

        fullDict = json.loads(fullJSON)
        keysList = list(fullDict.keys())

        assert len(keysList) == 1
        assert keysList[0] == type(self).__name__

        return fullDict[type(self).__name__]


class Encounter(HandlerJSON):
    """
    An encouter from the game Gloomhaven
    Abstract class to capture scenarios and events
    """

    def __init__(self, number=None, fullJSON=None):
        """
        number (int):
            the number of the Encounter
        fullJSON (str):
            JSON representation of the Encounter

        Provide either a JSON or all other parameters as input.
        The JSON will override any other input if set.
        """

        # enforce only abstract use of this class
        assert type(self) != Encounter

        if fullJSON is not None:
            number = self.fromJSON(fullJSON)["number"]

        assert type(number) == int

        self.number = number

    def toJSON(self):
        """
        Returns the JSON string representation of the information in the Encounter (str)
        """

        nctrDict = {type(self).__name__: {"number": self.number}}

        return json.dumps(nctrDict, indent=2)

    def __eq__(self, other):
        """
        Other (Encounter):
            the encounter to compare to
        Return whether the two encounters are the same (bool)
        """

        assert type(other) == type(self)

        return self.number == other.number

    def __str__(self):
        """
        Returns general info about the encouter (str)
        """

        return str(self.number) + "."


class GridLocation(HandlerJSON):
    """
    A location by the grid on the map of Gloomhaven
    """

    def __init__(self, character=None, number=None, fullJSON=None):
        """
        character (single character string: A - O):
            the character denoting the horizontal / row value of the GridLocation
        number (int: 1 - 18):
            the number denoting the vertical / column value of the GridLocation

        fullJSON (str):
            JSON representation of the GridLocation

        Provide either a JSON or all other parameters as input.
        The JSON will override any other input if set.
        """

        if fullJSON is not None:
            fullDict = self.fromJSON(fullJSON)
            character = fullDict["character"]
            number = fullDict["number"]

        assert type(character) == str
        assert len(character) == 1

        assert 64 < ord(character) and ord(character) < 80

        assert type(number) == int
        assert 0 < number and number < 19

        self.character = character
        self.number = number

    def toJSON(self):
        """
        Returns the JSON string representation of the information in the GridLocation
        """

        gridLocDict = {"GridLocation": {
            "character": self.character, "number": self.number}}

        return json.dumps(gridLocDict, indent=2)

    def __eq__(self, other):
        """
        other (GridLocation):
            the grid location to compare to
        Return whether the two grid location point to a similar GridLocation on the map of Gloomhaven
        (bool)
        """

        assert type(other) == type(self)

        return self.character == other.character and self.number == other.number

    def __str__(self):
        """
        Returns general info about the GridLocation
        """

        return "(" + self.character + "-" + str(self.number) + ")"


class Scenario(Encounter):
    """
    A scenario from the game Gloomhaven
    """

    def __init__(self, number=None, name=None, gridLocation=None, fullJSON=None):
        """
        number (int):
            the number of the Scenario
        name (string):
            the name of the Scenario
        gridLocation (GridLocation):
            the grid location of the Scenario on the map of Gloomhaven
        fullJSON (str):
            JSON representation of the Scenario

        Provide either a JSON or all other parameters as input.
        The JSON will override any other input if set.
        """

        if fullJSON is not None:
            fullDict = self.fromJSON(fullJSON)
            number = fullDict["number"]
            name = fullDict["name"]
            gridLocation = GridLocation(
                fullJSON='{"GridLocation": ' + json.dumps(fullDict["GridLocation"]) + '}')

        assert type(name) == str
        assert type(gridLocation) == GridLocation

        super().__init__(number)

        self.name = name
        self.gridLocation = gridLocation

    def toJSON(self):
        """
        Returns the JSON string representation of the information in the Scenario
        """

        scenarioDict = json.loads(super().toJSON())

        scenarioDict["Scenario"]["name"] = self.name
        scenarioDict["Scenario"]["GridLocation"] = json.loads(
            self.gridLocation.toJSON())["GridLocation"]

        return json.dumps(scenarioDict, indent=2)

    def __str__(self):
        """
        Returns general info about the Scenario
        """

        return "Scenario: " + super().__str__() + " " + self.name + " " + self.gridLocation.__str__()


class Event(Encounter):
    """
    A abstract class for events from the game Gloomhaven
    """

    def __init__(self, number=None, fullJSON=None):
        """
        number (int):
            the number of the event
        """

        assert type(self) != Event

        super().__init__(number=number, fullJSON=fullJSON)

    def __str__(self):
        """
        Returns general info about the event
        """

        return "Event: " + super().__str__()


class RoadEvent(Event):
    """
    A class for road events from the game Gloomhaven
    """

    def __str__(self):
        """
        Returns general info about the road event
        """

        return "Road " + super().__str__()


class CityEvent(Event):
    """
    A class for city events from the game Gloomhaven
    """

    def __str__(self):
        """
        Returns general info about the city event
        """

        return "City " + super().__str__()


if __name__ == "__main__":
    print("script contains only object definitions, no functional code on its own")
