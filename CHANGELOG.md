# CHANGELOG.md

This file contains all notable changes to the [dirwalker][] project.

## Unreleased

### Added

- Build with [hatchling][] from a `pyproject.toml`, laid out under `src/`.
  The module moved from `dirwalker.py` at the repository root to
  `src/dirwalker/dirwalker.py`, re-exported from `src/dirwalker/__init__.py`,
  so `import dirwalker` and `dirwalker.find_filenames_with_extensions()` still
  read the same from the outside. The `src/` layout is what makes the test
  suite import the installed package rather than the working copy sitting in
  the current directory, which is the only arrangement under which the tests
  say anything about what a user would get.
- Type hints throughout, checked by [pyright][], with a `py.typed` marker so
  that the annotations are visible to anyone type checking against this
  package rather than stopping at its edge.
- Test on Python 3.12, 3.13, and 3.14 in a [CI workflow][] on GitHub Actions,
  which lints with [ruff][], type checks with pyright, runs the suite, and
  reports coverage to [Coveralls][coveralls link]. Travis-CI stopped running
  for this repository years ago; every check since then has been whatever the
  person pushing happened to run.
- Audit the workflows with [zizmor][] in CI and in `just lint`. Everything
  under `src/` is linted on every push, and the workflows, the part of this
  repository that can mint a PyPI credential, would otherwise be read by eye
  alone. It runs as a job of its own rather than as a step gated on one leg of
  the matrix: that gate would mean dropping a Python version silently stops
  the audit.
- Require the suite to cover every statement and branch. A floor set anywhere
  below that would let coverage fall without anything noticing.
- Publish from a [release workflow][] triggered by a `v*` tag, in place of the
  `python setup.py register sdist upload` that `tasks.py` ran from a
  developer's machine. It waits on the whole CI workflow, checks that the
  tagged commit is on `master`, checks the tag against the version in
  `pyproject.toml`, builds, and installs the built wheel somewhere `src/`
  cannot be reached to import it there, which is the only check that can catch
  a packaging mistake that left something out of the distribution. There is no
  PyPI API token anywhere: it authenticates with [trusted publishing][], and
  that same OIDC identity signs a [PEP 740][] attestation for each
  distribution. A [GitHub release][releases] follows the upload, carrying the
  CHANGELOG section for the version as its notes.
- A `Justfile` holding the lint, test, coverage, dependency, build, and
  release recipes. `just release` refuses to start against a dirty working
  tree, off `master`, on a `master` behind its upstream, with an empty
  Unreleased section, or when the tag it would create already exists, then
  shows the entries waiting under Unreleased next to the version each kind of
  bump would produce and asks which to cut. `tasks.py` asked the same
  questions as printed reminders and trusted the answers.
- Put the actions and the Python dependencies under [Dependabot][]. The
  actions in both workflows are pinned to commit SHAs, since a tag is mutable
  and the release job can mint a PyPI credential, and a pin with nothing
  updating it is a decision to stay on one commit forever.

### Changed

- Require Python 3.12 or newer, dropping 2.6, 2.7, 3.3, and 3.4. All four have
  been end of life for years, and the `from __future__` imports the module
  carried for them are gone.
- Manage the development environment with [uv][] and its lock file, replacing
  the pinned `requirements.txt`, and run the recipes with [Just][] rather than
  [invoke][]. Test with [pytest][] rather than [nose][], which does not run on
  any supported Python. Lint and format with ruff rather than flake8.
- Single source the version in `pyproject.toml`. It used to live in
  `__version__` in the module, which `setup.py` read back out with a regular
  expression; `uv version --bump` now owns it, and nothing has to be kept in
  step by hand.
- Match each extension with one `str.endswith()` call over a tuple of
  suffixes, rather than a loop over the extensions for every filename. The
  matching is unchanged: an extension may still be given with or without its
  leading period.
- Remove `AUTHORS.md` and the copyright notice's reference to it. The notice
  in `LICENSE.txt` read "The dirwalker developers (see AUTHORS.md)", and
  `AUTHORS.md` is not in the wheel: `license-files` carries `LICENSE.txt` into
  `dist-info/licenses/` and nothing carries the other, so every installed copy
  pointed at a file that was not there. A license travels into vendored trees
  and distro packages without the repository around it, so the notice has to
  stand on its own. It now names the same holder the source file headers have
  always named, and the file it used to defer to, which listed one person and
  two empty sections, is gone.
- Rewrite the suite as pytest functions with fixtures rather than a
  `unittest.TestCase` with a `setUp` that built eleven paths for tests that
  each used one or two of them. The test that searched `./tests/sample_dir/`
  passed only when pytest was invoked from the repository root; it now sets
  the working directory it depends on.
- Replace `.gitignore` with the standard Python template, which covers the
  tooling this project now uses.

### Fixed

- A non-recursive search returned a subdirectory whose own name ended in one
  of the extensions, e.g. an `archive.txt/` directory for `.txt`. The
  recursive branch never did, since `os.walk()` lists a directory under `dirs`
  rather than `files`, and the two branches answering differently for the same
  tree is not something a caller can use.

### Removed

- `dirwalker.__version__`. It existed for `setup.py` to read. The version now
  lives in the package metadata, which `importlib.metadata.version()` reads,
  so the module no longer carries a copy that can fall out of step with the
  one being published.
- The Travis-CI configuration, `setup.py`, `setup.cfg`, `MANIFEST.in`,
  `requirements.txt`, `tasks.py`, and `AUTHORS.md`.

## v0.5.0 - 2015-08-20

### Added

- Added coverage
- Migrated Travis from legacy to container-based infrastructure

## v0.4.1 - 2014-08-08

### Fixed

- Fix links to GitHub repo

## v0.4 - 2014-08-08

### Fixed

- Return a set instead of an array

## v0.3.2 - 2014-08-08

### Fixed

- Travis-CI fails for 2.7, 3.3, and 3.4. Skipping one unit test to try
  and resolve.

## v0.3.1 - 2014-08-08

### Fixed

- Travis-CI failed. Updated requirements.txt and confirmed that tests
  pass on local machine using Python 2.6.8, 2.7.8, and 3.4.1

## v0.3 - 2014-08-08

### Added

- Changed from git-flow to Github Flow
- Changed badges to shields.io
- Moved CHANGES.md to CHANGELOG.md
- Updated README.md
- Updated all links related to moving GitHub repo.
  - **Old:** https://github.com/matthewrankin/dirwalker
  - **New:** https://github.com/questrail/dirwalker

## v0.2.2 - 2014-01-23

### Added

- Added unit test for multiple extensions

## v0.2.1 - 2014-01-23

### Fixed

- Corrected v0.2 release

## v0.1.6 - 2014-01-23

### Fixed

- Fixed setup.py for README.md to rst

## v0.1.5 - 2014-01-23

### Fixed

- Fixed tasks.py for release

## v0.1.4 - 2014-01-23

### Added

- Changed setup.py to convert README.md to rst

## v0.1.2 - 2014-01-21

### Added

- Added MIT-license
- Added unit tests
- Converted from distutils to setuptools
- Began using git-flow development process
- Began using invoke tasks for automation

## v0.1 - 2010-11-16

### Added

- Initial release to Github. Not released to PyPI.

[coveralls link]: https://coveralls.io/github/questrail/dirwalker?branch=master
[CI workflow]: https://github.com/questrail/dirwalker/blob/master/.github/workflows/ci.yml
[Dependabot]: https://docs.github.com/en/code-security/dependabot
[dirwalker]: https://github.com/questrail/dirwalker
[hatchling]: https://hatch.pypa.io/latest/
[invoke]: https://www.pyinvoke.org/
[just]: https://just.systems/
[nose]: https://nose.readthedocs.io/
[PEP 740]: https://peps.python.org/pep-0740/
[pyright]: https://microsoft.github.io/pyright/
[pytest]: https://docs.pytest.org/
[release workflow]: https://github.com/questrail/dirwalker/blob/master/.github/workflows/release.yml
[releases]: https://github.com/questrail/dirwalker/releases
[ruff]: https://docs.astral.sh/ruff/
[trusted publishing]: https://docs.pypi.org/trusted-publishers/
[uv]: https://docs.astral.sh/uv/
[zizmor]: https://docs.zizmor.sh/
