from tempfile import NamedTemporaryFile
from os import remove as remove_file
from os.path import exists as path_exists


class IsisFile:
    def __init__(self):
        self.input_target = NamedTemporaryFile(delete=False)
        self.output_target = NamedTemporaryFile(delete=False)

    def cleanup(self):
        IsisFile._delete_if_exists(self.input_target.name)
        IsisFile._delete_if_exists(self.output_target.name)

    @staticmethod
    def _delete_if_exists(file_path: str):
        if path_exists(file_path):
            remove_file(file_path)
