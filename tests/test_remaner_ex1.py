import os
import pytest
from app.renamer import InputCheckExtract, Renamer


absolute = os.getcwd()
temp_test_dir_files = absolute + os.sep + 'tests' + os.sep + 'example_files' + os.sep + 'ex1'
temp_test_dir_names_1 = absolute + os.sep + 'tests' + os.sep + 'example_files' + os.sep + 'ex1.txt'
temp_test_dir_names_2 = absolute + os.sep + 'tests' + os.sep + 'example_files' + os.sep + 'ex1_2.txt'


class TestInputCheckExtract:
    def test_files_to_rename(self):
        path1 = temp_test_dir_files
        path2 = os.path.abspath(temp_test_dir_files)
        assert len(InputCheckExtract().files_to_rename(path1)) == 5
        assert len(InputCheckExtract().files_to_rename(path2)) == 5

    def test_names_file(self):
        txt_ext = temp_test_dir_names_1
        names = ['f5', 'f4', 'f3', 'f2', 'f1']
        assert InputCheckExtract().names_file(txt_ext) == names


class TestRenamer:
    @pytest.fixture(scope='class')
    def renamer_obj_1(self):
        files = InputCheckExtract().files_to_rename(temp_test_dir_files)
        names = InputCheckExtract().names_file(temp_test_dir_names_1)
        renamer_obj = Renamer(files, names)
        return renamer_obj

    @pytest.fixture(scope='class')
    def renamer_obj_2(self):
        files = InputCheckExtract().files_to_rename(temp_test_dir_files)
        names = InputCheckExtract().names_file(temp_test_dir_names_2)
        renamer_obj = Renamer(files, names)
        return renamer_obj

    def test_Renamer_self(self):
        assert len(self.renamer_obj_1().files) == 5
        assert len(self.renamer_obj_1().names) == 5
        assert self.renamer_obj_1().index_width == 1
        assert len(self.renamer_obj_2().files) == 5
        assert len(self.renamer_obj_2().names) == 5
        assert self.renamer_obj_2().index_width == 1

    def test_Renamer_rename(self):
        # self.renamer_obj_1().rename()
        # assert len(os.listdir(temp_test_dir_files)) == 5
        self.renamer_obj_2().rename()
        assert sorted(
            os.listdir(temp_test_dir_files)
            ) == ['a.txt', 'b.txt', 'c.txt', 'd.txt', 'e.txt']
