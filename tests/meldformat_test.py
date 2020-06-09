#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import stat
import pytest
import shutil
import logging
import tempfile
from pathlib import Path

import meldformat


RUN_ALL_TESTS = True


def _error_remove_readonly(_action, name, _exc):
    Path(name).chmod(stat.S_IWRITE)
    Path(name).unlink()
    
    
@pytest.fixture()
def cwd():
    workspace_path = Path(tempfile.mkdtemp())
    yield workspace_path
    if getattr(sys, 'last_value'):
        print(f'Tests workspace path: {workspace_path}')
    else:
        shutil.rmtree(workspace_path, ignore_errors=False, onerror=_error_remove_readonly)


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_file_SHOULD_raise_error_when_incorrect_formatter():
    with pytest.raises(meldformat.FormatterNotSpecifiedError):
        meldformat.format_file('dummy_formatter', 'file')


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_file_SHOULD_raise_error_when_is_not_a_file(cwd):
    with pytest.raises(meldformat.NotAFileError) as exc:
        meldformat.format_file(meldformat.Formatter.AUTOPEP8, cwd)

    assert 'File to format' in str(exc.value)

@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_file_SHOULD_raise_error_when_file_not_exists(cwd):
    with pytest.raises(meldformat.PathNotFoundError) as exc:
        meldformat.format_file(meldformat.Formatter.AUTOPEP8, cwd / 'file.txt')

    assert 'File to format' in str(exc.value)

@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_file_SHOULD_raise_error_when_setup_is_not_a_file(cwd):
    test_file_path = cwd / 'test.txt'
    test_file_path.touch()
    
    with pytest.raises(meldformat.NotAFileError) as exc:
        meldformat.format_file(meldformat.Formatter.AUTOPEP8, test_file_path, setup_path=cwd)

    assert 'Formatter setup' in str(exc.value)


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_file_SHOULD_raise_error_when_setup_file_not_exists(cwd):
    test_file_path = cwd / 'test.txt'
    test_file_path.touch()
    
    with pytest.raises(meldformat.FileNotFoundError) as exc:
        meldformat.format_file(meldformat.Formatter.AUTOPEP8, test_file_path, setup_path=cwd / 'setup.cfg')
    
    assert 'Formatter setup' in str(exc.value)


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_file_SHOULD_format_file_properly_USING_autopep8(cwd):
    not_formatted_file_content = """
if __name__ == '__main__':
    main()
    
"""

    formatted_file_content = """
if __name__ == '__main__':
    main()
"""
    
    test_file_path = cwd / 'module.py'
    test_file_path.write_text(not_formatted_file_content)
    
    formatted_file_path = meldformat.format_file(meldformat.Formatter.AUTOPEP8, test_file_path, with_meld=False)
    
    assert test_file_path.read_text() == formatted_file_content
    assert formatted_file_path == test_file_path


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_file_SHOULD_do_nothing_WHEN_no_changes(cwd, caplog):
    not_formatted_file_content = "\nif __name__ == '__main__':\n    main()\n"

    formatted_file_content = "\nif __name__ == '__main__':\n    main()\n"
    
    test_file_path = cwd / 'module.py'
    with open(test_file_path, 'w', newline='\n')as file:
        file.write(not_formatted_file_content)
    
    meldformat._logger.setLevel(logging.INFO)
    formatted_file_path = meldformat.format_file(meldformat.Formatter.AUTOPEP8, test_file_path, with_meld=False)
    
    assert test_file_path.read_text() == formatted_file_content
    assert formatted_file_path is None
    assert 'No changes in' in caplog.text


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_file_SHOULD_format_file_properly_WHEN_path_is_relative(cwd):
    not_formatted_file_content = """
if __name__ == '__main__':
    main()
    
"""

    formatted_file_content = """
if __name__ == '__main__':
    main()
"""
    
    temp_cwd = Path().cwd()
    os.chdir(cwd)
    
    test_file_path = cwd / 'module.py'
    test_file_path.write_text(not_formatted_file_content)
    
    meldformat.format_file(meldformat.Formatter.AUTOPEP8, test_file_path.name, with_meld=False)
    
    os.chdir(temp_cwd)
    
    assert test_file_path.read_text() == formatted_file_content


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_file_SHOULD_format_file_properly_WHEN_path_is_relative_and_parantheses(cwd):
    not_formatted_file_content = """
if __name__ == '__main__':
    main()
    
"""

    formatted_file_content = """
if __name__ == '__main__':
    main()
"""
    
    temp_cwd = Path().cwd()
    os.chdir(cwd)
    
    test_file_path = cwd / 'module.py'
    test_file_path.write_text(not_formatted_file_content)
    
    meldformat.format_file(meldformat.Formatter.AUTOPEP8, f'"{test_file_path.name}"', with_meld=False)
    
    os.chdir(temp_cwd)
    
    assert test_file_path.read_text() == formatted_file_content


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_file_SHOULD_format_file_properly_WHEN_path_is_absolute_and_parantheses(cwd):
    not_formatted_file_content = """
if __name__ == '__main__':
    main()
    
"""

    formatted_file_content = """
if __name__ == '__main__':
    main()
"""
    
    temp_cwd = Path().cwd()
    os.chdir(cwd)
    
    test_file_path = cwd / 'module.py'
    test_file_path.write_text(not_formatted_file_content)
    
    meldformat.format_file(meldformat.Formatter.AUTOPEP8, f'"{test_file_path.__str__()}"', with_meld=False)
    
    os.chdir(temp_cwd)
    
    assert test_file_path.read_text() == formatted_file_content


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_file_SHOULD_format_file_properly_with_setup_USING_autopep8(cwd):
    not_formatted_file_content = """
if __name__ == '__main__':
    def this_is_very_long_long_long_function(param1, param2, param3, param4, param5, param6, param7, param8):
        pass
"""

    formatted_file_content = """
if __name__ == '__main__':
    def this_is_very_long_long_long_function(
            param1,
            param2,
            param3,
            param4,
            param5,
            param6,
            param7,
            param8):
        pass
"""
    
    setup_file_path = Path(cwd) / 'setup.cfg'
    setup_file_path.write_text("""
[flake8]
aggressive=2
""")
    
    test_file_path = cwd / 'module.py'
    test_file_path.write_text(not_formatted_file_content)
    
    meldformat.format_file(meldformat.Formatter.AUTOPEP8, test_file_path, setup_path=setup_file_path, with_meld=False)
    print(test_file_path.read_text())
    
    assert test_file_path.read_text() == formatted_file_content


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_file_SHOULD_format_file_properly_USING_clang_format(cwd):
    not_formatted_file_content = """
#include "module1.h"


int module1_add(int a, int b) { return a + b; } 
"""

    formatted_file_content = """
#include "module1.h"

int module1_add(int a, int b) { return a + b; }
"""
    
    test_file_path = cwd / 'module.c'
    test_file_path.write_text(not_formatted_file_content)
    print(test_file_path.read_text())
    
    meldformat.format_file(meldformat.Formatter.CLANGFORMAT, test_file_path, with_meld=False)
    print(test_file_path.read_text())
    
    assert test_file_path.read_text() == formatted_file_content


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_file_SHOULD_format_file_properly_with_setup_USING_clang_format(cwd):
    not_formatted_file_content = """
#include "module1.h"

int module1_add(int a, int b) { return a + b; } 
"""

    formatted_file_content = """
#include "module1.h"

int module1_add(int a, int b)
{
  return a + b;
}
"""
    
    test_file_path = cwd / 'module.c'
    test_file_path.write_text(not_formatted_file_content)
    
    setup_path = Path(__file__).parent / '.clang-format'
    meldformat.format_file(meldformat.Formatter.CLANGFORMAT, test_file_path, setup_path=setup_path, with_meld=False)
    print(test_file_path.read_text())
    
    assert test_file_path.read_text() == formatted_file_content


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_is_line_endings_differences_or_no_changes_SHOULD_return_true_if_only_line_endings_differences(cwd):
    file1_path = cwd / 'file1.txt'
    file2_path = cwd / 'file2.txt'
    with open(file1_path, 'w', newline='\n')as file1, open(file2_path, 'w', newline='\r\n') as file2:
        file1.write('line1\nline2\n')
        file2.write('line1\nline2\n')
    
    assert meldformat._is_line_endings_differences_or_no_changes(file1_path, file2_path) == True


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_is_line_endings_differences_or_no_changes_SHOULD_return_true_if_the_same_files(cwd):
    file1_path = cwd / 'file1.txt'
    file2_path = cwd / 'file2.txt'
    with open(file1_path, 'w', newline='\n')as file1, open(file2_path, 'w', newline='\n') as file2:
        file1.write('line1\nline2\n')
        file2.write('line1\nline2\n')
    
    assert meldformat._is_line_endings_differences_or_no_changes(file1_path, file2_path) == True


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_is_line_endings_differences_or_no_changes_SHOULD_return_false_if_changes_and_different_line_endings(cwd):
    file1_path = cwd / 'file1.txt'
    file2_path = cwd / 'file2.txt'
    with open(file1_path, 'w', newline='\n')as file1, open(file2_path, 'w', newline='\r\n') as file2:
        file1.write('line1\nline2\n')
        file2.write('line1\nlines2\n')

    assert meldformat._is_line_endings_differences_or_no_changes(file1_path, file2_path) == False


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_is_line_endings_differences_or_no_changes_SHOULD_return_false_if_changes_and_the_same_line_endings(cwd):
    file1_path = cwd / 'file1.txt'
    file2_path = cwd / 'file2.txt'
    with open(file1_path, 'w', newline='\n')as file1, open(file2_path, 'w', newline='\n') as file2:
        file1.write('line1\nline2\n')
        file2.write('line1\nlines2\n')

    assert meldformat._is_line_endings_differences_or_no_changes(file1_path, file2_path) == False    


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_collect_files_to_format_SHOULD_collect_files_properly(cwd):
    (cwd / 'file1.c').touch()
    (cwd / 'file2.c').touch()
    (cwd / 'file1.h').touch()
    (cwd / 'file2.h').touch()
    (cwd / 'file1.cpp').touch()
    (cwd / 'file1.cxx').touch()
    (cwd / 'file1.txt').touch()
    (cwd / 'dir').mkdir()
    (cwd / 'dir' / 'file1.hpp').touch()
    (cwd / 'dir' / 'file1.hxx').touch()
    (cwd / 'dir' / 'file1.txt').touch()
    (cwd / 'dir' / 'file1.cfg').touch()
    
    expected_paths = {
        'dir/file1.hpp',
        'dir/file1.hxx',
        'file1.c',
        'file1.cpp',
        'file1.cxx',
        'file1.h',
        'file2.c',
        'file2.h'
    }

    formatter = meldformat.ClangFormatter

    paths = {path.relative_to(cwd).as_posix() for path in meldformat._collect_files_to_format(formatter, cwd)}

    assert paths == expected_paths


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_dir_SHOULD_format_directory_properly(cwd):
    not_formatted_file1_content = """
if __name__ == '__main__':
    main()
    
"""

    formatted_file1_content = """
if __name__ == '__main__':
    main()
"""

    not_formatted_file2_content = """
if __name__ == '__main__':
    fun()
    
"""

    formatted_file2_content = """
if __name__ == '__main__':
    fun()
"""
    
    expected_formatted_files_paths = {
        'module1.py',
        'module2.py',
        'dir/module3.py'
    }

    (cwd / 'file1.txt').touch()
    (cwd / 'dir').mkdir()
    (cwd / 'dir' / 'file1.txt').touch()
    (cwd / 'dir' / 'file1.cfg').touch()
    
    test_file1_path = cwd / 'module1.py'
    test_file1_path.write_text(not_formatted_file1_content)
    test_file2_path = cwd / 'module2.py'
    test_file2_path.write_text(not_formatted_file2_content)
    test_file3_path = cwd / 'dir' / 'module3.py'
    test_file3_path.write_text(not_formatted_file2_content)
    
    meldformat._logger.setLevel(logging.INFO)
    formatted_files_paths = {path.relative_to(cwd).as_posix() 
                             for path in meldformat.format_dir(meldformat.Formatter.AUTOPEP8, cwd, with_meld=False)}
    
    assert test_file1_path.read_text() == formatted_file1_content
    assert test_file2_path.read_text() == formatted_file2_content
    assert test_file3_path.read_text() == formatted_file2_content
    assert formatted_files_paths == expected_formatted_files_paths


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_dir_SHOULD_raise_error_WHEN_path_not_exists(cwd):
    with pytest.raises(meldformat.PathNotFoundError):
        meldformat.format_dir(meldformat.Formatter.AUTOPEP8, cwd / 'dir', with_meld=False)


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_dir_SHOULD_raise_error_WHEN_path_not_a_directory(cwd):
    (cwd / 'file.txt').touch()
    
    with pytest.raises(meldformat.NotADirectoryError):
        meldformat.format_dir(meldformat.Formatter.AUTOPEP8, cwd / 'file.txt', with_meld=False)


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_dir_SHOULD_return_empty_WHEN_no_files_to_format(cwd):
    (cwd / 'file.txt').touch()
    
    assert meldformat.format_dir(meldformat.Formatter.AUTOPEP8, cwd, with_meld=False) is None


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_dir_SHOULD_print_no_changes_WHEN_no_changes(cwd, caplog):
    not_formatted_file_content = "\nif __name__ == '__main__':\n    main()\n"

    formatted_file_content = "\nif __name__ == '__main__':\n    main()\n"
    
    test_file_path = cwd / 'module.py'
    with open(test_file_path, 'w', newline='\n')as file:
        file.write(not_formatted_file_content)
    
    meldformat._logger.setLevel(logging.INFO)
    formatted_files_paths = meldformat.format_dir(meldformat.Formatter.AUTOPEP8, cwd, with_meld=False)
    
    assert test_file_path.read_text() == formatted_file_content
    assert formatted_files_paths is None
    assert 'No changes in' in caplog.text
