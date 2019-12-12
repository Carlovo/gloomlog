class Encounter(object):
    """
    An encouter from the game Gloomhaven
    Abstract class to capture scenarios and events
    """

    def __init__(self, number, name):
        """
        number (int):
            the number of the encouter
        name (string):
            the name of the encouter
        """

        assert type(self) != Encounter

        assert type(number) == int
        assert type(name) == str

        self.number = number
        self.name = name
    

    def getNumber(self):
        """
        Returns the number of the encouter (int)
        """

        return self.number


    def getName(self):
        """
        Returns the name of the encouter (string)
        """

        return self.name
    

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

        return str(self.number) + ". " + self.name



class GridLocation(object):
    """
    A location by the grid on the map of Gloomhaven
    """

    def __init__(self, character, number):
        """
        character (single character string: A - O):
            the character denoting the horizontal / row value of the location
        number (int: 1 - 18):
            the number denoting the vertical / column value of the location
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
        Returns the character denoting the horizontal / row value of the location.
        (single character string: a - o)
        """

        return self.character


    def getNumber(self):
        """
        Returns the number denoting the vertical / column value of the location.
        (int: 1 - 18)
        """

        return self.number

    
    def __eq__(self, other):
        """
        other (GridLocation):
            the grid location to compare to
        Return whether the two grid location point to a similar location on the map of Gloomhaven
        (bool)
        """

        assert type(other) == type(self)

        return self.character == other.character and self.number == other.number
    

    def __str__(self):
        """
        Returns general info about the grid location
        """

        return "(" + self.character + "-" + str(self.number) + ")"



class Scenario(Encounter):
    """
    A scenario from the game Gloomhaven
    """

    def __init__(self, number, name, gridLocation):
        """
        number (int):
            the number of the scenario
        name (string):
            the name of the scenario
        gridLocation (GridLocation):
            the grid location of the scenario on the map of Gloomhaven
        """

        assert type(gridLocation) == GridLocation

        super().__init__(number, name)

        self.gridLocation = gridLocation


    def getGridLocation(self):
        """
        Returns GridLocation of the scenario on the map
        """

        return self.gridLocation


    def __str__(self):
        """
        Returns general info about the scenario
        """

        return super().__str__() + " " + self.gridLocation.__str__()



class Event(Encounter):
    """
    A abstract class for events from the game Gloomhaven
    """

    def __init__(self, number, name):
        """
        number (int):
            the number of the event
        name (string):
            the name of the event
        """

        assert type(self) != Event

        super().__init__(number, name)


    def __str__(self):
        """
        Returns general info about the event
        """

        return "Event: " + super().__str__()



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
