import json


class Encounter(object):
    """
    An encouter from the game Gloomhaven
    Abstract class to capture scenarios and events
    """

    def __init__(self, number=None, encounterJSON=None):
        """
        number (int):
            the number of the Encounter
        encounterJSON (str):
            JSON representation of the Encounter

        Provide either a JSON or all other parameters as input.
        The JSON will override any other input if set.
        """

        # enforce only abstract use of this class
        assert type(self) != Encounter

        if encounterJSON is not None:
            # could return just int, but this is more consistent with other classes
            number, = self.fromJSON(encounterJSON)

        assert type(number) == int

        self.number = number

    def fromJSON(self, encounterJSON):
        """
        encounterJSON (str):
            JSON representation of the Encounter
        Returns a tuple with all input necessary to instantiate an Encounter object
        """

        assert type(encounterJSON) == str

        encounterDict = json.loads(encounterJSON)

        # could return just int, but this is more consistent with other classes
        return (encounterDict["number"],)

    def toJSON(self):
        """
        Returns the JSON string representation of the information in the Encounter (str)
        """

        nctrDict = {"number": self.number}

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


class GridLocation(object):
    """
    A location by the grid on the map of Gloomhaven
    """

    def __init__(self, character=None, number=None, gridLocationJSON=None):
        """
        character (single character string: A - O):
            the character denoting the horizontal / row value of the GridLocation
        number (int: 1 - 18):
            the number denoting the vertical / column value of the GridLocation

        gridLocationJSON (str):
            JSON representation of the GridLocation

        Provide either a JSON or all other parameters as input.
        The JSON will override any other input if set.
        """

        if gridLocationJSON is not None:
            character, number = self.fromJSON(gridLocationJSON)

        assert type(character) == str
        assert len(character) == 1

        assert 64 < ord(character) and ord(character) < 80

        assert type(number) == int
        assert 0 < number and number < 19

        self.character = character
        self.number = number

    def fromJSON(self, gridLocationJSON):
        """
        gridLocationJSON (str):
            JSON representation of the GridLocation
        Returns a tuple with all input necessary to instantiate an GridLocation object
        """

        assert type(gridLocationJSON) == str

        encounterDict = json.loads(gridLocationJSON)

        return (encounterDict["character"], encounterDict["number"])

    def toJSON(self):
        """
        Returns the JSON string representation of the information in the GridLocation
        """

        gridLocDict = {"character": self.character, "number": self.number}

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

    def __init__(self, number=None, name=None, gridLocation=None, scenarioJSON=None):
        """
        number (int):
            the number of the Scenario
        name (string):
            the name of the Scenario
        gridLocation (GridLocation):
            the grid location of the Scenario on the map of Gloomhaven
        """

        if scenarioJSON is not None:
            number, name, gridLocation = self.fromJSON(scenarioJSON)

        assert type(name) == str
        assert type(gridLocation) == GridLocation

        super().__init__(number)

        self.name = name
        self.gridLocation = gridLocation

    def fromJSON(self, scenarioJSON):
        """
        scenarioJSON (str):
            JSON representation of the Scenario
        Returns a tuple with all input necessary to instantiate an Scenario object
        """

        assert type(scenarioJSON) == str

        scenarioDict = json.loads(scenarioJSON)
        scenarioGridLoc = GridLocation(
            gridLocationJSON=json.dumps(scenarioDict["GridLocation"]))

        return (scenarioDict["number"], scenarioDict["name"], scenarioGridLoc)

    def toJSON(self):
        """
        Returns the JSON string representation of the information in the Scenario
        """

        scenarioDict = json.loads(super().toJSON())

        scenarioDict["name"] = self.name
        scenarioDict["GridLocation"] = json.loads(self.gridLocation.toJSON())

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

    def __init__(self, number=None, eventJSON=None):
        """
        number (int):
            the number of the event
        """

        assert type(self) != Event

        super().__init__(number=number, encounterJSON=eventJSON)

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
