import json



class Encounter(object):
    """
    An encouter from the game Gloomhaven
    Abstract class to capture scenarios and events
    """

    def __init__(self, number):
        """
        number (int):
            the number of the encouter
        """

        assert type(self) != Encounter # enforce only abstract use of this class

        assert type(number) == int

        self.number = number
    

    def getNumber(self):
        """
        Returns the number of the encouter (int)
        """

        return self.number


    def toJSON(self):
        """
        Returns the JSON string representation of the information in the Encounter
        """

        nctrDict = {"number" : self.number}

        return json.dumps(nctrDict, indent=2)

    

    def __eq__(self, other):
        """
        Other (Encounter):
            the encounter to compare to
        Return whether the two encounters are the same
        (bool)
        """

        assert type(other) == type(self)

        return self.number == other.number


    def __str__(self):
        """
        Returns general info about the encouter
        """

        return str(self.number) + "."



class GridLocation(object):
    """
    A location by the grid on the map of Gloomhaven
    """

    def __init__(self, character, number):
        """
        character (single character string: A - O):
            the character denoting the horizontal / row value of the GridLocation
        number (int: 1 - 18):
            the number denoting the vertical / column value of the GridLocation
        """

        assert type(character) == str
        assert len(character) == 1

        assert 64 < ord(character) and ord(character) < 80

        assert type(number) == int
        assert 0 < number and number < 19

        self.character = character
        self.number = number

    
    def getCharacter(self):
        """
        Returns the character denoting the horizontal / row value of the GridLocation
        (single character string: a - o)
        """

        return self.character


    def getNumber(self):
        """
        Returns the number denoting the vertical / column value of the GridLocation
        (int: 1 - 18)
        """

        return self.number


    def toJSON(self):
        """
        Returns the JSON string representation of the information in the GridLocation
        """

        gridLocDict = {"character" : self.character, "number" : self.number}

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

    def __init__(self, number, name, gridLocation):
        """
        number (int):
            the number of the Scenario
        name (string):
            the name of the Scenario
        gridLocation (GridLocation):
            the grid location of the Scenario on the map of Gloomhaven
        """

        assert type(name) == str
        assert type(gridLocation) == GridLocation

        super().__init__(number)

        self.name = name
        self.gridLocation = gridLocation

    
    def getName(self):
        """
        Returns the name of the Scenario (string)
        """

        return self.name


    def getGridLocation(self):
        """
        Returns GridLocation of the Scenario on the map
        """

        return self.gridLocation
    

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

    def __init__(self, number):
        """
        number (int):
            the number of the event
        """

        assert type(self) != Event

        super().__init__(number)


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



def getEncounter():
    """
    Prompts the user to input information about its encounters in Gloomhaven
    """

    number = input("Enter an encounter number (int): ")
    name = input("Enter an encounter name (string): ")

    return Encounter(number, name)


def getScenario():
    """
    Prompts the user to input information about its scenarios in Gloomhaven
    """

    number = input("Enter a scenario number (int): ")
    name = input("Enter a scenario name (string): ")
    location_char = input("Enter a scenario character coordinate (single character string): ")
    location_numb = input("Enter a scenario number coordinate (int): ")

    location = GridLocation(location_char, location_numb)

    return Scenario(number, name, location)


# nctr = get_encounter()
# print_log(nctr)

# scen = getScenario()
# print(scen)


if __name__ == "__main__":
    print("programm not yet fully functional")

