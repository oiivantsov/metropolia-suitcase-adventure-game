from colorama import Fore, Back, Style

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


MENU_COLOR = color.PURPLE
LINE = "------------------------------------------------------------------------------------------------------------------------------------------------------------"

def printBanner():
    print(Style.RESET_ALL+"       "+Back.YELLOW+Fore.BLACK+Style.BRIGHT+"[[__]]"+Style.RESET_ALL+"                  " + Back.LIGHTGREEN_EX + Fore.BLACK +Style.BRIGHT+ "  WELCOME TO \"SUITCASE ADVENTURE\"!  " + Back.RESET + Fore.RESET + "                   "+Back.BLUE + Fore.BLACK +"           "+Back.WHITE+"/ |"+Back.BLUE+"                      "+Back.LIGHTWHITE_EX+"( `   )"+ Back.BLUE+"")
    print(Style.RESET_ALL+"   "+Back.YELLOW+Fore.BLACK+Style.BRIGHT+";-----------.|"+Style.RESET_ALL+"          " + Fore.LIGHTGREEN_EX + "  Your are a lost suitcase in a major airport.  " + Back.RESET + Fore.RESET + "           "+Back.BLUE + Fore.BLACK +"          "+Back.WHITE+"|  |"+Back.BLUE+"                    "+Back.LIGHTWHITE_EX+"(    )    `)"+ Back.BLUE+"                  "+Back.LIGHTWHITE_EX+"(  )"+ Back.BLUE+"")
    print(Style.RESET_ALL+"   "+Back.YELLOW+Fore.BLACK+Style.BRIGHT+"|           ||"+Style.RESET_ALL+"     " + Fore.LIGHTGREEN_EX + "  Your mission: find your owner with the least flights.  " + Back.RESET + Fore.RESET + "       "+Back.BLUE + Fore.BLACK +"      "+Back.WHITE+"|"+Back.BLUE+"   "+Back.WHITE+"|  |"+Back.BLUE+"    "+Back.WHITE+"/-|"+Back.BLUE+"          "+Back.LIGHTWHITE_EX+"(_   (_ .  _) _)"+ Back.BLUE+"              "+Back.LIGHTWHITE_EX+"( `  ) . )"+ Back.BLUE+"")
    print(Style.RESET_ALL+"   "+Back.YELLOW+Fore.BLACK+Style.BRIGHT+"|           ||"+Style.RESET_ALL+"       " + Fore.LIGHTGREEN_EX + "  Explore the world and make eco-conscious choices!  " + Style.RESET_ALL + "         "+Back.BLUE + Fore.BLACK +"      *"+Back.WHITE+"|__|  |____----"+Back.BLUE+"                                     "+Back.LIGHTWHITE_EX+"(_, _(  ,_)_)"+ Back.BLUE+"")
    print(Style.RESET_ALL+"   "+Back.YELLOW+Fore.BLACK+Style.BRIGHT+"|           ||"+Style.RESET_ALL+"                                                                     "+Back.BLUE + Fore.BLACK +"      "+Back.WHITE+"|"+Back.BLUE+"   "+Back.WHITE+"|  |"+Back.BLUE+"    "+Back.WHITE+"\-|"+Back.BLUE+"")
    print(Style.RESET_ALL+"   "+Back.YELLOW+Fore.BLACK+Style.BRIGHT+"|___________|/"+Style.RESET_ALL+"         " + Fore.LIGHTBLUE_EX + "  Let's leave a positive impact on the planet!  " + Style.RESET_ALL + "            "+Back.BLUE + Fore.BLACK +"          "+Back.WHITE+"|  |"+Back.BLUE+"                             "+Back.LIGHTWHITE_EX+"(  _ )"+ Back.BLUE+"")
    print(Style.RESET_ALL+"                               " + Fore.WHITE + "  Made in Metropolia, Finland, 2024  " + Back.RESET + Fore.RESET + "                  "+Back.BLUE + Fore.BLACK +"           "+Back.WHITE+"\_|"+Back.BLUE+"                           "+Back.LIGHTWHITE_EX+"(_  _(_ ,)"+ Back.BLUE+"")
    print(Style.RESET_ALL+"")

rules = f"""
{Back.LIGHTGREEN_EX}{Fore.BLACK} GAME RULES {Style.RESET_ALL}{color.END}
{MENU_COLOR}{color.BOLD}Game aim{color.END}:
You're a lost suitcase. {color.UNDERLINE}{color.BOLD}Your task{color.END} is to find your owner in one of the largest airports in the world in a minimum number of flights. 
Choose the airport carefully – the fewer flights, the less emissions into the atmosphere!
{MENU_COLOR}{color.BOLD}Game start{color.END}:
To start the game, select {color.UNDERLINE}{color.BOLD}Login (2){color.END} in the main menu if you already have an account, or {color.UNDERLINE}{color.BOLD}Registration (3){color.END} to create an account. 
During logging, enter {color.CYAN}{color.BOLD}0{color.END} at any time if you want to return to the main menu.
{MENU_COLOR}{color.BOLD}Game play{color.END}:
To select an airport, follow the prompts of the game. {color.UNDERLINE}{color.BOLD}The distance{color.END} to the owner will tell you which continent, country or airport is better to choose.
To save your progress and go to the main menu, enter {color.CYAN}{color.BOLD}menu{color.END} at any time when choosing a direction.
{MENU_COLOR}{color.BOLD}Winning{color.END}:
The game ends if you guess the location of your owner. After that you can choose to start a new game, or return to the main menu.
{MENU_COLOR}{color.BOLD}Statistics{color.END}:
To compare your result with game average results of all players, select the {color.UNDERLINE}{color.BOLD}Statistics{color.END} option in the main menu.
{MENU_COLOR}{color.BOLD}Music{color.END}:
To turn off / turn on background music, choose {color.UNDERLINE}{color.BOLD}Background Music{color.END} option in the main menu, or enter {color.CYAN}{color.BOLD}music{color.END} at any time during the game.
{MENU_COLOR}{color.BOLD}Program exit{color.END}:
To close the program, select {color.UNDERLINE}{color.BOLD}Exit{color.END} from the main menu.
"""


def print_rules():
    print(rules)
    input("Press \033[94m[ENTER]\033[0m to continue...")  # cian color
