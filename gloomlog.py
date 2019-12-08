class scenario(object):
    """
    A scenario from the game Gloomhaven
    """
    def __init__(self, id, location, name):
        """
        id (int):
            the number of the scenario
        location (tuple of a character and a number):
            location of the scenario on the map
        name (string):
            the name of the scenario
        """

        self.id = id
        self.location = location
        self.name = name
    

    def get_id(self):
        """
        Returns the number of the scenario (int)
        """

        return self.id


    def get_location(self):
        """
        Returns location of the scenario on the map (tuple of a character and a number)
        """

        copy_location = self.location
        return copy_location


    def get_name(self):
        """
        Returns the name of the scenario (string)
        """

        return self.name

    
    def print_info(self):
        """
        Prints the general info about the scenario
        """

        print(self.id + ". " + self.name + " (" + self.location[0] + "-" + self.location[1] + ")")


def get_log():
    """
    Prompts the user to input information about its encounters in Gloomhaven
    """

    id = input("Enter a scenario id (int): ")
    location_char = input("Enter a scenario character coordinate (single character string): ")
    location_numb = input("Enter a scenario number coordinate (int): ")
    name = input("Enter a scenario name (string): ")

    return scenario(id, (location_char, location_numb), name)


def print_log(encounter):
    """
    Print the general info of the encouters the user had in Gloomhaven
    """

    encounter.print_info()

encounter = get_log()
print_log(encounter)
