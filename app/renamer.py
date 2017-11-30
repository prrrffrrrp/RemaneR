import os
import textract
from itertools import zip_longest
from .color_variables import display_1, end_fore
from .exceptions import PathDoesNotExistError, EmptyDirectoryError,\
    DirectoryNotFoundError, FileDoesNotExistError, FileExtensionNotSupported,\
    IndexOutOfRangeError, NotAValidOption, DuplicateNamesError


class InputCheckExtract:
    def files_to_rename(self, path):
        if not os.path.exists(path):
            raise PathDoesNotExistError
        try:
            files = os.listdir(path)
        except FileNotFoundError:
            raise DirectoryNotFoundError
        else:
            if files == []:
                raise EmptyDirectoryError
            else:
                files.sort()
                return files

    def names_file(self, path_to_file):
        path = os.path.abspath(path_to_file)
        filename = os.path.split(path_to_file)[1]
        if not os.path.exists(path):
            raise PathDoesNotExistError
        if not os.path.isfile(path_to_file):
            raise FileDoesNotExistError(filename)
        try:
            names = set()
            extract = textract.process(path_to_file).decode('utf8')
        except textract.exceptions.ExtensionNotSupported:
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
    def __init__(self, files, names):
        self.files = files
        self.names = names
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
        pairs = list(zip_longest(self.files, self.names, fillvalue='-*-'))
        return pairs

    def display(self):
        max_files = max([len(x) for x in self.files])
        max_names = max([len(x) for x in self.names])
        display_width = max_files + max_names + self.index_width + 15
        print()
        print(display_1 + '!RemaneR'.center(display_width))
        print(display_1 + ('_' * display_width))
        for i, v in enumerate(self.pairs(), start=1):
            print(str(i).ljust(self.index_width) +
                  display_1 + ' _ ' + end_fore +
                  v[0].ljust(max_files) +
                  display_1 + ' -----> ' + end_fore +
                  v[1] +
                  '{}'.format(extension(v[0], v[1])))
        print(display_1 + '_' * display_width)
        print()

    def sort_files(self, sort_method):
        if sort_method not in ['1', '2', '3']:
            raise NotAValidOption
        if sort_method == '3':
            return                          # to do: back to original sort
        if sort_method == '1':
            order = False
        if sort_method == '2':
            order = True
        self.files = sorted(self.files, key=natural_key, reverse=order)

    def rename(self):
        temp_names = []
        for n in self.pairs():

            if '-*-' in n:
                continue

            old = os.path.join(self.path, n[0])
            new = os.path.join(self.path, n[1] + extension(n[0]))
            new_n = os.path.basename(new)
            # Avoid accidental overide
            if old != new and new_n in self.files:
                # raise FileNameAlreadyExists(os.path.basename(new))
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
        len_f = len(self.files)
        len_n = len(self.names)
        if len_n < len_f:
            self.names = self.names + ['-*-'] * (len_f - len_n)
        for n in [now, then]:
            if not 1 <= n <= len(self.pairs()):
                raise IndexOutOfRangeError
        names_cp = self.names
        names_cp.insert(then - 1, names_cp.pop(now - 1))
        self.names = names_cp


def extension(file_name, new_name=None):
    if file_name == '-*-' or new_name == '-*-':
        return ''
    for i in range(len(file_name)-1, 0, -1):
        if file_name[i] == '.':
            return file_name[i:]
    return ''


def natural_key(string_):
    ''' Allows human sorting. See Natural Sorting Algorithm.'''
    import re
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]
