class encounter(object):
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

        self.number = number
        self.name = name
    

    def get_number(self):
        """
        Returns the number of the encouter (int)
        """

        return self.number


    def get_name(self):
        """
        Returns the name of the encouter (string)
        """

        return self.name

    
    def print_info(self):
        """
        Prints the general info about the encouter
        """

        print(str(self.number) + ". " + self.name)



class scenario(encounter):
    """
    A scenario from the game Gloomhaven
    """
    def __init__(self, number, name, location):
        """
        number (int):
            the number of the scenario
        name (string):
            the name of the scenario
        location (tuple of a character and a number):
            location of the scenario on the map
        """

        super().__init__(number, name)
        self.location = location


    def get_location(self):
        """
        Returns location of the scenario on the map (tuple of a character and a number)
        """

        copy_location = self.location
        return copy_location


    def print_info(self):
        """
        Prints the general info about the encouter
        """

        super().print_info()
        print("Location: (" + self.location[0] + "-" + str(self.location[1]) + ")")



def get_encounter():
    """
    Prompts the user to input information about its encounters in Gloomhaven
    """

    number = input("Enter an encounter number (int): ")
    name = input("Enter an encounter name (string): ")

    return encounter(number, name)


def get_scenario():
    """
    Prompts the user to input information about its scenarios in Gloomhaven
    """

    number = input("Enter a scenario number (int): ")
    name = input("Enter a scenario name (string): ")
    location_char = input("Enter a scenario character coordinate (single character string): ")
    location_numb = input("Enter a scenario number coordinate (int): ")

    return scenario(number, name, (location_char, location_numb))


def print_log(encounter):
    """
    Print the general info of the encouters the user had in Gloomhaven
    """

    encounter.print_info()


# nctr = get_encounter()
# print_log(nctr)

scen = get_scenario()
print_log(scen)
