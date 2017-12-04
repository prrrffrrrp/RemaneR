import os
import app.renamer as renamer
from .color_variables import cyan, magenta, draw_command_arrow, end_fore


class Editor:
    '''
    Class Editor contains the interactive cli interface.
    Its methods often just trigger the Renamer class methods
    but also handle all the exceptions.
    '''
    def __init__(self):
        self.data = ()
        self.menu_map = {
            "1": self.preview,
            "2": self.change_position,
            "3": self.add_suffix_menu,
            "4": self.sort_files,
            "5": self.apply_rename,
            "6": self.input_new_data,
            "7": self.quit
        }

    def menu(self):
        '''
        Shows the main menu options until the program is stopped.
        '''
        try:
            print(cyan + '''
\n\t!RemaneR\n
''')
            start = self.menu_map["6"]
            start()
            answer = ''
            while True:
                print(cyan + """
Menu options:
\t""" + magenta + ' 1 ' + end_fore + """-Preview changes
\t""" + magenta + ' 2 ' + end_fore + """-Move a new name up or down in the list
\t""" + magenta + ' 3 ' + end_fore + """-Add a suffix to new names
\t""" + magenta + ' 4 ' + end_fore + """-Sort files (ascending, descending)
\t""" + magenta + ' 5 ' + end_fore + """-Rename
\t""" + magenta + ' 6 ' + end_fore + """-Input new files directory or names file
\t""" + magenta + ' 7 ' + end_fore + """-Quit
""")
                draw_command_arrow()
                answer = input("Enter a command number: ")
                try:
                    func = self.menu_map[answer]
                except KeyError:
                    print(magenta +
                          "\n-- {} is not a valid option--".format(answer))
                else:
                    func()
        finally:
            print(cyan + '\n\tThanks for using !RemaneR\n')

    def input_new_data(self):
        '''
        Asks for the paths leading to the files to be renamed and to the file
        containing the new names.
        Then checks for validity, extracts the data and creates a Renamer
        object.
        '''
        files = []
        path = ''
        names = []
        while True:
            try:
                draw_command_arrow()
                ask_path = input('Enter path to the folder containing '
                                 'your files to be renamed: ')
                check_files = renamer.InputCheckExtract().files_to_rename(
                                                                       ask_path)
            except renamer.PathDoesNotExistError:
                print(magenta + '\n--That path does not seem to exist!--\n')
            except renamer.DirectoryNotFoundError:
                print(magenta + '\n--Directory not found!--\n')
            except renamer.EmptyDirectoryError:
                print(magenta + '\n--This directory is empty!--\n')
            else:
                files = check_files
                path = os.path.abspath(ask_path)
                break
        while True:
            try:
                draw_command_arrow()
                ask_names = input(
                    'Enter path to the file containing new file names: ')
                check_names = renamer.InputCheckExtract().names_file(ask_names)
            except renamer.PathDoesNotExistError:
                print(magenta + "\n--This path does not seem to exist!--\n")
            except renamer.FileDoesNotExistError as e:
                print(magenta +
                      "\n--Can't find file {}!--\n".format(e.filename))
            except renamer.FileExtensionNotSupported:
                print(magenta + "\n--This file extension is not supported!--\n")
            except renamer.DuplicateNamesError as e:
                print(magenta +
                      "\n--Name <{}> was found at least twice in the list"
                      "\nThis could lead to overriding files and loosing data"
                      "\nPlease make changes to avoid having duplicate names--"
                      .format(e.args[0]))
            else:
                names = check_names
                break
        self.data = renamer.Renamer(files, names)
        self.data.path = path

    def preview(self):
        '''
        Triggers the display method showing a preview of a list of
        files to be renamed side by side with the new names.
        '''
        self.data.display()

    def change_position(self):
        '''
        Allows changing the position of name items in the names list.
        The user needs to enter the original index number of the item
        and the index number of the new item's position in the names list.
        '''
        print()
        draw_command_arrow()
        now = input("Enter the origin index number: ")
        draw_command_arrow()
        then = input("Enter the destination index number: ")
        try:
            self.data.move(int(now), int(then))
        except renamer.IndexOutOfRangeError:
            print(magenta + '\n--Index out of range. Try again.--\n')
            func = self.menu_map['2']
            func()
        else:
            print(cyan + "\n--Name position changed--\n")

    def add_suffix_menu(self):
        '''
        Menu interface for the Renamer.add_suffix method.
        Allows adding a suffix to new names.
        '''
        draw_command_arrow()
        suffix = input("Enter a suffix: ")
        while True:
            print(cyan + """
Suffix addition modality:
\t""" + magenta + ' 1 ' + end_fore + """-All
\t""" + magenta + ' 2 ' + end_fore + """-Alternate. Suffixed before original
\t""" + magenta + ' 3 ' + end_fore + """-Alternate. Suffixed after original
\t""" + magenta + ' 4 ' + end_fore + """-Revert. Erase suffix
""")
            draw_command_arrow()
            mode = input("Enter a command number: ")
            try:
                self.data.add_suffix(suffix, mode)
            except renamer.NotAValidOption:
                print(magenta +
                      '\n-- {} is not a valid option--'.format(mode))
            except renamer.RevertSuffix:
                print(cyan + "\n--Suffixes deleted from names--\n")
                break
            else:
                print(cyan + "\n--Suffix added to new names!--\n")
                break

    def sort_files(self):
        '''
        Allows sorting the list of files to be renamed.
        The default is alphabetical order.
        '''
        sort_method = ''
        while True:
            print(cyan + """
Sort files method:
\t""" + magenta + ' 1 ' + end_fore + """-Alphabetical ascending order
\t""" + magenta + ' 2 ' + end_fore + """-Alphabetical descending order
\t""" + magenta + ' 3 ' + end_fore + """-ASCII ascending order
\t""" + magenta + ' 4 ' + end_fore + """-ASCII descending order
""")
            draw_command_arrow()
            sort_method = input("Enter a command number: ")
            try:
                self.data.sort_files(sort_method)
            except renamer.NotAValidOption:
                print(magenta +
                      '\n-- {} is not a valid option--'.format(sort_method))
            else:
                print(cyan + "\n--Files sorted!--\n")
                break

    def apply_rename(self):
        '''
        Changes the name of the files.
        '''
        self.data.rename()
        print(cyan + '\n--Files successfully renamed!--\n')
        self.quit()

    def quit(self):
        '''
        Exits the program.
        '''
        raise SystemExit()
