from gloommodel import Scenario, GridLocation, CityEvent, RoadEvent
import json


def error_exit_interfaces():
    """
    Something really strange happened...
    """

    # for just shut down
    # implement passing error to Controller at some point
    # maybe it can still handle it...

    print('Sorry, GloomLog could not parse that input')
    print('GloomLog has to shut down :(')
    exit()


class UserInterface:

    # should be overriden in child classes
    interface_header = ""

    encounter_types = (
        Scenario,
        RoadEvent,
        CityEvent
    )

    def __init__(self):
        # enfore abstract class
        assert type(self) != UserInterface

        # should be extended in child classes
        self.user_option_dict = {}
        self.update_user_option_dict(
            option_key="help",
            option_function=self.print_help,
            option_print="Show HELP"
        )
        self.update_user_option_dict(
            option_key="exit",
            option_function=self.exit_gloomlog,
            option_print="EXIT GloomLog"
        )

    def update_user_option_dict(
        self,
        option_key: str,
        option_function: callable,
        option_print: str
    ):
        """
        Add an entry to the user options in an interface
        according to the standard
        """
        assert isinstance(option_key, str)
        assert callable(option_function)
        assert isinstance(option_print, str)

        self.user_option_dict[option_key] = {
            "function": option_function,
            "print": option_print
        }

    def scale_interface(self):
        """
        For readability a line of ='s and -'s
        is added around parts of the interface.
        The length of this line should align with
        the longest string in the interface.
        """
        self.user_option_tuple = tuple(
            option for option in self.user_option_dict
        )

        self.interface_top = ""
        self.interface_bottom = ""

        max_len = max(
            len(self.interface_header),
            len(
                self.tuple_to_pretty_string(
                    input_tuple=self.user_option_tuple
                ) + ":"
            )
        )

        for _ in range(max_len):
            self.interface_top += "="
            self.interface_bottom += "-"

    def present_interface(self):
        """
        Print a user interface and
        return what the user selected there.
        """

        self.scale_interface()

        print('')
        print(self.interface_top)
        print(self.interface_header)
        print(self.interface_top)

        for option in self.user_option_dict:
            print(self.user_option_dict[option]["print"])
        print(self.interface_bottom)

        print('Please choose from')
        user_input = UserInterface.multiple_choice_question(
            options=self.user_option_tuple)

        try:
            assert user_input in self.user_option_dict
        except KeyError:
            print("Unavailable option selected")
            error_exit_interfaces()

        print(self.interface_bottom)

        return self.user_option_dict[user_input]["function"]()

    @staticmethod
    def print_help() -> True:
        """
        Print GloomLog's help text
        """

        print(':, only literal options')
        print('#, literal options + numbered positions')
        print('@, literal options + one character shorthands')
        print('>, literals + numbers + shorthands')

        return True

    @staticmethod
    def exit_gloomlog() -> False:
        """
        Breaks are not allowwed outside of a loop :(
        Exceptions and generators would be overkill
        So use the flag 'stay' in every userOptionDict
        and this simple function instead
        """

        return False

    @staticmethod
    def close_interface() -> 2:

        return 2

    @staticmethod
    def tuple_to_pretty_string(input_tuple: tuple) -> str:
        """
        Remove a trailing comma from strings
        of single entry tuples.
        """
        assert isinstance(input_tuple, tuple)

        if len(input_tuple) > 1:
            return str(input_tuple)
        else:
            return "(" + str(input_tuple[0]) + ")"

    @staticmethod
    def multiple_choice_question(
        options: tuple,
        question: str = "",
        range_options: str = None
    ) -> str:
        """
        question (str):
            the question to the user
        options (tuple of unique strings):
            the options the question allows the user to choose from
        rangeOptions(str):
            overrides autogenerations of options shown in question

        Keeps asking the user until a valid option is inputted.

        User can input a literal option.
        User can input the number of an option in options,
            if the first character of no option contains a number.
        User can input the first character of an option in options,
            if all first characters in options are unique.

        After the question comes a signal that the user may input:
        :, only literal options
        # , literal options + numbered positions
        @, literal options + one character shorthands
        >, literals + numbers + shorthands

        Returns the option from options chosen by the user (str)
        """

        assert isinstance(question, str)
        assert isinstance(options, tuple)
        assert options

        for i in options:
            assert isinstance(i, str)

        # assert that options are unique
        assert len({i: True for i in options}) == len(options)

        if range_options is None:
            range_options = UserInterface.tuple_to_pretty_string(
                input_tuple=options
            )
        else:
            assert isinstance(range_options, str)

        # if first characters of options contain no digits,
        # allow for numbered selection
        for i in options:
            if i[0].isdigit():
                contains_digits = True
                break
        else:
            contains_digits = False

        # if first characters in options are unique,
        # allow for shorthand selection
        fast_dict = {i[0]: i for i in options}
        if len(fast_dict) != len(options):
            fast_dict = {}
            if contains_digits:
                range_options += ": "
            else:
                range_options += "# "
        else:
            if contains_digits:
                range_options += "@ "
            else:
                range_options += "> "

        if len(question) > 0:
            range_options = " " + range_options

        while True:
            user_input = input(question + range_options)
            if user_input in options:
                return user_input
            else:
                if user_input in fast_dict:
                    return fast_dict[user_input]
                if not contains_digits:
                    try:
                        user_input = int(user_input)
                        assert user_input > 0
                    except BaseException:
                        print("Invalid input")
                    else:
                        user_input -= 1
                        if user_input < len(options):
                            return options[user_input]
                        else:
                            print("Inputted number out of option bounds")
                else:
                    print("Invalid input")

    @staticmethod
    def yes_no_question(question: str = "") -> bool:
        """
        question (str):
            the question to the user

        Keeps asking the user until 'yes', 'no', '1' or '2' is inputted
        '1' = 'yes'
        '2' = 'no'

        Returns whether the user chose 'yes' (bool)
        """

        assert isinstance(question, str)

        return UserInterface.multiple_choice_question(options=("yes", "no"), question=question) == "yes"


class UserInterfaceMain(UserInterface):

    interface_header = "What would you like to do?"

    def __init__(self, list_saves: list):

        super().__init__()

        assert isinstance(list_saves, list)
        for save in list_saves:
            assert isinstance(save, str)

        self.list_saves = list_saves
        self.save_interface = None

        self.update_user_option_dict(
            option_key="new",
            option_function=self.new_campaign_save,
            option_print="Create NEW campaign save file"
        )

        if self.list_saves:
            self.update_user_option_dict(
                option_key="load",
                option_function=self.load_campaign_save,
                option_print="LOAD a campaign save file"
            )
            # implement delete, copy, rename and restore here at some point

    def present_interface(self) -> object:
        """
        Coordinates data flow in the interface based on user input
        """
        # TODO: refactor to a single return type
        if self.save_interface is None:
            return super().present_interface()
        else:
            # TODO remove code duplication (from gloomcontroller) if possible
            hold = True

            while hold:
                hold = self.save_interface.present_interface()
                if hold == 2:
                    self.save_interface = None
                    return True
                if type(hold) == tuple:
                    return hold

            return hold

    def new_campaign_save(self) -> object:
        """
        Create a new campagin save file.

        listSaves (list of str): list of save files already present
        """

        if self.list_saves:
            print("The following campaign save names are already taken:")
            print(self.tuple_to_pretty_string(
                tuple(i for i in self.list_saves)))

        while True:
            print("Campaign save names will be converted to lower case.")
            save_file = input(
                "How would you like to call your campaign save file?: ").lower()
            if save_file in self.list_saves:
                print("Save already exists.")
            else:
                break

        self.save_interface = UserInterfaceSave(
            save_file_name=save_file,
            encounter_list=[CityEvent(number=0)]
        )

        return self.save_interface.get_save_data()

    def load_campaign_save(self) -> str:
        """
        Load a saved campaign file
        """

        print("Which save would you like to load?")

        save_file = self.multiple_choice_question(
            options=tuple(self.list_saves)
        )

        return save_file

    def prepare_save_interface(self, save_file: str, save_text: str):
        """
        Load save information into a save interface
        """
        assert isinstance(save_file, str)
        assert isinstance(save_text, str)

        try:
            save_dict = json.loads(save_text)
            encounter_list = []
            for encounter_as_dict in save_dict["EnounterList"]:
                for encounter_type in self.encounter_types:
                    if encounter_type.__name__ == encounter_as_dict["type"]:
                        encounter_list.append(
                            encounter_type(
                                fullJSON=json.dumps(encounter_as_dict)
                            )
                        )
                        break
                else:
                    raise TypeError
        except BaseException:
            print("Invalid save file :(")
            error_exit_interfaces()

        self.save_interface = UserInterfaceSave(
            save_file_name=save_file,
            encounter_list=encounter_list
        )


class UserInterfaceSave(UserInterface):

    interface_header = "What would you like to do with the campaign save?"

    def __init__(self, save_file_name: str, encounter_list: list):

        super().__init__()

        assert isinstance(save_file_name, str)
        assert isinstance(encounter_list, list)
        for encounter in encounter_list:
            assert type(encounter) in self.encounter_types

        self.update_user_option_dict(
            option_key="add",
            option_function=self.add_encounter_to_save,
            # TODO
            option_print="ADD new encounter (implemented as replace for now)"
        )
        self.update_user_option_dict(
            option_key="close",
            option_function=self.close_interface,
            option_print="CLOSE save and go back to main interface"
        )

        # implement here at some point:
        # SAVE progress
        # REMOVE encounters from save file
        # EDIT encounter properties
        # DELETE this save
        # Inspect BACKUP save file -> Maybe advanced interface
        # Try to FIX broken save file -> Maybe advanced interface

        # self.save_file_name is slightly redundant for now,
        # but will be usefull with renaming saves
        self.save_file_name = save_file_name
        self.encounter_list = encounter_list

    def present_interface(self) -> object:
        """
        Present the save interface
        """

        print("")

        if self.encounter_list:
            print("Your last encounter was:")
            print(self.encounter_list[-1])
        else:
            print("Your campaign save does not yet contain any encounters.")

        return super().present_interface()

    def add_encounter_to_save(self):
        """
        Get the necessary data to add an encounter to the save file
        from the user's input.
        """

        new_encounter_friendly_name = self.multiple_choice_question(
            question="What type was your last encounter?",
            options=tuple(encounter_type.friendly_name
                          for encounter_type in self.encounter_types)
        )

        for new_encounter_class in self.encounter_types:
            if new_encounter_class.friendly_name == new_encounter_friendly_name:
                break
        else:
            print("Undefined class obtained")
            error_exit_interfaces()

        new_encounter_info = []

        # get encounter number
        new_encounter_info.append(
            int(
                self.multiple_choice_question(
                    question="What is the number of the {encounter} you did?".format(
                        encounter=new_encounter_friendly_name),
                    options=tuple(str(i) for i in range(1, 101)),
                    range_options="(1-100)"
                )
            )
        )

        if new_encounter_class == Scenario:
            # get scenario name
            new_encounter_info.append(
                input("What is the name of the scenario you did?: "))
            # get/create scenario gridLocation
            new_encounter_info.append(
                GridLocation(
                    self.multiple_choice_question(
                        question="What is the character of that scenario's location?",
                        # TODO: refactor to single defenition
                        options=tuple(chr(i) for i in range(65, 80)),
                        range_options="(A-O)"
                    ),
                    int(
                        self.multiple_choice_question(
                            question="What is the number of that scenario's location?",
                            # TODO: refactor to single defenition
                            options=tuple(str(i) for i in range(1, 19)),
                            range_options="(1-18)")
                    )
                )
            )

        new_encounter = new_encounter_class(*new_encounter_info)
        self.encounter_list.append(new_encounter)

        return self.get_save_data()

    def get_save_data(self):
        """
        Convert a list of Encounters to saveable text.
        """
        try:
            save_info = json.dumps(
                {"EnounterList": [json.loads(self.encounter_list[-1].toJSON()), ]}, indent=2)
        except BaseException:
            print("Invalid encounters created :(")
            error_exit_interfaces()

        return (self.save_file_name, save_info)
