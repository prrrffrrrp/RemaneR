import os
import renamer
from .color_variables import allgood, warning, draw_command_arrow, display_1, \
     display_2, end_fore


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
            print(display_1 + '''
\n\t!RemaneR\n
''')
            start = self.menu_map["5"]
            start()
            answer = ''
            while True:
                print(display_1 + """
Menu options:
\t""" + display_2 + ' 1 ' + end_fore + """-Preview changes
\t""" + display_2 + ' 2 ' + end_fore + """-Move a new name up or down in the list
\t""" + display_2 + ' 3 ' + end_fore + """-Sort files (ascending, descending)
\t""" + display_2 + ' 4 ' + end_fore + """-Apply changes
\t""" + display_2 + ' 5 ' + end_fore + """-Input new files directory or names file
\t""" + display_2 + ' 6 ' + end_fore + """-Quit
""")
                draw_command_arrow()
                answer = input("Enter a command number: ")
                try:
                    func = self.menu_map[answer]
                except KeyError:
                    print(warning +
                          "\n-- {} is not a valid option--".format(answer))
                else:
                    func()
        finally:
            print(display_1 + '\n\tThanks for using !RemaneR\n')

    def input_new_data(self):
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
                print(warning + '\n--That path does not seem to exist!--\n')
            except renamer.DirectoryNotFoundError:
                print(warning + '\n--Directory not found!--\n')
            except renamer.EmptyDirectoryError:
                print(warning + '\n--This directory is empty!--\n')
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
                print(warning + "\n--This path does not seem to exist!--\n")
            except renamer.FileDoesNotExistError as e:
                print(warning +
                      "\n--Can't find file {}!--\n".format(e.filename))
            except renamer.FileExtensionNotSupported:
                print(warning + "\n--This file extension is not supported!--\n")
            else:
                names = check_names
                break
        self.data = renamer.Renamer(files, names)
        self.data.path = path

    def preview(self):
        self.data.display()

    def change_position(self):
        print()
        draw_command_arrow()
        now = input("Enter the origin index number: ")
        draw_command_arrow()
        then = input("Enter the destination index number: ")
        try:
            self.data.move(int(now), int(then))
        except renamer.IndexOutOfRangeError:
            print(warning + '\n--Index out of range. Try again.--\n')
            func = self.menu_map['2']
            func()
        else:
            print(allgood + "\n--Name position changed--\n")

    def sort_files(self):
        sort_method = ''
        while True:
            print(display_1 + """
Sort files method:
\t""" + display_2 + ' 1 ' + end_fore + """-Ascending order
\t""" + display_2 + ' 2 ' + end_fore + """-Descending order
\t""" + display_2 + ' 3 ' + end_fore + """-Leave it as is
""")
            draw_command_arrow()
            sort_method = input("Enter a command number: ")
            try:
                self.data.sort_files(sort_method)
            except renamer.NotAValidOption:
                print(warning +
                      '\n-- {} is not a valid option--'.format(sort_method))
            else:
                print(allgood + "\n--Files sorted!--\n")
                break

    def apply_rename(self):
        try:
            self.data.rename()
        except renamer.FileNameAlreadyExists as e:
            print(warning + "\nCan't complete rename operation."
                  "\nFilename {} already exist and would be overriden.".
                  format(e.args[0]))
        else:
            print(allgood + '\n--Files successfully renamed!--\n')
            self.quit()

    def quit(self):
        raise SystemExit()
