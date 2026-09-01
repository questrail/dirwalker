# Copyright (c) 2010-2026 The dirwalker developers. All rights reserved.
# Project site: https://github.com/questrail/dirwalker
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Unit tests for dirwalker.py."""

import os.path

import pytest

import dirwalker


@pytest.fixture
def sample_dir():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample_dir")


@pytest.fixture
def sample_file(sample_dir):
    def path(*parts):
        return os.path.join(sample_dir, *parts)

    return path


def test_find_single_file_without_extension_period(sample_dir, sample_file):
    """Find extensions that don't have a period"""
    assert dirwalker.find_filenames_with_extensions(sample_dir, ["js"]) == {
        sample_file("sample_file_06.js")
    }


def test_find_single_file_with_extension_period(sample_dir, sample_file):
    """Find extensions that have a period"""
    assert dirwalker.find_filenames_with_extensions(sample_dir, [".js"]) == {
        sample_file("sample_file_06.js")
    }


def test_find_multiple_files_recursively(sample_dir, sample_file):
    """Find extensions in recursive directories"""
    assert dirwalker.find_filenames_with_extensions(sample_dir, ["txt"]) == {
        sample_file("sample_file_01.txt"),
        sample_file("sample_file_02.txt"),
        sample_file("sample_dir_level_2", "sample_level_2_file_01.txt"),
        sample_file("sample_dir_level_2", "sample_level_2_file_02.txt"),
    }


def test_find_multiple_files_without_recursion(sample_dir, sample_file):
    """Find extensions without recursing subdirectories"""
    assert dirwalker.find_filenames_with_extensions(
        sample_dir, ["txt"], recurse=False
    ) == {
        sample_file("sample_file_01.txt"),
        sample_file("sample_file_02.txt"),
    }


def test_find_multiple_extensions(sample_dir, sample_file):
    """Find more than one extension"""
    assert dirwalker.find_filenames_with_extensions(sample_dir, ["js", ".py"]) == {
        sample_file("sample_file_05.py"),
        sample_file("sample_file_06.js"),
        sample_file("sample_dir_level_2", "sample_level_2_file_05.py"),
    }


def test_no_match_returns_an_empty_set(sample_dir):
    """An extension nothing in the tree carries finds nothing"""
    assert dirwalker.find_filenames_with_extensions(sample_dir, [".rs"]) == set()


def test_relative_path_is_resolved(monkeypatch, sample_dir, sample_file):
    """A relative directory is resolved against the working directory"""
    monkeypatch.chdir(os.path.dirname(sample_dir))
    assert dirwalker.find_filenames_with_extensions("./sample_dir/", [".js"]) == {
        sample_file("sample_file_06.js")
    }


@pytest.mark.parametrize("recurse", [True, False])
def test_a_directory_named_like_a_match_is_not_returned(tmp_path, recurse):
    """A subdirectory whose own name ends in the extension is not a match

    os.walk lists it under dirs rather than files, so the recursive branch
    never matched it; the non-recursive branch has to pass over it too, or the
    two answer differently for the same tree.
    """
    (tmp_path / "notes.txt").write_text("")
    (tmp_path / "archive.txt").mkdir()

    assert dirwalker.find_filenames_with_extensions(
        tmp_path, [".txt"], recurse=recurse
    ) == {str(tmp_path / "notes.txt")}
