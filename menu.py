import renamer


class Editor:
    def __init__(self):
        self.menu_map = {
            "input new data": self.input_data,
            "preview": self.preview,
            "change position": self.change_position,
            "apply rename": self.apply_rename,
            "quit": self.quit
        }

    def menu(self):
        try:
            start = self.menu_map["input new data"]
        except:
            pass
        else:
            try:
                answer = ''
                while True:
                    print("""
Enter a command:
\t 1\t-Preview changes
\t 2\t-Move a new name up or down in the list
\t 3\t-Apply changes
\t 4\t-Input new files directory or names file
\t 5\t-Quit
""")
                    answer = input("enter a command number: ")
                    try:
                        func = self.menu[answer]
                    except KeyError:
                        print("{} is not a valid option".format(answer))
                    else:
                        func()
            finally:
                print('*')

    def input_new_data(self):
        pass

    def preview(self):
        pass

    def change_position(self):
        pass

    def apply_rename(self):
        pass

    def quit(self):
        raise SystemExit()
