#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import shutil
import logging
import tempfile
import autopep8
import subprocess
from pathlib import Path
from enum import Enum


__author__ = 'Damian Pala'
__version__ = '0.0.1'


_logger = logging.getLogger(__name__)


class MeldFormatError(Exception):
    def __init__(self, msg, logger):
        super().__init__(msg)
        self.logger = logger


class NotAFileError(MeldFormatError):
    pass


class FileNotFoundError(MeldFormatError):
    pass


class FormatterNotSpecifiedError(MeldFormatError):
    pass


class ExecuteCmdError(MeldFormatError):
    pass


class MeldError(MeldFormatError):
    pass


class Autopep8Formatter():
    name = 'Autopep8'
    linter = 'flake8'

    @staticmethod
    def format_file(file_to_format_path, setup_path):
        if setup_path is not None:
            options = autopep8.parse_args(('--global-config='+setup_path.__str__(),
                                           file_to_format_path.__str__()), apply_config=True)
        else:
            options = None
        temp_fd, temp_path = tempfile.mkstemp(prefix=f'{file_to_format_path.stem}_', suffix=file_to_format_path.suffix, text=True)
        with os.fdopen(temp_fd, 'w') as file:
            autopep8.fix_file(file_to_format_path.__str__(), output=file, options=options)
            
        return Path(temp_path)

    @staticmethod
    def lint_file(file_to_lint_path, setup_path):
        _logger.info('Lint formatted file and show report.')

        if not shutil.which(Autopep8Formatter.linter):
            raise MeldError(f'{Autopep8Formatter.linter} not found. Please install it and add to PATH', _logger)

        try:
            _execute_cmd([Autopep8Formatter.linter, file_to_lint_path.__str__(), f'--config={setup_path}'])
        except ExecuteCmdError as e:
            return e.__str__()
        else:
            _logger.info('File is OK!')


class ClangFormatter():
    pass


class Formatter(Enum):
    AUTOPEP8 = Autopep8Formatter
    CLANGFORMAT = ClangFormatter


def format_file(formatter, path, setup_path=None, with_meld=True):
    if not isinstance(formatter, Formatter):
        raise FormatterNotSpecifiedError('Formatter is not specified properly. Use Formatter class', _logger)
    
    formatter = formatter.value
    
    if with_meld:
        _logger.info(f'Format the file: {path} using the {formatter.name} '
                     f'with merge mode in Meld.')
    else:
        _logger.info(f'Format the file: {path} using the {formatter.name}.')
    
    path = Path().cwd().resolve() / path
    if not path.exists():
        raise FileNotFoundError('File to format not exists!', _logger)
    if not path.is_file():
        raise NotAFileError('File to format path must point to a file!', _logger)
    if setup_path is not None:
        setup_path = Path().cwd().resolve() / setup_path
        if not setup_path.exists():
            raise FileNotFoundError('Formatter setup file not exists!', _logger)
        if not setup_path.is_file():
            raise NotAFileError('Formatter setup path must point to a file!', _logger)
    
    formatted_file_path = formatter.format_file(path, setup_path)
    
    if with_meld:
        if not shutil.which('meld'):
            raise MeldError('Meld not found. Please install it and add to PATH', _logger)

        merge_changes(path, formatted_file_path)
    else:
        path.unlink()
        shutil.copy(formatted_file_path, path)
    
    if hasattr(formatter, 'lint_file'):
        linter_output = formatter.lint_file(path, setup_path)
        if linter_output:
            print(linter_output)


def merge_changes(file_to_format_path, formatted_file_path):
    try:
        _execute_cmd(('meld', 
                      file_to_format_path.__str__(), 
                      file_to_format_path.__str__(), 
                      formatted_file_path.__str__(), 
                      '-o', file_to_format_path.__str__()))
    except ExecuteCmdError as e:
        raise MeldError(f'Error occured while run Meld: {e}', _logger)
    formatted_file_path.unlink()


def _execute_cmd(args):
    try:
        p = subprocess.run(args,
                           check=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           encoding='utf-8')
    except subprocess.CalledProcessError as e:
        raise ExecuteCmdError(e.output, _logger)
    else:
        return p.stdout


_logger.setLevel(logging.INFO)
_logger.warning('textst')
print('yyy')
# format_file(Formatter.AUTOPEP8, 'tests/meldformat_test.py', with_meld=True)
