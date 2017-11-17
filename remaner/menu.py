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

import os
from docopt import docopt
import renamer


class Editor:
    def __init__(self):
        self.data = ()
        self.menu_map = {
            "1": self.preview,
            "2": self.change_position,
            "3": self.sort_files,
            "4": self.apply_rename,
            "5": self.input_new_data,
            "6": self.quit
        }

    def menu(self):
        try:
            print('''
\n!RemaneR\n
''')
            start = self.menu_map["5"]
            start()
            answer = ''
            while True:
                print("""
Enter a command:
\t 1\t-Preview changes
\t 2\t-Move a new name up or down in the list
\t 3\t-Sort files (ascending, descending)
\t 4\t-Apply changes
\t 5\t-Input new files directory or names file
\t 6\t-Quit
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
        files = []
        path = ''
        names = []
        while True:
            try:
                ask_path = input('Enter path to the folder containing'
                                 'your files to be renamed: ')
                check_files = renamer.InputCheckExtract().files_to_rename(
                                                                       ask_path)
            except renamer.PathDoesNotExistError:
                print('\n--That path does not seem to exist!--\n')
            except renamer.DirectoryNotFoundError:
                print('\n--Directory not found!--\n')
            except renamer.EmptyDirectoryError:
                print('\n--This directory is empty!--\n')
            else:
                files = check_files
                path = os.path.abspath(ask_path)
                break
        while True:
            try:
                ask_names = input(
                    'Enter path to the file containing new file names: ')
                check_names = renamer.InputCheckExtract().names_file(ask_names)
            except renamer.PathDoesNotExistError:
                print("\n--This path does not seem to exist!--\n")
            except renamer.FileDoesNotExistError as e:
                print("\n--Can't find file {}!--\n".format(e.filename))
            except renamer.FileExtensionNotSupported:
                print("\n--This file extension is not supported!--\n")
            else:
                names = check_names
                break
        self.data = renamer.Renamer(files, names)
        self.data.path = path

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

    def sort_files(self):
        sort_method = ''
        while True:
            print('''
Choose an option:
\t 1\t-Ascending order
\t 2\t-Descending order
\t 3\t-Leave it as is
''')
            sort_method = input("Enter a command number: ")
            try:
                self.data.sort_files(sort_method)
            except renamer.NotAValidOption:
                print('{} is not a valid option'.format(sort_method))
            else:
                break

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
