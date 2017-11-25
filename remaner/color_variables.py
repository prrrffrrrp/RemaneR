from colorama import init, Fore, Back, Style


# colorama boilerplate
init(autoreset=True)

# colorama variables
warning = Fore.LIGHTRED_EX
allgood = Fore.LIGHTGREEN_EX
display_1 = Fore.CYAN
display_2 = Fore.MAGENTA
end_fore = Fore.RESET
end_back = Back.RESET


def draw_command_arrow():
    print(Fore.MAGENTA + '--> ', end=' ')
