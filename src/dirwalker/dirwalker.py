# Copyright (c) 2010-2026 The dirwalker developers. All rights reserved.
# Project site: https://github.com/questrail/dirwalker
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Walk a directory searching for certain file extensions.

This package will walk multiple-level directories searching for files with the
given extensions.
"""

# Standard module imports
import os
from collections.abc import Iterable


def find_filenames_with_extensions(
    search_directory: str | os.PathLike[str],
    extensions: Iterable[str],
    recurse: bool = True,
) -> set[str]:
    """Find filenames with given extensions.

    An extension is matched against the end of the filename, so it may be
    given with or without its leading period: both 'csv' and '.csv' find
    `readings.csv`.

    Args:
        search_directory: The absolute or relative directory to search.
        extensions: The extensions to look for, as a sequence of strings.
            Passing a bare string matches each of its characters separately.
        recurse: Whether or not to recurse any subdirectories.

    Returns:
        A set of the absolute paths of the files found.
    """
    # str.endswith takes a tuple of suffixes and tries each of them, which is
    # what this needs and saves a loop over the extensions per filename.
    suffixes = tuple(extensions)
    search_directory = os.path.abspath(search_directory)
    files_found: set[str] = set()

    if recurse:
        for root, _dirs, files in os.walk(search_directory):
            files_found.update(
                os.path.join(root, filename)
                for filename in files
                if filename.endswith(suffixes)
            )
    else:
        # scandir rather than listdir, so that a directory whose own name ends
        # in one of the extensions is passed over. os.walk above lists it
        # under dirs rather than files and never matches it, and the two
        # branches answering differently is not something a caller can use.
        with os.scandir(search_directory) as entries:
            files_found.update(
                entry.path
                for entry in entries
                if entry.name.endswith(suffixes) and entry.is_file()
            )

    return files_found
