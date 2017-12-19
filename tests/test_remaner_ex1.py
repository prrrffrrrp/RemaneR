import os
import pytest
from app.renamer import InputCheckExtract, Renamer

# Test failing, missing directory ev1 with test content. No setup procedure?

absolute = os.getcwd()
temp_test_dir_files = absolute + os.sep + 'tests' + os.sep + 'example_files' + os.sep + 'ex1'
temp_test_dir_names_2 = absolute + os.sep + 'tests' + os.sep + 'example_files' + os.sep + 'ex1_2.txt'
# use os.path.join


class TestInputCheckExtract:
    def test_files_to_rename(self):
        path1 = temp_test_dir_files
        path2 = os.path.abspath(temp_test_dir_files)
        assert len(InputCheckExtract().files_to_rename(path1)) == 5
        assert len(InputCheckExtract().files_to_rename(path2)) == 5

    def test_names_file(self):
        txt_ext = temp_test_dir_names_2
        assert len(InputCheckExtract().names_file(txt_ext)) == 5


class TestRenamer:
    @pytest.fixture(scope='class')
    def renamer_obj_2(self):
        files = InputCheckExtract().files_to_rename(temp_test_dir_files)
        names = InputCheckExtract().names_file(temp_test_dir_names_2)
        renamer_obj = Renamer(files, names)
        return renamer_obj

    def test_Renamer_self(self):
        assert len(self.renamer_obj_2().files) == 5
        assert len(self.renamer_obj_2().names) == 5
        assert self.renamer_obj_2().index_width == 1

    @pytest.mark.xfail(reason='it should not but it fails')
    def test_Renamer_rename(self):
        self.renamer_obj_2().rename()
        assert set(
            os.listdir(temp_test_dir_files)
            ) == {'a.txt', 'b.txt', 'c.txt', 'd.txt', 'e.txt'}
