# Meldformat

Meldformat is a tool for convenient formatting your source code files according to a chosen formatter e.g. Autopep8. It incorporates [Meld](http://meldmerge.org/) tool to simple merging formatted files that provides more control and insight what is actually changes during formatting a file. Formatting an entire directory is also possible.

Meldformat is intended to use only as a python module.

## Workflow

1. Read a source file

2. Format contents

3. Write a temporary formatted file

4. Open [Meld](http://meldmerge.org/) in a 3 pane mode with files:

   | NOT FORMATTED FILE | FINAL FILE | FORMATTED FILE |
   | ------------------ | ---------- | -------------- |
   | some code          | some code  | some code      |


5. Merge changes manually
6. Save final file manually


## Requirements

- [Meld](http://meldmerge.org/) to merging files
- Autopep8 to format python sources
- Clang-Format to format C and C++ sources

## Features

- There are two formatters available:
  - Autopep8 for Python with Flake8 as linter
  - Clang-Format for C and C++
- Format a specified file
- Format an entire directory
- Provide a setup file with a configuration for the formatter
- When using Meld is chosen and the formatted file has changes only in line endings then it is treated as no changes and merging process will not be started
- When using Python Formatter additional linting is performed after formatting

## Usage

To format a **specified file** use `format_file` function.

To format an **entire directory** use `format_dir` function.

You can specify a formatter setup file via `setup_path` parameter.

By default logger from `logging` module is used but you can specify your own logger via `logger` parameter.

Formatting without Meld is available via `with_meld` parameter.

