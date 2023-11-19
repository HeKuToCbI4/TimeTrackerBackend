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
        if executable is None:
            return title
        if executable.lower() == "telegram.exe":
            found_start = re.findall(r"^(\(\d+\))+", title)
            print(f"{found_start=}")
            if len(found_start) == 1:
                title = title.replace(found_start[0], "")
            found_end = re.findall(r"(\s.\s\(\d+\))+$", title)
            print(f"{found_end=}")
            if len(found_end) == 1:
                title = title.replace(found_end[0], "")
            found_end_2 = re.findall(r"(\(\d+\))+$", title)
            print(f"{found_end_2=}")
            if len(found_end_2) == 1:
                title = title.replace(found_end_2[0], "")
            return title.strip()

        if "youtube" in title.lower():
            found = re.findall(r"(\(\d+\))?\s+?(.+)", title)
            if not found:
                return title.strip()
            if len(found) == 1:
                return found[0][1]
            else:
                print("We're fucked!")
        return title
