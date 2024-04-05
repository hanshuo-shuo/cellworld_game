import os


class Resources(object):
    @staticmethod
    def file(file_name: str) -> str:
        return os.path.join("files", file_name)
