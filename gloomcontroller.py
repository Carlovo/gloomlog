from gloombackend import Backend
from gloomview import UserInterfaceMain


def error_exit_gloomlog():
    """
    Something really strange happened...
    """

    print('Sorry, GloomLog lost controll')
    print('GloomLog has to shut down :(')
    exit()


class Controller:

    def __init__(self):
        self.backend = None
        self.interface = None

    def run(self):
        """
        Call this command to boot up GloomLog
        """

        self.backend = Backend()
        saves_copy = self.backend.check_saves()
        self.interface = UserInterfaceMain(list_saves=saves_copy)

        self.present_user_interface_main()

    def present_user_interface_main(self):
        """
        The main control function.
        Boots an interface.
        Coordinates data flow in the programm based on user input
        """

        hold = True

        while hold:
            hold = self.interface.present_interface()
            if type(hold) == tuple:
                self.backend.save_to_file(save_file=hold[0], save_info=hold[1])
                # slight overkill, but works well enough for a simple app as this
                self.interface.list_saves = self.backend.check_saves()
            if type(hold) == str:
                save_text = self.backend.load_save_file_as_text(save_file=hold)
                self.interface.prepare_save_interface(
                    save_file=hold,
                    save_text=save_text
                )

        self.exit_gloomlog()

    @staticmethod
    def exit_gloomlog():
        """
        Gracefully exits GloomLog
        """

        print('Bye!')
        exit()
