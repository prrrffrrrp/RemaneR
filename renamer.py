import os
import textract


class EmptyDirectoryError(Exception):
    pass


class FileExtensionNotSupported(Exception):
    pass


class NotSameLenghtError(Exception):
    pass

class IndexOutOfRangeError(Exception):
    pass


class OriginalFiles:
    def find_files(self, path):
        try:
            files = os.listdir(path)
        except FileNotFoundError:
            print("Can't find such directory")
        else:
            if files == []:
                raise EmptyDirectoryError
            else:
                return files


class NamesFile:
    def find_names(self, path_to_filename):
        path_to_filename = os.path.abspath(path_to_filename)
        filename = os.path.split(path_to_filename)[1]
        try:
            names = textract.process(path_to_filename).decode('utf8')

        except textract.exceptions.MissingFileError:
            print("Can't find file {}".format(filename))

        else:
            if '\n' in names:
                names = names.splitlines()
            if ',' in names:
                names = names.split(',')

            names = [name.strip() for name in names if not name == '']
            return names


class Renamer:
    def __init__(self, path, names):
        self.path = os.path.abspath(path)
        self.files = OriginalFiles().find_files(path)
        self.names = NamesFile().find_names(names)
        self.combine = list(zip(self.files, self.names))

    def display(self):
        #if not len(self.files) == len(self.names):
        #    raise NotSameLenghtError

        len_i = len(str(len(self.files)))
        max_files = max([len(x) for x in self.files])
        max_names = max([len(x) for x in self.names])
        display_with = max_files + max_names + len_i + 11
        print()
        print('!RemaneR'.center(display_with))
        print('_' * display_with)
        for i, v in enumerate(self.combine, start=1):
            print(str(i).ljust(len_i) + ' _ ' + v[0].ljust(max_files) +
                  ' -----> ' + v[1] + '{}'.format(extension(v[0])))
        print('_' * display_with)
        print()

    def rename(self):
        for n in self.combine:
            old = os.path.join(self.path, n[0])
            new = os.path.join(self.path, n[1] + extension(n[0]))
            os.rename(old, new)

    def move(self, now, then):
        for n in [now, then]:
            if not 1 <= n <= len(self.combine):
                raise IndexOutOfRangeError
        self.names.insert(then - 1, self.names.pop(now - 1))
        self.combine = list(zip(self.files, self.names))


def extension(file_name):
    for i, v in enumerate(file_name):
        if v == '.':
            return file_name[i:]


#a = Renamer()
#a.input_data()
#a.display()
#a.rename()
