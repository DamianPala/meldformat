#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import stat
import pytest
import shutil
import tempfile
from pathlib import Path
from pprint import pprint

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
    with pytest.raises(meldformat.FileNotFoundError) as exc:
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
def test_format_file_SHOULD_format_file_properly(cwd):
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
    
    meldformat.format_file(meldformat.Formatter.AUTOPEP8, test_file_path, with_meld=False)
    
    assert test_file_path.read_text() == formatted_file_content


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_format_file_SHOULD_format_file_properly_with_setup(cwd):
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

    
