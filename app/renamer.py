import os
# import textract
from .extract_docx import get_docx_text
from itertools import zip_longest
from .color_variables import cyan, end_fore
from .exceptions import PathDoesNotExistError, EmptyDirectoryError,\
    DirectoryNotFoundError, FileDoesNotExistError, FileExtensionNotSupported,\
    IndexOutOfRangeError, NotAValidOption, DuplicateNamesError, RevertSuffix


class InputCheckExtract:
    '''
    Checks user input (paths and files) for validity and extracts data.
    '''
    def files_to_rename(self, path):
        '''
        The path argument should contain the path to the files that
        the user wants to rename.
        The method checks that the path exists and that the
        directory is not empty. Returns an alfabetically ordered list of files.
        '''

        if not os.path.exists(path):
            raise PathDoesNotExistError
        try:
            files = os.listdir(path)
        except Exception:
            raise DirectoryNotFoundError
        else:
            if files == []:
                raise EmptyDirectoryError
            else:
                files = sorted(files, key=natural_key)
                return files

    def names_file(self, path_to_file):
        '''
        The path to file argument should contain the path and the
        full name (with the extension) of the file that contains
        the list of names that we want to use to rename the files
        listed by the files_to_rename rename method.
        The file containing names can be of any type that is supported
        by the textract module. However, the only formats that have been
        tested so far are:
            -.xlsx with a single column of data.
            -.docx, .odt and .txt formats containing words separated
            by a coma or by a next lign character.
        The names_file method checks that the path and file exist,
        that the extension is supported by the textract library and
        that there are no duplicated names in the names list (what
        could lead to file overriding).
        Returns a list.
        '''
        path = os.path.abspath(path_to_file)
        filename = os.path.split(path_to_file)[1]
        if not os.path.exists(path):
            raise PathDoesNotExistError
        if not os.path.isfile(path_to_file):
            raise FileDoesNotExistError(filename)
        try:
            names = set()
            extract = get_docx_text(path_to_file)
        except Exception:
            raise FileExtensionNotSupported
        else:
            if '\n' in extract:
                extract = extract.splitlines()
            if ',' in extract:
                extract = extract.split(',')
            if len(extract) == 1:
                # In case there is only one line with a \n at the end of it
                # example- names.txt: f1, f2, f3\n
                # in which case names becomes a list with a single item:
                # example- names=['f1, f2, f3']
                # in which case there is nothing to split with ','.
                if ',' in extract[0]:
                    extract = extract[0].split(',')
            extract = [name.strip() for name in extract if not name == '']
            for name in extract:
                if name not in names:
                    names.add(name)
                else:
                    raise DuplicateNamesError(name)
            return extract


class Renamer:
    '''
    Class that contains all the core features that allow to manipulate
    the data entered by the user.
    '''
    def __init__(self, files, names):
        '''
        Initializes an instance with a list of files and a list of names that
        can be both subjected to changes.
        '''
        self.files = files
        self.names = names
        self.names_backup = names
        self.index_width = max((len(str(len(self.files)))),
                               (len(str(len(self.names)))))
        self.path = ''

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, files_val):
        self._files = files_val

    @property
    def names(self):
        return self._names

    @names.setter
    def names(self, names_val):
        self._names = names_val

    def pairs(self):
        '''
        Creates a list of tuples.
        In each tuple there is a file name and a new name that will
        replace the former.
        If the the two lists (files and names) are not of equal length,
        when one of the lists reaches its end, a fill value is used
        that artifitially extends it allowing tuples to continue to be
        formed and expose all the items of either lists.
        '''
        pairs = list(zip_longest(self.files, self.names, fillvalue='-*-'))
        return pairs

    def display(self):
        '''
        Offers a visualization of the existing files and their new names.
        The new names appear with the same file extension that existing
        files have.
        '''
        max_files = max([len(x) for x in self.files])
        max_names = max([len(x) for x in self.names])
        display_width = max_files + max_names + self.index_width + 15
        print()
        print(cyan + '!RemaneR'.center(display_width))
        print(cyan + ('_' * display_width))
        for i, v in enumerate(self.pairs(), start=1):
            print(str(i).ljust(self.index_width) +
                  cyan + ' _ ' + end_fore +
                  v[0].ljust(max_files) +
                  cyan + ' -----> ' + end_fore +
                  v[1] +
                  '{}'.format(extension(v[0], v[1])))
        print(cyan + '_' * display_width)
        print()

    def sort_files(self, sort_method):
        '''
        Allows changing the way current files are sorted.
        The options are:
            1-Alphabetical ascending order
            2-Alphabetical descending order
            3-ASCII ascending order
            4-ASCII descending order
        '''
        if sort_method not in ['1', '2', '3', '4']:
            raise NotAValidOption
        if sort_method == '1':
            key = natural_key
            order = False
        if sort_method == '2':
            key = natural_key
            order = True
        if sort_method == '3':
            key = None
            order = False
        if sort_method == '4':
            key = None
            order = True
        self.files = sorted(self.files, key=key, reverse=order)

    def rename(self):
        '''
        Calls the self.pairs method and changes the name of the files.
        Doesn't do anything if the self.pairs tuple contains a fill
        value instead of a rightfull (file, name) pair.
        When a file new name is detected to exist already in the current
        files list, the new name is not applied directly to avoid file
        overriding. Instead, a temporary name is given to that file.
        The definitive name is applied when the rest of files have been
        renamed.
        '''
        temp_names = []
        for n in self.pairs():

            if '-*-' in n:
                continue

            old = os.path.join(self.path, n[0])
            new = os.path.join(self.path, n[1] + extension(n[0]))
            new_n = os.path.basename(new)
            # Avoid accidental overide
            if old != new and new_n in self.files:
                new += '_temp'
                temp_names.append(new)
                os.rename(old, new)
            else:
                os.rename(old, new)

        if temp_names:
            for temp in temp_names:
                old = temp
                new = old[:-5]
                os.rename(old, new)

    def move(self, now, then):
        '''
        Allows changing the position of items in the names list.
        It will result in the creation of new (file, name) tuples in
        the pairs list.
        '''
        len_f = len(self.files)
        len_n = len(self.names)
        if len_n < len_f:
            self.names = self.names + ['-*-'] * (len_f - len_n)
        for n in [now, then]:
            if not 1 <= n <= len(self.pairs()):
                raise IndexOutOfRangeError
        names_cp = self.names[:]
        names_cp.insert(then - 1, names_cp.pop(now - 1))
        self.names = names_cp

    def add_suffix(self, suffix, mode):
        '''
        Allows adding a suffix to the existing names from the names file.
        There are two modalities:
            -All: all the names get the same suffix.
            -Alternate: each name is duplicated and the suffix is added to the
            duplicate.
        In both modalities the suffix is the same for all the files that get
        one.
        '''
        if mode not in ['1', '2', '3', '4']:
            raise NotAValidOption
        if mode == '1':
            self.names = [n + suffix for n in self.names]
        if mode == '2' or mode == '3':
            names_cp = self.names[:]
            item = 0
            # x is added to the enumerate index to determine where to
            # insert the suffixed names (before or after the original name).
            x = 0 if mode == '2' else 1
            for i, n in enumerate(self.names):
                i += item
                names_cp.insert(i + x, (n + suffix))
                item += 1
            self.names = names_cp[:]
        if mode == '4':
            self.names = self.names_backup
            raise RevertSuffix


def extension(file_name, new_name=None):
    '''
    Detects the extension of the current file.
    It can be used to add the same extension to the new name that
    will be given to the current file.
    '''
    if file_name == '-*-' or new_name == '-*-':
        return ''
    for i in range(len(file_name)-1, 0, -1):
        if file_name[i] == '.':
            return file_name[i:]
    return ''


def natural_key(string_):
    ''' Allows human sorting. See Natural Sorting Algorithm.'''
    import re
    return [int(s) if s.isdigit() else s.lower() for s in re.split(r'(\d+)',
                                                                   string_)]
