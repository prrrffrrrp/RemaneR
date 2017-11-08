'''
Usage: menu.py <path> <names> (-r)
       menu.py -i
       menu.py -h

Options:
    -h, --help           : show help page
    path                : path to files to be renamed
    names               : path to the file containing list of names
    -r, --rename        : apply rename operation
    -i, --interactive   : open menu with options
'''

from docopt import docopt
import renamer


class Editor:
    def __init__(self):
        self.data = ()
        self.menu_map = {
            "1": self.preview,
            "2": self.change_position,
            "3": self.apply_rename,
            "4": self.input_new_data,
            "5": self.quit
        }

    def menu(self):
        try:
            print('''
\n!RemaneR\n
''')
            start = self.menu_map["4"]
            start()
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
                answer = input("Enter a command number: ")
                try:
                    func = self.menu_map[answer]
                except KeyError:
                    print("{} is not a valid option".format(answer))
                else:
                    func()
        finally:
            print('*')

    def input_new_data(self):
        path = input(
            'Enter path to the folder containing your files to be renamed: ')
        names = input('Enter path to the file containing new file names: ')
        self.data = renamer.Renamer(path, names)

    def preview(self):
        self.data.display()

    def change_position(self):
        now = input("\nEnter the origin index number: ")
        then = input("Enter the destination index number: ")
        try:
            self.data.move(int(now), int(then))
        except renamer.IndexOutOfRangeError:
            print('\n', '#' * 10, ' Index out of range. Try again. ', '#' * 10)
            func = self.menu_map['2']
            func()

    def apply_rename(self):
        self.data.rename()
        print('\n', '#' * 10, ' Files renamed ', '#' * 10)

    def quit(self):
        print('\n', '#' * 10, 'Thanks for using !RemaneR', '#' * 10)
        raise SystemExit()


if __name__ == "__main__":
    args = docopt(__doc__)

    path = args['<path>']
    names = args['<names>']

    if args['--rename']:
        renamer.Renamer(path, names).rename()

    elif args['--interactive']:
        Editor().menu()
