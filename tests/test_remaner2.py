import os
import shutil
import pytest
import tempfile
from app.renamer import InputCheckExtract, Renamer, extension, natural_key
from app.exceptions import DuplicateNamesError, EmptyDirectoryError

absolute = os.getcwd()
temp_test_dir_files = tempfile.mkdtemp()
temp_test_dir_names = tempfile.mkdtemp(suffix='_1')


@pytest.fixture(scope="module")
def setup_temps(request):
    # make temporary directory with files (to be renamed)
    for i in range(1, 6):
        open(temp_test_dir_files + '/f_{}.txt'.format(i), 'w')

    # create directory with a file containing filenames
    with open(os.path.join(temp_test_dir_names, 'names.txt'), 'w') as names:
        names.write('orange, lemon, apple, plum, banana')

    def teardown_temps():
        ''' Remove the temp directory and namesFile '''
        shutil.rmtree(temp_test_dir_files)
        shutil.rmtree(temp_test_dir_names)

    request.addfinalizer(teardown_temps)


class TestInputCheckExtract:
    def test_files_to_rename(self, setup_temps):
        path1 = temp_test_dir_files
        path2 = os.path.abspath(temp_test_dir_files)
        files = ['f_1.txt', 'f_2.txt', 'f_3.txt', 'f_4.txt', 'f_5.txt']
        assert InputCheckExtract().files_to_rename(path1) == files
        assert InputCheckExtract().files_to_rename(path2) == files

    def test_names_file(self, setup_temps):
        txt_file = temp_test_dir_names + os.sep + 'names.txt'
        names = ['orange', 'lemon', 'apple', 'plum', 'banana']
        assert InputCheckExtract().names_file(txt_file) == names


class TestInputCheckExtractDuplicates:
    def setup_method(self, method):
        with open(os.path.join(temp_test_dir_names, 'names.txt'), 'a') as names:
            names.write(', lemon')

    def teardown_method(self, method):
        with open(os.path.join(temp_test_dir_names, 'names.txt'), 'w') as names:
            names.write('orange, lemon, apple, plum, banana')

    def test_duplicate_names(self):
        txt_file = os.path.join(temp_test_dir_names, 'names.txt')
        with pytest.raises(DuplicateNamesError) as excinfo:
            InputCheckExtract().names_file(txt_file)
        assert "lemon" in str(excinfo.value)


class TestInputCheckExtractEmptyDirectoryError:
    @pytest.fixture(scope="class")
    def setup_method(request):
        empty_dir = tempfile.mkdtemp()
        with pytest.raises(EmptyDirectoryError) as excinfo:
            InputCheckExtract().files_to_rename(os.path.abspath(empty_dir))
        assert "empty!" in str(excinfo.value)


class TestRenamer:
    @pytest.fixture(scope='class')
    def renamer_obj(self):
        txt_file = temp_test_dir_names + os.sep + 'names.txt'
        files = InputCheckExtract().files_to_rename(temp_test_dir_files)
        names = InputCheckExtract().names_file(txt_file)
        renamer_obj = Renamer(files, names)
        return renamer_obj

    def test_Renamer_self(self):
        assert len(self.renamer_obj().files) == 5
        assert len(self.renamer_obj().names) == 5
        assert self.renamer_obj().index_width == 1


def test_extension():
    assert extension('lorem.odt') == '.odt'
    assert extension('lorem.odt', 'ipsum') == '.odt'
    assert extension('-*-') == ''
    assert extension('lorem.odt', '-*-') == ''
    assert extension('lorem') == ''
    assert extension('lorem', 'ipsum') == ''
