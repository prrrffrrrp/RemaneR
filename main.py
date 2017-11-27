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
from renamer import InputCheckExtract, Renamer
from menu import Editor
from color_variables import warning, display_1


if __name__ == "__main__":
    args = docopt(__doc__)

    path = args['<path>']
    names = args['<names>']

    if args['--rename']:
        try:
            files = InputCheckExtract().files_to_rename(path)
        except:
            print(warning + '\n--Files to be renamed not found--')
        try:
            names = InputCheckExtract().names_file(names)
        except:
            print(warning +
                  '\n--File containing names not found or not supported--')
        absolute_path = os.path.abspath(path)
        task = Renamer(files, names)
        task.path = absolute_path
        try:
            task.rename()
        except:
            print(warning + "\n--Can't rename files!--")
        else:
            print(display_1 + "\n--Files renamed!--" +
                  display_1 + "\n\tThanks for using !RemaneR\n")

    elif args['--interactive']:
        Editor().menu()
