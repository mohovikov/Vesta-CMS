from app.config import Config
from app.helpers.console import printColored
from app.constants.bcolors import Bcolors

def print_server_start_header(ascii_art: bool = True) -> None:
    if ascii_art:
        printColored(r"  _   ___________________     _______  _______", Bcolors.GREEN)
        printColored(r" | | / / __/ __/_  __/ _ |   / ___/  |/  / __/", Bcolors.GREEN)
        printColored(r" | |/ / _/_\ \  / / / __ |  / /__/ /|_/ /\ \  ", Bcolors.GREEN)
        printColored(r" |___/___/___/ /_/ /_/ |_|  \___/_/  /_/___/  ", Bcolors.GREEN)
        print("\n")
    printColored(f"> Welcome to {Config.APP_NAME} v{Config.APP_VERSION}", Bcolors.GREEN)
    printColored(f"> Made by MOHOVICK(mohovikov)", Bcolors.GREEN)
    printColored("{}> https://github.com/mohovikov/Vesta-CMS".format(Bcolors.UNDERLINE), Bcolors.GREEN)
    printColored(f"> Press CTRL+C to exit\n", Bcolors.GREEN)