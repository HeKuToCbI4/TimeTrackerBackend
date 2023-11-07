import re


class WindowTitlePreprocessor(object):
    """
    Basically checks for some conditions and does some stuff.
    WIP to be extended.
    Maybe make it configurable from some file?
    """

    def __init__(self):
        pass

    @staticmethod
    def process_title(executable: str, title: str) -> str:
        if executable.lower() == "telegram.exe":
            found = re.findall(
                r"(\(\d+\))?\s?([\w\s,|\\/()\[\].!@#$%^&*]+)(.\s\(\d+\))?", title
            )
            if not found:
                return title.strip()
            if len(found) == 1:
                return found[0][1]
            else:
                print("We're fucked!")
        if "youtube" in title.lower():
            found = re.findall(
                r"(\(\d+\))?\s+?(.+)", title
            )
            if not found:
                return title.strip()
            if len(found) == 1:
                return found[0][1]
            else:
                print("We're fucked!")
        return title
