'''
Usage: main.py <path> <names> (-r)
       main.py -i
       main.py -h

Options:
    -h, --help           : show help page
    path                : path to files to be renamed
    names               : path to the file containing list of names
    -r, --rename        : apply rename operation
    -i, --interactive   : open menu with options
'''


import os
from docopt import docopt
from app.renamer import InputCheckExtract, Renamer
from app.menu import Editor
from app.color_variables import magenta, cyan


if __name__ == "__main__":
    args = docopt(__doc__)

    path = args['<path>']
    names = args['<names>']

    if args['--rename']:
        try:
            files = InputCheckExtract().files_to_rename(path)
        except:
            print(magenta + '\n--Files to be renamed not found--')
        try:
            names = InputCheckExtract().names_file(names)
        except:
            print(magenta +
                  '\n--File containing names not found or not supported--')
        absolute_path = os.path.abspath(path)
        task = Renamer(files, names)
        task.path = absolute_path
        try:
            task.rename()
        except:
            print(magenta + "\n--Can't rename files!--")
        else:
            print(cyan + "\n--Files succesfully renamed!--\n" +
                  cyan + "\n\tThanks for using !RemaneR\n")

    elif args['--interactive']:
        Editor().menu()
