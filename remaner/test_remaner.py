import os
import shutil
from renamer import InputCheckExtract, Renamer, extension, natural_key


class TestInputCheckExtract:
    absolute = os.getcwd()
    temp_test_dir_files = absolute + os.sep + 'temp_test_dir_files'
    temp_test_dir_names = absolute + os.sep + 'temp_test_dir_names'

    @classmethod
    def setup_class(cls):
        # make temporary directory with files (to be renamed)
        os.mkdir(cls.temp_test_dir_files)
        for i in range(1, 6):
            open(cls.temp_test_dir_files + '/f_{}.txt'.format(i), 'w+')

        # create directory with a file containing filenames
        os.mkdir(cls.temp_test_dir_names)
        with open(os.path.join(
                cls.temp_test_dir_names + os.sep + 'names.txt'), 'w+') as names:
            names.write('orange, lemon, apple, plum, banana')

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.temp_test_dir_files)
        shutil.rmtree(cls.temp_test_dir_names)

    def test_files_to_rename(self):
        path1 = self.temp_test_dir_files
        path2 = os.path.abspath(self.temp_test_dir_files)
        files = ['f_1.txt', 'f_2.txt', 'f_3.txt', 'f_4.txt', 'f_5.txt']
        assert InputCheckExtract().files_to_rename(path1) == files
        assert InputCheckExtract().files_to_rename(path2) == files

    def test_names_file(self):
        txt_ext = self.temp_test_dir_names + os.sep + 'names.txt'
        names = ['orange', 'lemon', 'apple', 'plum', 'banana']
        assert InputCheckExtract().names_file(txt_ext) == names


def test_extension():
    assert extension('lorem.odt') == '.odt'
    assert extension('lorem.odt', 'ipsum') == '.odt'
    assert extension('-*-') == ''
    assert extension('lorem.odt', '-*-') == ''
    assert extension('lorem') == ''
    assert extension('lorem', 'ipsum') == ''
