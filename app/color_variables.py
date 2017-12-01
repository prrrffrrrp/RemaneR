from colorama import init, Fore


# colorama boilerplate
init(autoreset=True)

# colorama variables
magenta = Fore.MAGENTA
cyan = Fore.CYAN
end_fore = Fore.RESET


def draw_command_arrow():
    print(Fore.MAGENTA + '--> ', end=' ')
