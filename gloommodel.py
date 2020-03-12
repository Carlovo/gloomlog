import json


class HandlerJSON:
    """
    An abstract class to standardize JSON handling among objects
    """

    # It would be better to inherit from json.JSONEncoder or dict instead of object...
    # but json.JSONEncoder inheritance gives errors in the unittest framework...
    # and dict inheritance is limited in functionality

    def __init__(self):
        """
        There can only be none
        """

        # enforce only abstract use of this class
        assert type(self) != HandlerJSON

    def fromJSON(self, fullJSON: str) -> dict:
        """
        fullJSON (str):
            JSON representation of an object

        Checks whether the JSON is generally correct to form an object
        Strips the object header

        Returns a dict with the object parameters in the JSON
        """

        assert type(fullJSON) == str

        fullDict = json.loads(fullJSON)

        assert fullDict["type"] == type(self).__name__
        assert "data" in fullDict

        return fullDict["data"]

    def toJSON(self) -> str:
        """
        Returns the JSON string representation of the information in the object
        """

        # It would be better to inherit and override json.JSONEncoder.default() for this,
        # but that seems to give errors in the unittest framework

        return json.dumps(self, default=lambda o: {"type": type(o).__name__, "data": o.__dict__}, indent=2)


class Encounter(HandlerJSON):
    """
    An encouter from the game Gloomhaven
    Abstract class to capture scenarios and events
    """

    # should be overwritten by child classes
    friendly_name = "encounter"

    def __init__(self, number: int = None, unlockables: list = [], fullJSON: str = None):
        """
        number (int):
            the number of the Encounter
        unlockables (list of Encounter):
            list of Encounter objects this Encounter unlocked
        fullJSON (str):
            JSON representation of the Encounter

        Provide either a JSON or all other parameters as input.
        The JSON will override any other input if set.
        """

        # enforce only abstract use of this class
        assert type(self) != Encounter

        if fullJSON is not None:
            fullDict = self.fromJSON(fullJSON)
            number = fullDict["number"]
            unlockables = fullDict["unlockables"]

        assert type(number) == int
        assert type(unlockables) == list

        self.number = number
        self.unlockables = []

        for unlockable_dict in unlockables:
            unlockable_json = json.dumps(unlockable_dict)
            unlockable_class = globals()[unlockable_dict["type"]]
            unlockable_object = unlockable_class(fullJSON=unlockable_json)
            self.unlockables.append(unlockable_object)

    def __eq__(self, other) -> bool:
        """
        Other (Encounter):
            the encounter to compare to
        Return whether the two encounters are the same (bool)
        """

        return type(other) == type(self) and self.number == other.number

    def __str__(self) -> str:
        """
        Returns general info about the encouter (str)
        """

        return f"{self.friendly_name} {self.number}.".capitalize()


class GridLocation(HandlerJSON):
    """
    A location by the grid on the map of Gloomhaven
    """

    def __init__(self, character: str = None, number: int = None, fullJSON: str = None):
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

    def __eq__(self, other) -> bool:
        """
        other (GridLocation):
            the grid location to compare to
        Return whether the two grid location point to a similar GridLocation on the map of Gloomhaven
        (bool)
        """

        return type(other) == type(self) and self.character == other.character and self.number == other.number

    def __str__(self) -> str:
        """
        Returns general info about the GridLocation
        """

        return "(" + self.character + "-" + str(self.number) + ")"


class NamedEncounter(Encounter):
    """
    An abstract class for encounters with a name from the game Gloomhaven
    """

    # should be overwritten by child classes
    friendly_name = "named encounter"

    def __init__(
        self,
        number: int = None,
        name: str = None,
        unlockables: list = [],
        fullJSON: str = None
    ):
        """
        number (int):
            the number of the named encounter
        name (string):
            the name of the named encounter
        unlockables (list of Encounter):
            list of Encounter objects this Encounter unlocked

        Provide either a JSON or all other parameters as input.
        The JSON will override any other input if set.
        """

        if fullJSON is not None:
            fullDict = self.fromJSON(fullJSON)
            number = fullDict["number"]
            name = fullDict["name"]
            unlockables = fullDict["unlockables"]

        assert type(name) == str

        super().__init__(number, unlockables)

        self.name = name

    def __str__(self) -> str:
        """
        Returns general info about the named encounter
        """

        super_str = super().__str__()

        return f"{super_str} {self.name}"


class Scenario(NamedEncounter):
    """
    A scenario from the game Gloomhaven
    """

    friendly_name = "scenario"

    def __init__(
        self,
        number: int = None,
        name: str = None,
        gridLocation: GridLocation = None,
        succes=None,
        unlockables: list = [],
        fullJSON: str = None
    ):
        """
        number (int):
            the number of the Scenario
        name (string):
            the name of the Scenario
        gridLocation (GridLocation):
            the grid location of the Scenario on the map of Gloomhaven
        succes (bool or ""):
            bool for whether scenario was accomplished, "" if only unlocked
        unlockables (list of Encounter):
            list of Encounter objects this Encounter unlocked
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
                fullJSON=json.dumps(fullDict["gridLocation"])
            )
            succes = fullDict["succes"]
            unlockables = fullDict["unlockables"]

        assert type(gridLocation) == GridLocation
        assert type(succes) == bool or succes == ""

        super().__init__(number, name, unlockables)

        self.gridLocation = gridLocation
        self.succes = succes

    def __str__(self) -> str:
        """
        Returns general info about the Scenario
        """

        super_str = super().__str__()
        location_str = self.gridLocation.__str__()

        if self.succes == "":
            str_end = ""
        elif self.succes:
            str_end = ": succes"
        else:
            str_end = ": failure"

        return f"{super_str} {location_str}{str_end}"


class Event(Encounter):
    """
    An abstract class for events from the game Gloomhaven
    """

    # should be overwritten by child classes
    friendly_name = "event"

    def __init__(
        self,
        number: int = None,
        choice: str = None,
        unlockables: list = [],
        fullJSON: int = None
    ):
        """
        number (int):
            the number of the event
        choice ("A", "B" or ""):
            "A" or "B" for outcome choice, "" if only unlocked
        unlockables (list of Encounter):
            list of Encounter objects this Encounter unlocked
        """

        assert type(self) != Event

        if fullJSON is not None:
            fullDict = self.fromJSON(fullJSON)
            number = fullDict["number"]
            choice = fullDict["choice"]
            unlockables = fullDict["unlockables"]

        assert choice == "A" or choice == "B" or choice == ""

        super().__init__(number, unlockables)

        self.choice = choice

    def __str__(self) -> str:
        """
        Returns general info about the event
        """

        super_str = super().__str__()

        if self.choice:
            str_end = f": {self.choice}"
        else:
            str_end = ""

        return f"{super_str}{str_end}"


class RoadEvent(Event):
    """
    A class for road events from the game Gloomhaven
    """

    friendly_name = "road event"


class CityEvent(Event):
    """
    A class for city events from the game Gloomhaven
    """

    friendly_name = "city event"


class Treasure(Encounter):
    """
    An abstract class for treasure from the game Gloomhaven
    """

    friendly_name = "treasure"


class Quest(NamedEncounter):
    """
    A personal quest from the game Gloomhaven
    """

    friendly_name = "quest"


class ItemDesign(NamedEncounter):
    """
    An item design from the game Gloomhaven
    """

    friendly_name = "item design"


class IncrementalEncounter(Encounter):
    """
    An abstract class for incremental encounters from the game Gloomhaven
    Incremental encounters are encounters which number is the number of
    the previous encounter of the same type increased by one
    """

    # should be overwritten by child classes
    friendly_name = "Incremental encounter"


class Donation(IncrementalEncounter):
    """
    A sanctuary donation from the game Gloomhaven
    """

    friendly_name = "donation"


class AncientTechnology(IncrementalEncounter):
    """
    An ancient technology from the game Gloomhaven
    """

    friendly_name = "ancient technology"


if __name__ == "__main__":
    print("script contains only object definitions, no functional code on its own")
