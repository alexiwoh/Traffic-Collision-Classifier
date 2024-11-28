from constants import *


def print_title(title: str = ""):
    print(f"----{title:-^{TITLE_LENGTH}}----")  # Print title centered and padded.


def run_section(title: str = "", func=None):
    if not func:
        return

    # Print out section if there is a passed in function.
    print()
    print_title(title)  # Print title header.
    func()
    print_title(title)  # Print title footer.
    print()

