import os
import shutil
from .renamer import InputCheckExtract, Renamer, extension, natural_key


class TestInputCheckExtract:
    temp_test_dir = 'temp_test_dir'

    @classmethod
    def setup_class(cls):
        os.mkdir(cls.temp_test_dir)
        for i in range(1, 6):
            open(cls.temp_test_dir + '/f_{}.txt'.format(i), 'w+')

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.temp_test_dir)

    def test_files_to_rename(self):
        path1 = self.temp_test_dir
        path2 = os.path.abspath(self.temp_test_dir)
        files = ['f_1.txt', 'f_2.txt', 'f_3.txt', 'f_4.txt', 'f_5.txt']
        assert InputCheckExtract().files_to_rename(path1) == files
        assert InputCheckExtract().files_to_rename(path2) == files


def test_extension():
    assert extension('lorem.odt') == '.odt'
    assert extension('lorem.odt', 'ipsum') == '.odt'
    assert extension('-*-') == ''
    assert extension('lorem.odt', '-*-') == ''
    assert extension('lorem') == ''
    assert extension('lorem', 'ipsum') == ''
