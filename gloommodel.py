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

        return json.dumps(self, default=lambda o: {"type": type(o).__name__, "data": o.__dict__}, indent=2, sort_keys=True)


class GridLocation(HandlerJSON):
    """
    A location by the grid on the map of Gloomhaven
    """

    def __init__(self, character: str = None, identifier: int = None, fullJSON: str = None):
        """
        character (single character string: A - O):
            the character denoting the horizontal / row value of the GridLocation
        identifier (int: 1 - 18):
            the identifier denoting the vertical / column value of the GridLocation

        fullJSON (str):
            JSON representation of the GridLocation

        Provide either a JSON or all other parameters as input.
        The JSON will override any other input if set.
        """

        if fullJSON is not None:
            fullDict = self.fromJSON(fullJSON)
            character = fullDict["character"]
            identifier = fullDict["identifier"]

        assert type(character) == str
        assert len(character) == 1

        assert 64 < ord(character) and ord(character) < 80

        assert type(identifier) == int
        assert 0 < identifier and identifier < 19

        self.character = character
        self.identifier = identifier

    def __eq__(self, other) -> bool:
        """
        other (GridLocation):
            the grid location to compare to
        Return whether the two grid location point to a similar GridLocation on the map of Gloomhaven
        (bool)
        """

        return type(other) == type(self) and self.character == other.character and self.identifier == other.identifier

    def __str__(self) -> str:
        """
        Returns general info about the GridLocation
        """

        return "(" + self.character + "-" + str(self.identifier) + ")"


class Encounter(HandlerJSON):
    """
    An encouter from the game Gloomhaven
    Abstract class to capture as much as possible of what is in Gloomhaven
    """

    # should be overwritten by child classes
    friendly_name = "encounter"

    def __init__(self, identifier=None, unlockables: list = [], fullJSON: str = None):
        """
        identifier (something unique):
            the identifier of the Encounter
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
            identifier = fullDict["identifier"]
            unlockables = fullDict["unlockables"]

        assert type(unlockables) == list

        self.identifier = identifier
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

        return type(other) == type(self) and self.identifier == other.identifier

    def __str__(self) -> str:
        """
        Returns general info about the encouter (str)
        """

        capitalized_friendly_name = self.friendly_name.capitalize()

        return f"{capitalized_friendly_name} {self.identifier}"


class EncounterByName(Encounter):
    """
    An encouter identified with a unique name from the game Gloomhaven
    Abstract class to capture mostly available characters and achievements
    """

    # should be overwritten by child classes
    friendly_name = "numbered by number"

    def __init__(self, identifier: str = None, unlockables: list = [], fullJSON: str = None):
        """
        identifier (int):
            the identifier of the Encounter
        unlockables (list of Encounter):
            list of Encounter objects this Encounter unlocked
        fullJSON (str):
            JSON representation of the Encounter

        Provide either a JSON or all other parameters as input.
        The JSON will override any other input if set.
        """

        # enforce only abstract use of this class
        assert type(self) != EncounterByName

        super().__init__(
            identifier=identifier,
            unlockables=unlockables,
            fullJSON=fullJSON
        )

        assert type(self.identifier) == str


class Character(EncounterByName):
    """
    An ancient technology from the game Gloomhaven
    """

    friendly_name = "character"


class PartyAchievement(EncounterByName):
    """
    A party achievement from the game Gloomhaven
    """

    friendly_name = "party achievement"


class GlobalAchievement(EncounterByName):
    """
    A lobal achievement from the game Gloomhaven
    """

    friendly_name = "global achievement"


class EncounterByNumber(Encounter):
    """
    An encouter identified with a unique number from the game Gloomhaven
    Abstract class to capture mostly scenarios and events
    """

    # should be overwritten by child classes
    friendly_name = "encounter by number"

    def __init__(self, identifier: int = None, unlockables: list = [], fullJSON: str = None):
        """
        identifier (int):
            the identifier of the Encounter
        unlockables (list of Encounter):
            list of Encounter objects this Encounter unlocked
        fullJSON (str):
            JSON representation of the Encounter

        Provide either a JSON or all other parameters as input.
        The JSON will override any other input if set.
        """

        # enforce only abstract use of this class
        assert type(self) != EncounterByNumber

        super().__init__(
            identifier=identifier,
            unlockables=unlockables,
            fullJSON=fullJSON
        )

        assert type(self.identifier) == int

    def __str__(self) -> str:
        """
        Returns general info about the encouter (str)
        """

        super_str = super().__str__()

        return f"{super_str}."


class Treasure(EncounterByNumber):
    """
    An abstract class for treasure from the game Gloomhaven
    """

    friendly_name = "treasure"


class IncrementalEncounterByNumber(EncounterByNumber):
    """
    An abstract class for incremental encounters from the game Gloomhaven
    Incremental encounters are encounters which identifier is the identifier of
    the previous encounter of the same type increased by one
    """

    # should be overwritten by child classes
    friendly_name = "Incremental encounter"


class Donation(IncrementalEncounterByNumber):
    """
    A sanctuary donation from the game Gloomhaven
    """

    friendly_name = "donation"


class AncientTechnology(IncrementalEncounterByNumber):
    """
    An ancient technology from the game Gloomhaven
    """

    friendly_name = "ancient technology"


class Event(EncounterByNumber):
    """
    An abstract class for events from the game Gloomhaven
    """

    # should be overwritten by child classes
    friendly_name = "event"

    def __init__(
        self,
        identifier: int = None,
        choice: str = None,
        remove: bool = False,
        unlockables: list = [],
        fullJSON: int = None
    ):
        """
        identifier (int):
            the identifier of the event
        choice ("A", "B" or ""):
            "A" or "B" for outcome choice, "" if only unlocked
        remove (bool):
            should the event be removed from available events
        unlockables (list of Encounter):
            list of Encounter objects this Encounter unlocked
        """

        assert type(self) != Event

        if fullJSON is not None:
            fullDict = self.fromJSON(fullJSON)
            identifier = fullDict["identifier"]
            choice = fullDict["choice"]
            remove = fullDict["remove"]
            unlockables = fullDict["unlockables"]

        assert choice == "A" or choice == "B" or choice == ""
        assert type(remove) == bool

        super().__init__(identifier, unlockables)

        self.choice = choice
        self.remove = remove

    def __str__(self) -> str:
        """
        Returns general info about the event
        """

        super_str = super().__str__()

        if self.choice:
            str_end = f": {self.choice}"
            if self.remove:
                str_end += "-"
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


class NamedEncounterByNumber(EncounterByNumber):
    """
    An abstract class for encounters with a name from the game Gloomhaven
    """

    # should be overwritten by child classes
    friendly_name = "named encounter"

    def __init__(
        self,
        identifier: int = None,
        name: str = None,
        unlockables: list = [],
        fullJSON: str = None
    ):
        """
        identifier (int):
            the identifier of the named encounter
        name (string):
            the name of the named encounter
        unlockables (list of Encounter):
            list of Encounter objects this Encounter unlocked

        Provide either a JSON or all other parameters as input.
        The JSON will override any other input if set.
        """

        if fullJSON is not None:
            fullDict = self.fromJSON(fullJSON)
            identifier = fullDict["identifier"]
            name = fullDict["name"]
            unlockables = fullDict["unlockables"]

        assert type(name) == str

        super().__init__(identifier, unlockables)

        self.name = name

    def __str__(self) -> str:
        """
        Returns general info about the named encounter
        """

        super_str = super().__str__()

        return f"{super_str} {self.name}"


class Quest(NamedEncounterByNumber):
    """
    A personal quest from the game Gloomhaven
    """

    friendly_name = "quest"


class ItemDesign(NamedEncounterByNumber):
    """
    An item design from the game Gloomhaven
    """

    friendly_name = "item design"


class Scenario(NamedEncounterByNumber):
    """
    A scenario from the game Gloomhaven
    """

    friendly_name = "scenario"

    def __init__(
        self,
        identifier: int = None,
        name: str = None,
        gridLocation: GridLocation = None,
        succes=None,
        unlockables: list = [],
        fullJSON: str = None
    ):
        """
        identifier (int):
            the identifier of the Scenario
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
            identifier = fullDict["identifier"]
            name = fullDict["name"]
            gridLocation = GridLocation(
                fullJSON=json.dumps(fullDict["gridLocation"])
            )
            succes = fullDict["succes"]
            unlockables = fullDict["unlockables"]

        assert type(gridLocation) == GridLocation
        assert type(succes) == bool or succes == ""

        super().__init__(identifier, name, unlockables)

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


if __name__ == "__main__":
    print("script contains only object definitions, no functional code on its own")
