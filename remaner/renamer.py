import os
import textract
from itertools import zip_longest
from exceptions import PathDoesNotExistError, EmptyDirectoryError,\
    DirectoryNotFoundError, FileDoesNotExistError, FileExtensionNotSupported,\
    IndexOutOfRangeError, NotAValidOption


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
                return files

    def names_file(self, path_to_file):
        path = os.path.abspath(path_to_file)
        filename = os.path.split(path_to_file)[1]
        if not os.path.exists(path):
            raise PathDoesNotExistError
        if not os.path.isfile(path_to_file):
            raise FileDoesNotExistError(filename)
        try:
            names = textract.process(path_to_file).decode('utf8')
        except textract.exceptions.ExtensionNotSupported:
            raise FileExtensionNotSupported
        else:
            if '\n' in names:
                names = names.splitlines()
            if ',' in names:
                names = names.split(',')

        names = [name.strip() for name in names if not name == '']
        return names


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
        display_with = max_files + max_names + self.index_width + 11
        print()
        print('!RemaneR'.center(display_with))
        print('_' * display_with)
        for i, v in enumerate(self.pairs(), start=1):
            print(str(i).ljust(self.index_width) +
                  ' _ ' +
                  v[0].ljust(max_files) +
                  ' -----> ' +
                  v[1] +
                  '{}'.format(extension(v[0], v[1])))
        print('_' * display_with)
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
        for n in self.pairs():
            if '-*-' in n:
                continue
            old = os.path.join(self.path, n[0])
            new = os.path.join(self.path, n[1] + extension(n[0]))
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
    if new_name == '-*-':
        return ''
    elif file_name == '-*-':
        return ''
    for i, v in enumerate(file_name):
        if v == '.':
            return file_name[i:]


def natural_key(string_):
    ''' Allows human sorting. See Natural Sorting Algorithm.'''
    import re
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]
