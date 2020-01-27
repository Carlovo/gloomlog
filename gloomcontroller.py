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

        self.backend = Backend()
        saves_copy = self.backend.list_saves.copy()
        self.interface = UserInterfaceMain(list_saves=saves_copy)

        self.present_user_interface_main()

    def present_user_interface_main(self):

        hold = True

        while hold:
            hold = self.interface.present_interface()
            if type(hold) == tuple:
                self.backend.save_to_file(save_file=hold[0], save_info=hold[1])

        self.exit_gloomlog()

    @staticmethod
    def exit_gloomlog():
        """
        Gracefully exits GloomLog
        """

        print('Bye!')
        exit()

    @staticmethod
    def load_campaign_save():

        pass
