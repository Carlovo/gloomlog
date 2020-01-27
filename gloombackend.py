import os


class Backend:
    # this value is also in .gitignore, change it together with this one
    save_path = "__gloomsave__"
    save_extension = ".json.gml"
    backup_extension = ".prev"
    delete_extension = ".old"
    new_extension = ".new"

    def __init__(self):

        self.list_saves = self.check_saves()

    def check_saves(self) -> list:
        list_saves = []

        if os.path.exists(self.save_path):
            for save_file in os.listdir(self.save_path):
                if save_file.endswith(self.save_extension):
                    list_saves.append(
                        save_file.replace(self.save_extension, ""))

        return list_saves

    @staticmethod
    def write_new_text_file(file_name: str, file_text: str):
        """
        file_name (str): path name of the file to write
        file_text (str): text to write in the file

        Write a new text file to disk.
        """

        assert isinstance(file_name, str)
        assert isinstance(file_text, str)

        with open(file_name, "x") as file:
            file.write(file_text)

    def _backup_creation_(self, save_file: str):
        """
        This function should only be used by saveToFile.
        Use at your own risk.

        save_file (str): file name of the save file

        Sets the current save file to become a backup file.
        Sets the new save file to become the current save file.
        """

        assert isinstance(save_file, str)

        os.rename(save_file, save_file + self.backup_extension)
        os.rename(save_file + self.new_extension, save_file)

    def save_to_file(
        self,
        save_file: str,
        save_info: str,
        save_path: str = None,
        save_extension: str = None
    ):
        """
        save_path (str): relative path where to save the file
        save_file (str): base name of the save file to write
        save_info (str): save info to write in the file

        Saves text to a file.
        Also, checks if a directory for saving and backups exist,
        creates a directory and rotates saves and backups if present.
        """

        if save_path is None:
            save_path = self.save_path

        if save_extension is None:
            save_extension = self.save_extension

        assert isinstance(save_file, str)
        assert isinstance(save_info, str)
        assert isinstance(save_path, str)
        assert isinstance(save_extension, str)

        save_file = save_path + "/" + save_file + save_extension

        if os.path.exists(save_path):
            if os.path.exists(save_file):
                self.write_new_text_file(
                    file_name=save_file + self.new_extension,
                    file_text=save_info
                )
                if os.path.exists(save_file + self.backup_extension):
                    os.rename(
                        save_file + self.backup_extension,
                        save_file + self.delete_extension
                    )
                    self._backup_creation_(save_file=save_file)
                    os.remove(save_file + self.delete_extension)
                else:
                    self._backup_creation_(save_file=save_file)
                return
        else:
            os.mkdir(save_path)

        self.write_new_text_file(file_name=save_file, file_text=save_info)
