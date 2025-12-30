from app.constants import Bcolors


def printColored(string: str, color: str):
    print("{}{}{}".format(color, string, Bcolors.ENDC))
